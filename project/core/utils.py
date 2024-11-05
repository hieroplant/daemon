import pandas as pd

def is_valid_sheet_name(sheet_name):
    if len(sheet_name) < 4:
        return False
    
    return (
        sheet_name.startswith("_0") and
        sheet_name[4] != '9' and
        all(char in "_0123456789" for char in sheet_name)
    )

def extract_station_info(file):
    station_info = []
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        if is_valid_sheet_name(sheet_name):
            df = pd.read_excel(xls, sheet_name=sheet_name)
            station_info.append((sheet_name, df.iloc[2, 1]))  # Get value from B3
    return station_info

def extract_fail_code_data(file):
    fail_code_data = []
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        if is_valid_sheet_name(sheet_name):
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Extract fail code data
            if "Fail Code" in df.iloc[:, 0].values and "Fail Code End" in df.iloc[:, 0].values:
                start_row = df[df.iloc[:, 0].str.contains("Fail Code", na=False)].index[0]
                end_row = df[df.iloc[:, 0].str.contains("Fail Code End", na=False)].index[0]
                fail_code_data.extend(df.iloc[start_row + 1:end_row, 1].tolist())  # Get data from column B
    return fail_code_data