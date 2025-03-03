import pandas as pd
import time
import requests
import json

# csv_files =  ['19_SC_pFix.csv', '31_OR_pFix.csv', '22_TT_pFix.csv', '24_UNKNOWN_pFix.csv', '15_TT_pFix.csv', '4_OR_pFix.csv', '4_EB_pFix.csv','12_EBWL_pFix.csv']

csv_file = r"C:/Capstone/Dataset collection/Testing_files/Processed_Fix/6T_SR_pFix.csv"  
df = pd.read_csv(csv_file)

api_url = "http://localhost:5000/predict_fix"  


for _, row in df.iterrows():
    # Construct the JSON payload
    payload = {
        "Latitude": row["LatitudeDegrees"],
        "Longitude": row["LongitudeDegrees"],
        "Altitude": row["AltitudeMeters"],
        "Bearing": row["BearingDegrees"],
        "SpeedMps": row["SpeedMps"],
        "AccuracyMeters": row["AccuracyMeters"],
        "MockLocation": bool(row["MockLocation"])
    }
    
    try:
        # Send the POST request
        response = requests.post(api_url, json=payload)
        # print(f"Response: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Error occurred: {e}")
    
    # Wait for 1 second before sending the next request
    time.sleep(0.1)
print(f"Successfully sent {len(df)} rows!")
