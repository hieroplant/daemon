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

# project/core/utils.py

def extract_fail_codes(file, sheet_name=None):
    fail_codes = {}
    xls = pd.ExcelFile(file)  # Open the Excel file
    
    # If a specific sheet name is provided, process only that sheet
    sheet_names = [sheet_name] if sheet_name else xls.sheet_names
    
    # Iterate through each sheet in the file
    for sheet in sheet_names:
        if is_valid_sheet_name(sheet):  # Assuming this function is defined elsewhere
            df = pd.read_excel(xls, sheet_name=sheet, header=None)  # Read the sheet into a DataFrame
            
            # Check if "Fail Code" and "Fail Code End" exist in the sheet
            if "Fail Code" not in df.iloc[:, 0].values or "Fail Code End" not in df.iloc[:, 0].values:
                print(f"Warning: 'Fail Code' or 'Fail Code End' not found in sheet '{sheet}'")
                continue
            
            try:
                start_idx = df[df.iloc[:, 0] == "Fail Code"].index[0] + 1
                end_idx = df[df.iloc[:, 0] == "Fail Code End"].index[0]
                
                # Extract fail codes and descriptions
                codes = df.iloc[start_idx:end_idx, 0].dropna().tolist()
                descriptions = df.iloc[start_idx:end_idx, 1].dropna().tolist()
                
                # Handle the case when codes and descriptions have different lengths
                if len(codes) != len(descriptions):
                    print(f"Warning: Mismatch between codes and descriptions in sheet '{sheet}'")
                    min_len = min(len(codes), len(descriptions))
                    codes = codes[:min_len]
                    descriptions = descriptions[:min_len]
                
                # Store the fail codes and descriptions in the dictionary
                fail_codes[sheet] = list(zip(codes, descriptions))
            
            except IndexError as e:
                print(f"Error processing sheet '{sheet}': {e}")
                continue
    return fail_codes