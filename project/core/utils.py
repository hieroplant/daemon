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
    station_info = {}
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        if is_valid_sheet_name(sheet_name):
            df = pd.read_excel(xls, sheet_name=sheet_name)
            station_info[sheet_name] = df
    return station_info

import pandas as pd

def extract_fail_code_data(df):
    """
    Extract pairs of 'Fail Code ID' and 'Description' from the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing the relevant data.
        
    Returns:
        list: List of tuples where each tuple contains ('Fail Code ID', 'Description').
    """
    fail_code_data = []
    
    # Check if both 'Fail Code' and 'Fail Code End' are present in the first column
    if "Fail Code" in df.iloc[:, 0].dropna().values and "Fail Code End" in df.iloc[:, 0].dropna().values:
        try:
            # Find the start and end rows based on the "Fail Code" and "Fail Code End" markers
            start_row = df[df.iloc[:, 0].str.contains("Fail Code", na=False)].index[0]
            end_row = df[df.iloc[:, 0].str.contains("Fail Code End", na=False)].index[0]

            # Extract the relevant rows from columns A and B
            fail_code_ids = df.iloc[start_row + 1:end_row, 0].astype(str).fillna("").tolist()  # Fail Code IDs from column A
            descriptions = df.iloc[start_row + 1:end_row, 1].astype(str).fillna("").tolist()   # Descriptions from column B
            
            # Check if both lists have the same length
            if len(fail_code_ids) == len(descriptions):
                # Zip the lists together into pairs of ('Fail Code ID', 'Description')
                fail_code_data.extend(zip(fail_code_ids, descriptions))
            else:
                print(f"Warning: Mismatched lengths between Fail Code IDs and Descriptions: {len(fail_code_ids)} vs {len(descriptions)}")

        except IndexError:
            print("Error: Unable to find the correct range between 'Fail Code' and 'Fail Code End'.")
    else:
        print("Markers 'Fail Code' and 'Fail Code End' not found in the first column.")
    
    return fail_code_data

