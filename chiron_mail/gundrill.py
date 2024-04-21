import pandas as pd
import numpy as np
from prophet import Prophet
import pyodbc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def establish_database_connection():
    return pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "Server=na0vm00024.apac.bosch.com;"
                          "Database=DB_MFC2DB_SQL;"
                          "Trusted_Connection=yes;")

def retrieve_data(connection):
    sql = """SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz10' AS dz
        FROM [ChironDZ10]
        WHERE [PresentTool] =8
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz9' AS dz
        FROM [ChironDZ9_1]
        WHERE [PresentTool] IN (7, 23)
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz8' AS dz
        FROM [ChironDZ8]
        WHERE [PresentTool] =18
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz7' AS dz
        FROM [ChironDZ7]
        WHERE [PresentTool] =8
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz6' AS dz
        FROM [ChironDZ6]
        WHERE [PresentTool] IN (7, 23)
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz4' AS dz
        FROM [ChironDZ4]
        WHERE [PresentTool] IN (8, 23)
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz3' AS dz
        FROM [ChironDZ3]
        WHERE [PresentTool] IN (8, 23)
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz2' AS dz
        FROM [ChironDZ2]
        WHERE [PresentTool] IN (8, 23)
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        UNION

        SELECT CONVERT(date, [TimeStamp]) AS ds, MAX([CoolantPr]) AS y, [PresentTool] AS tool, 'dz1' AS dz
        FROM [ChironDZ1]
        WHERE [PresentTool] IN (8, 23)
        GROUP BY [PresentTool], CONVERT(date, [TimeStamp])

        ORDER BY ds ASC;""" 
    return pd.read_sql_query(sql, connection, parse_dates=True)

def train_prophet_model(data, tool, dz):
    df = data[(data['tool'] == tool) & (data['dz'] == dz)]

    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    result = result.rename(columns={'ds': 'date', 'yhat': 'predicted', 'yhat_lower': 'lower_range', 'yhat_upper': 'upper_range'})
    return result.tail(1)

def send_email(subject, body, sender, receiver, password, server_address='rb-smtp-auth.rbesz01.com', port=25):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(server_address, port)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)


def main():
    connection = establish_database_connection()
    data = retrieve_data(connection)
    machine_tools = [(8, 'dz1'), (23, 'dz1'), (8, 'dz2'), (23, 'dz2'), (8, 'dz3'), (23, 'dz3'), 
                     (8, 'dz4'), (23, 'dz4'), (7, 'dz6'), (23, 'dz6'), (8, 'dz7'), (18, 'dz8'), 
                     (7, 'dz9'), (23, 'dz9')]

    results = {}
    for tool, dz in machine_tools:
        result = train_prophet_model(data, tool, dz)
        key = f'{dz}_tool{tool}'
        results[key] = result

    email_body = "\n".join([f"Date: {np.datetime_as_string(value['date'].values[0], unit='D')}, Machine: {key}, Predicted coolant_value: {value['predicted'].values[0]:.2f}" for key, value in results.items()])
    email_body += "\n\n*Note: If Predicted Date doesn't matches, Machine is either stopped or data is not captured in the database."
    # receivers = ['chs9na@bosch.com', 'plp1na@bosch.com', 'bbk1na@bosch.com', 'wat2na@bosch.com']
    send_email('DZ Machine Gundrill Coolant_pr | Predicted Result ', email_body, 'chs9na@bosch.com', 'chs9na@bosch.com', 'Welcome@Nashik2')

if __name__ == "__main__":
    main()






