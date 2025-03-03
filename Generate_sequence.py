#Does not work

import os
import glob
import pandas as pd
import warnings
import numpy as np

fix_files = glob.glob(os.path.join("Processed_Fix", '*'))
all_X, all_y = [], []

features = ['RelativeLatitude', 'RelativeLongitude', 'RelativeAltitude', 'SpeedMps', 'AccuracyMeters', 'RelativeBearing']
target = 'MockLocation'

def split_sequence(sequence, target, n_steps = 5):
    X, y = [], []
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence) - 1:
            break
        seq_x, seq_y = sequence[i:end_ix], target[end_ix]
        X.append(seq_x)
        y.append(seq_y)

    return np.array(X), np.array(y)

for fix_file in fix_files:
    df_fix = pd.read_csv(f"{fix_file}", header=0)
    # Split the sequence
    X, y = split_sequence(df_fix[features].values, df_fix[target].values)
    all_X.append(X)
    all_y.append(y)

final_X = np.concatenate(all_X, axis=0)
final_y = np.concatenate(all_y, axis=0)

# Save final merged X and y
np.save("merged_X.npy", final_X)
np.save("merged_y.npy", final_y)