# Weather Forecasting API
## Introduction
This is API done using FLask to hourly forecast weather. We support the API with the previous 20 hourly data to predict the upcoming 10 hours. We can upload the data whether through json request or via csv file. And it accepts the timestamps in different formats.

## Weather Features
It works with these 7 features with the corresponding units: 
| Feature              | Unit    |
| -------------------- | ------- |
| Temperature          |  °C     |
| Pressure             |   hPa   |
| Humidity             |   %     |
| Wind Speed           |   m/s   |
| Wind Direction       |   °     |
| Solar Radiation      |   W/m²  |
| Rain                 |   mm/h  |


## Endpoints

### 1. / (main route)
- *Method*: GET
- *Description*: prints general information about the service and the available routes with some information about each one.

### 2. /health
- *Method*: GET
- *Description*: checks the health of the service to validate the server status

### 3. /predict
- *Method*: POST
- *Description*: we send the data as **json** request. This request must contain the required 7 features and the timestamp. It can be only these 8 columns or more.

### 4. /predict_file
- *Method*: POST
- *Description*: we send the data as **CSV** file. The file must contain the required features. It handles the null values and empty rows in the csv file.


## Usage

### 1. Clone the repository 
```
git clone https://github.com/DohaRagab1/WeatherForecasting.git
```

### 2. Install the required packages
```
pip install -r requirements.txt
```

### 3. Initialize the Flask server
Run `app.py` to initialize the server and open the current URL (in the terminal, Flask server). You can see the main route, and navigate to the health route to check the server.

### 4. Test with json request
You can test with examples of json requests in `Test folder` or your own requests. Run `testjson.py` but change the path of the json file. You will get the predictions from the model for the upcoming 10 hours.

### 5. Test with CSV files
You can test with examples of csv files in `Test folder` or your own file. Run `testcsv.py` but change the path of the csv file. You will get the predictions from the model for the upcoming 10 hours.

### 6. Convert from CSV to json file (*Optional*)
If you have CSV file, you can convert it to json file directly using `convert.py` but consider changing the paths of the files.
