import warnings
warnings.filterwarnings("ignore")
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from datetime import datetime

# some definitions
WINDOW_SIZE = 20
FORECAST_STEPS = 10
N_FEATURES = 12  # total input features
N_TARGETS = 7  # 7 weather features
MODEL_PATH = os.environ.get("MODEL_PATH", "Weights/model.h5")
SCALER_X_PATH = os.environ.get("SCALER_X_PATH", "Weights/scaler_x.pkl")
SCALER_Y_PATH = os.environ.get("SCALER_Y_PATH", "Weights/scaler_y.pkl")

ordered_cols = [ # The 12 input features, ordered
        "temperature_C",
        "pressure_hPa",
        "humidity_%",
        "wind_speed_mps",
        "wind_dir_deg",
        "solar_radiation_Wm2",
        "rain_mm_h",
        "hour",
        "month",
        "WeekDay",
        "YearDay",
        "quarter"
    ]

weather_cols = [ # The required 7 features
        "temperature_C",
        "pressure_hPa",
        "humidity_%",
        "wind_speed_mps",
        "wind_dir_deg",
        "solar_radiation_Wm2",
        "rain_mm_h"
    ]

feature_units = {
    "temperature_C": "°C",
    "pressure_hPa": "hPa",
    "humidity_%": "%",
    "wind_speed_mps": "m/s",
    "wind_dir_deg": "°",
    "solar_radiation_Wm2": "W/m²",
    "rain_mm_h": "mm/h"
}

app = Flask(__name__)

# Load model and scalers
print("Loading model and scalers...")
if os.path.exists(MODEL_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("Loaded full model from", MODEL_PATH)
    except Exception as e:
        raise RuntimeError("Failed to load model file. Error:" + str(e))
else:
    raise RuntimeError(f"Model path not found: {MODEL_PATH}")
if not os.path.exists(SCALER_X_PATH) or not os.path.exists(SCALER_Y_PATH):
    raise RuntimeError("Scaler files not found.")

scaler_x = joblib.load(SCALER_X_PATH)
scaler_y = joblib.load(SCALER_Y_PATH)
print("Scalers loaded.")


def get_time_based_features(dt):
    # Function to get the time based feature from each timeindex
    # Some differences between Pandas.DateTimeIndex & Python.Datetime.DateTime
    hour = dt.hour
    month = dt.month
    WeekDay = dt.weekday()
    YearDay = dt.timetuple().tm_yday
    quarter = (dt.month - 1) // 3 + 1
    return hour, month, WeekDay, YearDay, quarter


def build_input_features(ts, weather_feats):
    # Check if null or empty
    if pd.isna(ts):
        raise ValueError("Invalid timestamp: NaN or missing")
    ts = str(ts).strip()
    if not ts:
        raise ValueError("Invalid timestamp: empty string")
    # parse timestamp to get datetime format
    try:
        dt = datetime.fromisoformat(ts)
    except Exception:
        try: # Different time formats
            dt = datetime.strptime(ts, "%d/%m/%Y %H:%M")  # for CSV files
        except Exception:
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
            except Exception:
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    raise ValueError("Unsupported format")

    hour, month, WeekDay, YearDay, quarter = get_time_based_features(dt)
    row = [
        float(weather_feats["temperature_C"]),
        float(weather_feats["pressure_hPa"]),
        float(weather_feats["humidity_%"]),
        float(weather_feats["wind_speed_mps"]),
        float(weather_feats["wind_dir_deg"]),
        float(weather_feats["solar_radiation_Wm2"]),
        float(weather_feats["rain_mm_h"]),
        hour, month, WeekDay, YearDay, quarter
    ]
    return row


def preprocess_json(data):
    # validate length of records
    if len(data) < WINDOW_SIZE:
        raise ValueError(f"Need at least {WINDOW_SIZE} rows of data")
    rows = []
    for record in data[-WINDOW_SIZE:]:
        weather_feats = {
            "temperature_C": record["temperature_C"],
            "pressure_hPa": record["pressure_hPa"],
            "humidity_%": record["humidity_%"],
            "wind_speed_mps": record["wind_speed_mps"],
            "wind_dir_deg": record["wind_dir_deg"],
            "solar_radiation_Wm2": record["solar_radiation_Wm2"],
            "rain_mm_h": record["rain_mm_h"]
        }
        ts = record["timestamp"]
        rows.append(build_input_features(ts, weather_feats))

    arr = np.array(rows, dtype=float)
    if arr.shape != (WINDOW_SIZE, N_FEATURES):
        raise ValueError(f"Expected array shape ({WINDOW_SIZE},{N_FEATURES}), got {arr.shape}")
    scaled = scaler_x.transform(arr)
    return scaled.reshape(1, WINDOW_SIZE, N_FEATURES)


def preprocess_csv(df):
    # make sure the 7 weather columns exist
    if not set(weather_cols).issubset(df.columns):
        raise ValueError(f"Not matched columns.")

    # drop rows where timestamp or any weather col is NaN
    df = df.dropna(subset=weather_cols + ['timestamp'])
    if len(df) < WINDOW_SIZE:
        raise ValueError(f"Need at least {WINDOW_SIZE} valid rows of data")
    # get the last window_size predictions
    df_tail = df.tail(WINDOW_SIZE).copy()
    rows = []
    for _, row in df_tail.iterrows():
        weather_feats = {i : row[i] for i in weather_cols[:]}
        ts = row["timestamp"]
        rows.append(build_input_features(ts, weather_feats))

    arr = np.array(rows, dtype=float)
    if arr.shape != (WINDOW_SIZE, N_FEATURES):
        raise ValueError(f"Expected array shape ({WINDOW_SIZE},{N_FEATURES}), got {arr.shape}")
    scaled = scaler_x.transform(arr)
    return scaled.reshape(1, WINDOW_SIZE, N_FEATURES)


def postprocess_pred(prediction):
    flat = prediction.reshape(-1, N_TARGETS)  # (FORECAST_STEPS, N_TARGETS)
    inv = scaler_y.inverse_transform(flat)
    return inv.reshape(FORECAST_STEPS, N_TARGETS).tolist()


#-------------------API route-------------------#
# main route, simple definitions & routes
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Hourly Weather Forecast API",
        "routes": {
            "/health (GET)": "health check",
            "/predict (POST JSON)": "Send raw data with timestamp + 7 features",
            "/predict_file (POST CSV file)": "Upload CSV with timestamp + 7 features"
        },
        "required_columns": weather_cols,
        "note": f"Must send the last {WINDOW_SIZE} hours of data."
    })


# health check route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# route to predict with json request
@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        data = payload.get("data")
        x_scaled = preprocess_json(data)
        pred_s = model.predict(x_scaled)
        pred_orig = postprocess_pred(pred_s)

        forecast_vals = []
        for hour_idx, row in enumerate(pred_orig, 1):
            hour_data = {}
            for col_idx, value in enumerate(row):
                feat = weather_cols[col_idx]
                unit = feature_units[feat]
                hour_data[feat] = f"{value:.3f} {unit}"
            forecast_vals.append({"hour": hour_idx, "values": hour_data})

        return jsonify({"forecast": forecast_vals})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# route to predict with csv files
@app.route("/predict_file", methods=["POST"])
def predict_file():
    try:
        if "file" not in request.files:
            raise ValueError("No file uploaded.")
        f = request.files["file"]
        df = pd.read_csv(f)
        # if timestamp is the index
        if "timestamp" not in df.columns:
            df = df.reset_index().rename(columns={"index": "timestamp"})
        x_scaled = preprocess_csv(df)
        pred_s = model.predict(x_scaled)
        pred_orig = postprocess_pred(pred_s)

        forecast_vals = []
        for hour_idx, row in enumerate(pred_orig, 1):
            hour_data = {}
            for col_idx, value in enumerate(row):
                feat = weather_cols[col_idx]
                unit = feature_units[feat]
                hour_data[feat] = f"{value:.3f} {unit}"
            forecast_vals.append({"hour": hour_idx, "values": hour_data})

        return jsonify({"forecast": forecast_vals})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

