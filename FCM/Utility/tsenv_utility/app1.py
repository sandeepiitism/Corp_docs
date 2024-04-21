from flask import Flask, render_template, request
import pandas as pd
from prophet import Prophet

app = Flask(__name__)

def forecast_prophet(df, column_name):
    tank_708_before = df[["Date", column_name]]
    tank_708_before.columns = ['ds', 'y']
    train = tank_708_before.iloc[:1120]
    test = tank_708_before.iloc[1120:]
    m = Prophet()
    m.fit(train)
    future = m.make_future_dataframe(periods=3, freq='D')
    forecast = m.predict(future)
    result = forecast.iloc[-1:][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    ds = pd.to_datetime(result['ds'].values[0]).strftime("%Y-%m-%d")
    yhat = round(result['yhat'].values[0], 2)
    yhat_lower = round(result['yhat_lower'].values[0], 2)
    yhat_upper = round(result['yhat_upper'].values[0], 2)
    return ds, yhat, yhat_lower, yhat_upper

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            df = pd.read_excel(uploaded_file)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            unique_tanks = df['Tank'].unique().tolist()
            
            if 'tank_number' in request.form:
                selected_tank = request.form['tank_number']
                df_filtered = df[df['Tank'] == selected_tank]

                ds_pH, yhat_pH, yhat_lower_pH, yhat_upper_pH = forecast_prophet(df_filtered, "pH")
                ds_conductivity, yhat_conductivity, yhat_lower_conductivity, yhat_upper_conductivity = forecast_prophet(df_filtered, "Cond ")
                ds_bod, yhat_bod, yhat_lower_bod, yhat_upper_bod = forecast_prophet(df_filtered, "BOD ")
                ds_cod, yhat_cod, yhat_lower_cod, yhat_upper_cod = forecast_prophet(df_filtered, "COD")
                ds_toc, yhat_toc, yhat_lower_toc, yhat_upper_toc = forecast_prophet(df_filtered, "TOC")
                ds_turb, yhat_turb, yhat_lower_turb, yhat_upper_turb = forecast_prophet(df_filtered, 'Turb ')

                result = {
                    'forecasted_pH': yhat_pH,
                    'forecasted_min_pH': yhat_lower_pH,
                    'forecasted_max_pH': yhat_upper_pH,
                    'forecast_date_pH': ds_pH,

                    'forecasted_conductivity': yhat_conductivity,
                    'forecasted_min_conductivity': yhat_lower_conductivity,
                    'forecasted_max_conductivity': yhat_upper_conductivity,
                    'forecast_date_conductivity': ds_conductivity,

                    'forecasted_bod': yhat_bod,
                    'forecasted_min_bod': yhat_lower_bod,
                    'forecasted_max_bod': yhat_upper_bod,
                    'forecast_date_bod': ds_bod,

                    'forecasted_cod': yhat_cod,
                    'forecasted_min_cod': yhat_lower_cod,
                    'forecasted_max_cod': yhat_upper_cod,
                    'forecast_date_cod': ds_cod,

                    'forecasted_toc': yhat_toc,
                    'forecasted_min_toc': yhat_lower_toc,
                    'forecasted_max_toc': yhat_upper_toc,
                    'forecast_date_toc': ds_toc,

                    'forecasted_turb': yhat_turb,
                    'forecasted_min_turb': yhat_lower_turb,
                    'forecasted_max_turb': yhat_upper_turb,
                    'forecast_date_turb': ds_turb
                }

                return render_template('result.html', result=result, unique_tanks=unique_tanks)

    return render_template('index1.html', unique_tanks=[])

if __name__ == '__main__':
    app.run(debug=True)

    #### changing the port
    app.run(host="0.0.0.0", port=8000)
