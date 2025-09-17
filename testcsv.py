import requests

# the API URL, from Flask server
url = "http://127.0.0.1:5000/predict_file"

# open the file & send POST request
files = {'file': open("Test/2.csv", "rb")}
response = requests.post(url, files=files)
print(response.json())
