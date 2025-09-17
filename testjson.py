import requests
import json

# the API URL, from Flask server
url = "http://127.0.0.1:5000/predict"

# Example payload: last 20 hours, 7 features + timestamp
'''payload = {
    "data": [
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 00:00:00","temperature_C":23.4,"pressure_hPa":1012.4,"humidity_%":60.1,"wind_speed_mps":3.2,"wind_dir_deg":180,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0},
        {"timestamp":"2025-09-16 01:00:00","temperature_C":23.1,"pressure_hPa":1012.5,"humidity_%":59.7,"wind_speed_mps":3.3,"wind_dir_deg":179,"solar_radiation_Wm2":0.0,"rain_mm_h":0.0}
    ]
}'''
with open("Test/2.json", "r") as f:
    payload = json.load(f)

# send POST request
response = requests.post(url, json=payload)
print(response.json())
