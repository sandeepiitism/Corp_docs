import pandas as pd
from prophet import Prophet
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, ttk
import io

columns_coolant = ['ds', 'y', 'tool']
columns_temp = ['ds', 'y', 'y1']

df_coolant = pd.read_csv('notebook/test.csv')
df_temp = pd.read_csv('notebook/temp.csv')


def forecast_prophet_coolant(df, tool, days):
    tool_df = df[df['tool'] == tool]

    if len(tool_df) < 2:
        raise ValueError(f" {tool} is not a gun drill.")

    tool_df = tool_df[['ds', 'y']].rename(columns={'ds': 'ds', 'y': 'y'})

    model = Prophet()
    model.fit(tool_df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


def forecast_prophet_temp(df, tool, days):
    df = df[['ds', 'y']].rename(columns={'ds': 'ds', 'y': 'y'})

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]


def get_forecast_coolant():
    tool = int(tool_var.get())
    days = int(days_entry.get())

    # Check if the selected machine is not 'dz9'
    if machine_var.get() != 'dz9':
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Work under progress for {machine_var.get()} machine type")
        return

    if tool == 23 or tool == 7:
        try:
            result_df = forecast_prophet_coolant(df_coolant, tool, days)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result_df.tail(days).to_string(index=False))
        except ValueError as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, str(e))
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"{tool} is not a gun drill.")


def get_forecast_temp():
    tool = int(tool_var.get())
    days = int(days_entry.get())

    # Check if the selected machine is not 'dz9'
    if machine_var.get() != 'dz9':
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Work under progress for {machine_var.get()} machine type")
        return

    try:
        result_df = forecast_prophet_temp(df_temp, tool, days)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result_df.tail(days).to_string(index=False))
    except ValueError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, str(e))


root = tk.Tk()
root.title("Chiron Analytics")

title_label = Label(root, text="Chiron Analytics", font=("Helvetica", 16), fg="red", bg="yellow")
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

machine_label = Label(root, text="Select Machine:")
machine_label.grid(row=1, column=0, sticky="e", padx=(20, 10))

machines = ['dz1', 'dz2', 'dz3', 'dz4', 'dz5', 'dz6', 'dz7', 'dz8', 'dz9', 'dz10', 'dz11']
machine_var = StringVar()
machine_combobox = ttk.Combobox(root, textvariable=machine_var, values=machines, state='readonly')
machine_combobox.grid(row=1, column=1, padx=(0, 20), pady=(10, 10), sticky="w")

tool_label = Label(root, text="Select Tool:")
tool_label.grid(row=2, column=0, sticky="e", padx=(20, 10))

tool_var = StringVar()
tool_entry = Entry(root, textvariable=tool_var)
tool_entry.grid(row=2, column=1, pady=(0, 10), sticky="w")

days_label = Label(root, text="Number of Days to Forecast:")
days_label.grid(row=3, column=0, sticky="e", padx=(20, 10))

days_entry = Entry(root)
days_entry.grid(row=3, column=1, pady=(0, 10), sticky="w")

forecast_coolant_button = Button(root, text="Get Coolant Forecast", command=get_forecast_coolant)
forecast_coolant_button.grid(row=4, column=0, pady=(10, 20))

forecast_temp_button = Button(root, text="Get Temperature Forecast", command=get_forecast_temp)
forecast_temp_button.grid(row=4, column=1, pady=(10, 20))

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=5, column=0, columnspan=2, pady=(0, 20))

made_by_label = Label(root, text="Testing Phase 💻 by Sandeep", font=("Helvetica", 10))
made_by_label.grid(row=6, column=0, columnspan=2, pady=(10, 20))

root.mainloop()
