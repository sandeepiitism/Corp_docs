import pandas as pd

def fcm_eda(filename, sheet_index):
    data = pd.read_excel(filename, skiprows=3, sheet_name=sheet_index)
    data.columns = ["Date", "Tank No.", "Batch No.", "pH", "Cond", "BOD", "COD", "TOC", "Turb", 
                    "Hardness", "Remark", "Type of Effluent"]

    data = data.drop(0)
    data['Date'].fillna(method='ffill', inplace=True)
    new_data = data[data["Tank No."].fillna("").str.contains("\(Before\)")]
    new_data = new_data[["Date", "Tank No.", "Batch No.", "pH", "Cond", "BOD", "COD", "TOC", "Turb"]]
    new_data['Tank No.'] = new_data['Tank No.'].str.replace(r'\s*\(\s*Before\s*\)\s*', '', regex=True)
    return new_data

fcm_df = fcm_eda("fcm_data_2.xlsx", sheet_index=5)
print(fcm_df.tail(10))



