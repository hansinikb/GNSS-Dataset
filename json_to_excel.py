import pandas as pd
import json
import re

def encode_warning_level(warning_level):
    return 1.0 if warning_level == "High" else 0.5 if warning_level == "Medium" else 0

def encode_kalman_result(kalman_result):
    return 1.0 if kalman_result == "High" else 0.5 if kalman_result == "Medium" else 0.25 if kalman_result == "Low" else 0


# Initialize variables
json_data = []
data = []
chunk_size = 7
file_name= "Testing_files/Results/Testing1.txt"
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

# Convert json_data (list of JSON objects) to DataFrame
df = pd.DataFrame(json_data)
df["mock_loc"] = df["mock_loc"].astype(int)
df["warning_level_encoded"] = df["warning_level"].apply(encode_warning_level)
df["kalman_result_encoded"] = df["kalman_result"].apply(encode_kalman_result)
df["w2"] = (1 - df["w1"]) / 2 - .1 # Kalman
df["w3"] = (1 - df["w1"]) / 2 + .1 # LSTM
df["lstm_prediction"] = df["lstm_prediction"].replace("waiting for more data", 0)

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
