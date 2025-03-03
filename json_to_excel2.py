import pandas as pd
import json
import re
import numpy as np

def encode_warning_level(warning_level):
    return 1.0 if warning_level == "High" else 0.5 if warning_level == "Medium" else 0

def encode_kalman_result(kalman_result):
    return 1.0 if kalman_result == "High" else 0.5 if kalman_result == "Medium" else 0.25 if kalman_result == "Low" else 0

def calculate_weights(df):
    df['prev_kalman_result'] = df['kalman_result'].shift()

    # Apply the conditions using vectorized operations
    df.loc[df['prev_kalman_result'] == "Low", 'w1'] = 0.3
    df.loc[df['prev_kalman_result'] == "Low", 'w2'] = (1 - df['w1']) / 2 + 0.1
    df.loc[df['prev_kalman_result'] == "Low", 'w3'] = (1 - df['w1']) / 2 - 0.1

    # Gradually reduce w1 and w3 for "Medium" and "High"
    reduction_factor = 0.01

    for i in range(1, len(df)):
        prev_kalman = df.loc[i - 1, 'kalman_result']
        
        if prev_kalman in ["Medium", "High"]:
            df.loc[i, 'w1'] = max(df.loc[i - 1, 'w1'] - reduction_factor, 0)  # Reduce w1
            df.loc[i, 'w3'] = max(df.loc[i - 1, 'w3'] - reduction_factor, 0.4)  # Reduce w3
            df.loc[i, 'w2'] = 1 - df.loc[i, 'w1'] - df.loc[i, 'w3']          # Adjust w2
        elif prev_kalman == "Low":
            df.loc[i, 'w1'] = 0.3
            df.loc[i, 'w2'] = (1 - df.loc[i, 'w1']) / 2 + 0.1
            df.loc[i, 'w3'] = (1 - df.loc[i, 'w1']) / 2 - 0.1

    # Drop the helper column if not needed
    df = df.drop(columns=['prev_kalman_result'])
    return df

# Initialize variables
json_data = []
file_name= "Testing_files/Results/6T_SR.txt"
kalman_file_name = "UKF/6T_SR_ukf.csv"
data = []
chunk_size = 7
# Open and read the file
with open(file_name, "r") as f:
    for i, line in enumerate(f.readlines(), start=1):
        data.append(line.strip())  # Accumulate the line into data
        if i % chunk_size == 0:  # When we've accumulated 'chunk_size' lines
            # Join all the lines in the chunk to form a valid JSON string
            json_str = ''.join(data)
            try:
                # Parse the JSON string to check for validity and store it
                json_object = json.loads(json_str)
                json_data.append(json_object)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {json_str}")
            data = []  # Reset data for the next chunk

kalman_df = pd.read_csv(kalman_file_name)
# Convert json_data (list of JSON objects) to DataFrame
df = pd.DataFrame(json_data)

# Replace Kalman data if needed
df["kalman_result"] = kalman_df["SpoofingLevel"]
df["mock_loc"] = df["mock_loc"].astype(int)
df["warning_level_encoded"] = df["warning_level"].apply(encode_warning_level)
df["kalman_result_encoded"] = df["kalman_result"].apply(encode_kalman_result)
df["lstm_prediction"] = df["lstm_prediction"].replace("waiting for more data", 0)

# df["w2"] = (1 - df["w1"]) / 2 - .1 # Kalman
# df["w3"] = (1 - df["w1"]) / 2 + .1 # LSTM
df = calculate_weights(df)


df["pred"] = df["w1"]*df["warning_level_encoded"]+df["w2"]*df["kalman_result_encoded"]+df["w3"]*df["lstm_prediction"] 
thresholds = [.5,.55,.6,.65, .70, .75, .80, .90]
for thresh in thresholds:
    column = f"thresh_{thresh}"
    df[column] = (df["pred"] > thresh).astype(int)
    accuracy = (df["mock_loc"] == df[column]).mean() * 100
    print(f"Accuracy for {column}: {accuracy:.2f}%")


# For debugging, print the first few rows of the DataFrame
# print(df.head())

# Optionally, save the DataFrame to Excel
for_excel_name = re.search(r'([^/\\]+)\.txt$', file_name).group(1)
excel_filename = "Processed_test_files/"+for_excel_name+".xlsx"
df.to_excel(excel_filename, index=False)
print(f"JSON data has been successfully converted to {excel_filename}")
