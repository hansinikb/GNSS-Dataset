# Used to convert .txt to .csv file

import pandas as pd
import os 
import glob

def initialize_df():
    # Define the DataFrame with the specified columns
    df_raw = pd.DataFrame(columns=[
        "utcTimeMillis", "TimeNanos", "LeapSecond", "TimeUncertaintyNanos", 
        "FullBiasNanos", "BiasNanos", "BiasUncertaintyNanos", "DriftNanosPerSecond", 
        "DriftUncertaintyNanosPerSecond", "HardwareClockDiscontinuityCount", "Svid", 
        "TimeOffsetNanos", "State", "ReceivedSvTimeNanos", "ReceivedSvTimeUncertaintyNanos", 
        "Cn0DbHz", "PseudorangeRateMetersPerSecond", 
        "PseudorangeRateUncertaintyMetersPerSecond", "AccumulatedDeltaRangeState", 
        "AccumulatedDeltaRangeMeters", "AccumulatedDeltaRangeUncertaintyMeters", 
        "CarrierFrequencyHz", "CarrierCycles", "CarrierPhase", 
        "CarrierPhaseUncertainty", "MultipathIndicator", "SnrInDb", 
        "ConstellationType", "AgcDb", "BasebandCn0DbHz", 
        "FullInterSignalBiasNanos", "FullInterSignalBiasUncertaintyNanos", 
        "SatelliteInterSignalBiasNanos", "SatelliteInterSignalBiasUncertaintyNanos", 
        "CodeType", "ChipsetElapsedRealtimeNanos","IsFullTracking"
    ])

    df_fix = pd.DataFrame(columns=["Provider", "LatitudeDegrees", "LongitudeDegrees", "AltitudeMeters", "SpeedMps", 
                                "AccuracyMeters", "BearingDegrees", "UnixTimeMillis", "SpeedAccuracyMps", 
                                "BearingAccuracyDegrees", "elapsedRealtimeNanos", "VerticalAccuracyMeters", 
                                "MockLocation", "NumberOfUsedSignals", "VerticalSpeedAccuracyMps", "SolutionType"])

    df_status = pd.DataFrame(columns=["UnixTimeMillis","SignalCount","SignalIndex","ConstellationType","Svid","CarrierFrequencyHz","Cn0DbHz",
                                    "AzimuthDegrees","ElevationDegrees","UsedInFix","HasAlmanacData","HasEphemerisData","BasebandCn0DbHz"])
    return df_raw,df_fix,df_status

def process_data(file,df_raw,df_fix,df_status):
    # Open the file and read line-by-line
    with open(file, 'r') as fopen:
        for line in fopen:
            line = line.strip().strip('"') # Remove any extraneous characters (like trailing quotes)
            log_parts = line.split(',')
            #print(log_parts)
            data = log_parts[1:]
            if line.startswith("Raw"):
                df_raw.loc[len(df_raw)] = data
            elif line.startswith("Fix"):
                df_fix.loc[len(df_fix)] = data
            # elif line.startswith("Status"):
            #     df_status.loc[len(df_status)] = data
    return df_raw,df_fix,df_status

def save_files(file,df_raw,df_fix,df_status):
    output_file = 'Testing_files/Raw/'+file[:-4] + '_Raw' + '.csv'
    df_raw.to_csv(output_file, index=False)

    print(f"Raw data saved to {output_file} with {len(df_raw)} records")

    output_file = 'Testing_files/Fix/'+file[:-4] + '_Fix' + '.csv'
    df_fix.to_csv(output_file, index=False)

    print(f"Fix data saved to {output_file} with {len(df_fix)} records")

    # output_file = 'Status/'+ file[:-4] + '_Status' + '.csv'
    # df_status.to_csv(output_file, index=False)

    # print(f"Status data saved to {output_file} with {len(df_status)} records")

    return len(df_raw),len(df_fix),len(df_status)


# Get the file name from user input
# file = input("Enter the file name: ")

directory = 'Testing_files/Captured_logs'

# Get a list of all files in the directory
files = glob.glob(os.path.join(directory, '*'))
# Iterate through the list and open each file individually
for file_path in files:
    df_raw,df_fix,df_status = initialize_df()
    try:
        df_raw,df_fix,df_status = process_data(file_path,df_raw,df_fix,df_status)
        len_raw,len_fix,len_status = save_files(os.path.basename(file_path),df_raw,df_fix,df_status)
    except Exception as e:
        print(f"{file_path} has error {e}")

