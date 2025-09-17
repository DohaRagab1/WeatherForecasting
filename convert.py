import pandas as pd
import json

csv_file = "Test/4.csv"
json_file = "Test/4.json"

df = pd.read_csv(csv_file)
# drop null values
df = df.dropna(subset=['timestamp'])
records = df.to_dict(orient="records")
payload = {"data": records}
with open(json_file, "w") as f:
    json.dump(payload, f, indent=4)

print("CSV file has been converted to JSON file.")