import pandas as pd
import re

def fcm_eda(filename, sheet_index=0):
    data = pd.read_excel(filename, skiprows=3, sheet_name=sheet_index)
    data.columns = ["Date", "Tank No.", "Batch No.", "pH", "Cond", "BOD", "COD", "TOC", "Turb", 
                    "Hardness", "Remark", "Type of Effluent"]

    data = data.drop(0)
    print(data)

print(fcm_eda("fcm_data.xlsx"))
#     data['Date'].fillna(method='ffill', inplace=True)
    

#     def extract_numerical_values(cell_value):
#         numerical_values = re.findall(r'\b\d+(?:\.\d+)?\b', str(cell_value))
#         if numerical_values:
#             return float(numerical_values[0])
#         else:
#             return None
    

#     for column in ["pH", "Cond", "BOD", "COD", "TOC", "Turb"]:
#         data[column] = data[column].apply(extract_numerical_values)
    
#     data.fillna(method='ffill', inplace=True)
    
#     data.dropna(subset=['Date'], inplace=True)
    
#     new_data = data[data["Tank No."].fillna("").str.contains("\(Before\)")]
#     new_data = new_data[["Date", "Tank No.", "Batch No.", "pH", "Cond", "BOD", "COD", "TOC", "Turb"]]
#     new_data['Tank No.'] = new_data['Tank No.'].str.replace(r'\s*\(\s*Before\s*\)\s*', '', regex=True)
#     return new_data

# fcm_df = fcm_eda("fcm_data.xlsx", sheet_index=0)
# fcm_df.head(10)