# Merge the processed fix and raw data

import os
import glob
import pandas as pd
import warnings

raw_files = glob.glob(os.path.join("Processed_Raw", '*'))
# fix_files = glob.glob(os.path.join("Processed_Fix", '*'))

# fix_dfs = []
raw_dfs = []

# for fix_file in fix_files:
#     df_fix = pd.read_csv(f"{fix_file}", header=0)

#     #Extract name till second underscore and attach it as a new column
#     df_fix['BaseName'] = os.path.basename(fix_file)[:4]
    
#     fix_dfs.append(df_fix)


for raw_file in raw_files:

    df_raw = pd.read_csv(f"{raw_file}", header=0)

    #Extract name till second underscore and attach it as a new column
    df_raw['BaseName'] = os.path.basename(raw_file)[:4]
    
    raw_dfs.append(df_raw)


# # Concatenate all Fix DataFrames into one large DataFrame
# df_fix_merged = pd.concat(fix_dfs, ignore_index=True)

# Concatenate all Raw DataFrames into one large DataFrame
df_raw_merged = pd.concat(raw_dfs, ignore_index=True)

print("Merging done! Saving now...")

# df_fix_merged.to_csv("merged_fix.csv", index=False)
df_raw_merged.to_csv("merged_raw.csv", index=False)

print("Saved!")