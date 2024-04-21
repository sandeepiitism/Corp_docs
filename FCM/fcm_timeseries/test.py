import pandas as pd
from prophet import Prophet
import numpy as np

def clean_data():
    data = pd.read_csv("cleaned_fcm.csv")
    return data[["Date", "Tank No.", "Hardness"]]

def create_prophet_model(dataframe):
    dataframe = dataframe.rename(columns={'Date': 'ds', 'Hardness': 'y'})
    if len(dataframe) < 2:
        raise ValueError("Dataframe has less than 2 non-NaN rows.")
    model = Prophet()
    model.fit(dataframe)
    return model

def forecast_hardness(model, forecast_date):
    future = pd.DataFrame({'ds': [forecast_date]})
    forecast = model.predict(future)
    return forecast['yhat'].iloc[0], forecast_date

def group_tank(tank_no, forecast_date):
    tank_df = df[df['Tank No.'] == tank_no]
    if tank_df.empty:
        print("Tank number not found in the data.")
        return None, None
    if tank_df.isnull().values.any():
        raise ValueError("Tank data contains missing values.")
    try:
        model = create_prophet_model(tank_df)
    except ValueError as e:
        print(e)
        return None, None
    hardness_forecast, forecast_date = forecast_hardness(model, forecast_date)
    return hardness_forecast, forecast_date

df = pd.DataFrame(clean_data())

tank_no = int(input("Enter tank number: "))
forecast_date = input("Enter forecast date (YYYY-MM-DD): ")

forecast_value, forecast_date = group_tank(tank_no, forecast_date)
if forecast_value is not None:
    print("Forecasted hardness for tank", tank_no, "on", forecast_date, ":", forecast_value)
