import pandas as pd
import numpy as np

def clean_data(sheet_name):
    data = pd.read_excel("fcm_data_2.xlsx", skiprows=2, sheet_name=sheet_name, usecols="A:K")
    data = data[["Date", "Tank No.", "pH", "Cond ", "BOD", "COD ", "TOC", "Turb ", 
                    "Hardness"]]
    data['Date'].fillna(method='ffill', inplace=True)
    data['Tank No.'] = data['Tank No.'].replace(r'^After\s*$', np.nan, regex=True)
    data['Tank No.'].fillna(method='ffill', inplace=True)
    data = data.dropna(subset=['Hardness'])
    data['Tank No.'] = data['Tank No.'].str.replace(r'\s*\(Before\)', '', regex=True)
    data['Tank No.'] = data['Tank No.'].str.replace(' \( Before \)', '')
    print(data)

clean_data(0)