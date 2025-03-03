# This file has the following functions
# 1. Generate Approx labels for raw data
# 2. Handle null values by filling 0
# 3. Calculate the relative latitude, longitude, altitude

import os
import glob
import pandas as pd
import warnings

os.chdir("Testing_files")

# Suppress all warnings
warnings.filterwarnings("ignore")

def generate_approx_labels(df_raw,df_fix):
    df_raw['MockLocation_approx'] = None  

    raw_index = 0
    fix_index = 0

    while raw_index < len(df_raw) and fix_index < len(df_fix):
        if df_fix['UnixTimeMillis'][fix_index]>df_raw['utcTimeMillis'][raw_index]:
            df_raw['MockLocation_approx'][raw_index] = df_fix['MockLocation'][fix_index]
            raw_index += 1
        else:
            fix_index += 1
    return df_raw

def handle_null_values_fix(df):

    # Convert UnixTime from milliseconds to datetime
    df['DateTime'] = pd.to_datetime(df['UnixTimeMillis'], unit='ms')

    df.drop('elapsedRealtimeNanos', axis=1, inplace=True)

    # Fill missing values with zeros for columns with a few nulls
    columns_with_nulls = ['LatitudeDegrees', 'LongitudeDegrees', 'AltitudeMeters',
       'SpeedMps', 'AccuracyMeters', 'BearingDegrees', 
       'SpeedAccuracyMps', 'BearingAccuracyDegrees']
    df[columns_with_nulls] = df[columns_with_nulls].apply(lambda x: x.interpolate(method='linear', limit_direction='both'))

    # Calculate relative changes using diff() for efficiency
    df['RelativeLatitude'] = df['LatitudeDegrees'].diff().fillna(0)
    df['RelativeLongitude'] = df['LongitudeDegrees'].diff().fillna(0)
    df['RelativeBearing'] = df['BearingDegrees'].diff().fillna(0)
    df['RelativeAltitude'] = df['AltitudeMeters'].diff().fillna(0)

    return df

def handle_raw(df):
    c = 299792458  # Speed of light in m/s
    df["Pseudorange"] = c * 1e-9 * (df["TimeNanos"] + df["FullBiasNanos"] + df["BiasNanos"] - df["ReceivedSvTimeNanos"])
    columns = [
    'utcTimeMillis','Svid', 'Cn0DbHz', 'PseudorangeRateMetersPerSecond',
    'AccumulatedDeltaRangeUncertaintyMeters', 'AccumulatedDeltaRangeState',
    'CarrierFrequencyHz', 'SnrInDb', 'BasebandCn0DbHz', 'CodeType','State',
    'DriftNanosPerSecond','HardwareClockDiscontinuityCount',"Pseudorange"
    ]
    df = df[columns]

    df[columns] = df[columns].apply(lambda x: x.interpolate(method='linear', limit_direction='both'))
    return df

def drop_cols(df_raw,df_fix):
    raw_features = ['utcTimeMillis','Svid', 'Cn0DbHz', 'PseudorangeRateMetersPerSecond',
    'AccumulatedDeltaRangeUncertaintyMeters', 'AccumulatedDeltaRangeState',
    'CarrierFrequencyHz', 'SnrInDb', 'BasebandCn0DbHz', 'CodeType','State',
    'DriftNanosPerSecond','HardwareClockDiscontinuityCount',"Pseudorange",'MockLocation_approx']
    
    fix_features = ['LatitudeDegrees', 'LongitudeDegrees', 'AltitudeMeters', 'SpeedMps',
       'AccuracyMeters', 'BearingDegrees', 'UnixTimeMillis', 'MockLocation', 
       'RelativeLatitude','RelativeLongitude','RelativeAltitude','RelativeBearing']
    
    df_raw = df_raw[raw_features]
    df_fix = df_fix[fix_features]
    return df_raw,df_fix

def save_files(file,df_raw,df_fix):
    output_file = 'Processed_Raw/'+file + '_pRaw' + '.csv'
    df_raw.to_csv(output_file, index=False)

    print(f"Raw data saved to {output_file}")

    output_file = 'Processed_Fix/'+file + '_pFix' + '.csv'
    df_fix.to_csv(output_file, index=False)

    print(f"Fix data saved to {output_file}")


raw_files = glob.glob(os.path.join("Raw", '*'))
fix_files = glob.glob(os.path.join("Fix", '*'))


file_pairs = {}

for fix_file in fix_files:
    # Extract the base name and construct the expected raw file path
    fix_file_name = os.path.basename(fix_file)
    base_name = fix_file_name[:-8]
    raw_file_name = f"{base_name}_Raw.csv"
    file_pairs[base_name] = (fix_file_name, raw_file_name)
#print(file_pairs)

# Now iterate over the file pairs and read the data into DataFrames
for base_name, (fix_file, raw_file) in file_pairs.items():
    print(f"Processing files for {base_name}")
    
    # Read the corresponding CSV files into DataFrames
    df_fix = pd.read_csv(f"Fix/{fix_file}", header=0)
    df_raw = pd.read_csv(f"Raw/{raw_file}", header=0)

    df_fix = handle_null_values_fix(df_fix)
    df_raw = handle_raw(df_raw)
    
    df_raw = generate_approx_labels(df_raw,df_fix)
    df_raw,df_fix = drop_cols(df_raw,df_fix)
    save_files(base_name,df_raw,df_fix)

print("Done!")

