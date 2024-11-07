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

def extract_actuators(file, sheet_name=None):
    actuators = {}
    xls = pd.ExcelFile(file)  # Open the Excel file
    
    # If a specific sheet name is provided, process only that sheet
    sheet_names = [sheet_name] if sheet_name else xls.sheet_names
    
    # Iterate through each sheet in the file
    for sheet in sheet_names:
        if is_valid_sheet_name(sheet):  # Assuming this function is defined elsewhere
            df = pd.read_excel(xls, sheet_name=sheet, header=None)  # Read the sheet into a DataFrame
            
            # Check if "Actuator" and "Actuator End" exist in the sheet
            if "Actuator" not in df.iloc[:, 0].values or "Actuator End" not in df.iloc[:, 0].values:
                print(f"Warning: 'Actuator' or 'Actuator End' not found in sheet '{sheet}'")
                continue
            
            try:
                start_idx = df[df.iloc[:, 0] == "Actuator"].index[0] + 1
                end_idx = df[df.iloc[:, 0] == "Actuator End"].index[0]
                
                # Extract the relevant portion of the DataFrame
                df = df.iloc[start_idx:end_idx]
                
                # Drop rows where all elements are NaN
                df = df.dropna(how='all')
                
                # Extract actuator data and fill empty cells with empty strings
                actuator_id = df.iloc[:, 0].fillna('').tolist()
                name = df.iloc[:, 1].fillna('').tolist()
                index = df.iloc[:, 2].fillna('').tolist()
                data_type = df.iloc[:, 3].fillna('').tolist()
                prefix = df.iloc[:, 4].fillna('').tolist()
                actuator_output = df.iloc[:, 5].fillna('').tolist()
                output_description = df.iloc[:, 6].fillna('').tolist()
                actuator_input = df.iloc[:, 7].fillna('').tolist()
                input_description = df.iloc[:, 8].fillna('').tolist()
                alm_0 = df.iloc[:, 9].fillna('').tolist()
                alm_1 = df.iloc[:, 10].fillna('').tolist()
                alm_0_description_language_1 = df.iloc[:, 11].fillna('').tolist()
                alm_0_description_language_2 = df.iloc[:, 12].fillna('').tolist()
                alm_0_description_language_3 = df.iloc[:, 13].fillna('').tolist()
                alm_1_description_language_1 = df.iloc[:, 14].fillna('').tolist()
                alm_2_description_language_2 = df.iloc[:, 15].fillna('').tolist()
                alm_3_description_language_3 = df.iloc[:, 16].fillna('').tolist()
                alm_0_procedure = df.iloc[:, 17].fillna('').tolist()
                alm_1_procedure = df.iloc[:, 18].fillna('').tolist()
                alm_0_bad = df.iloc[:, 19].fillna('').tolist()
                alm_1_bad = df.iloc[:, 20].fillna('').tolist()
                alm_0_cause = df.iloc[:, 21].fillna('').tolist()
                alm_1_cause = df.iloc[:, 22].fillna('').tolist()
                alm_0_action = df.iloc[:, 23].fillna('').tolist()
                alm_1_action = df.iloc[:, 24].fillna('').tolist()
                
                # Handle the case when lists have different lengths
                min_len = min(len(actuator_id), len(name), len(index), len(data_type), len(prefix), len(actuator_output), len(output_description), len(actuator_input), len(input_description), len(alm_0), len(alm_1), len(alm_0_description_language_1), len(alm_0_description_language_2), len(alm_0_description_language_3), len(alm_1_description_language_1), len(alm_2_description_language_2), len(alm_3_description_language_3), len(alm_0_procedure), len(alm_1_procedure), len(alm_0_bad), len(alm_1_bad), len(alm_0_cause), len(alm_1_cause), len(alm_0_action), len(alm_1_action))
                
                # Store the actuator data in the dictionary
                actuators[sheet] = [
                    {
                        'actuator_id': actuator_id[i],
                        'name': name[i],
                        'index': index[i],
                        'data_type': data_type[i],
                        'prefix': prefix[i],
                        'actuator_output': actuator_output[i],
                        'output_description': output_description[i],
                        'actuator_input': actuator_input[i],
                        'input_description': input_description[i],
                        'alm_0': alm_0[i],
                        'alm_1': alm_1[i],
                        'alm_0_description_language_1': alm_0_description_language_1[i],
                        'alm_0_description_language_2': alm_0_description_language_2[i],
                        'alm_0_description_language_3': alm_0_description_language_3[i],
                        'alm_1_description_language_1': alm_1_description_language_1[i],
                        'alm_2_description_language_2': alm_2_description_language_2[i],
                        'alm_3_description_language_3': alm_3_description_language_3[i],
                        'alm_0_procedure': alm_0_procedure[i],
                        'alm_1_procedure': alm_1_procedure[i],
                        'alm_0_bad': alm_0_bad[i],
                        'alm_1_bad': alm_1_bad[i],
                        'alm_0_cause': alm_0_cause[i],
                        'alm_1_cause': alm_1_cause[i],
                        'alm_0_action': alm_0_action[i],
                        'alm_1_action': alm_1_action[i],
                    }
                    for i in range(min_len)
                ]
            
            except IndexError as e:
                print(f"Error processing sheet '{sheet}': {e}")
                continue
    return actuators