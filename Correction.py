# This file is for correcting Hansini's phone MockLocation
import os
import glob
import pandas as pd
import numpy as np

dirs = ["Testing_files/Fix"]

for dir_name in dirs:
    files = glob.glob(os.path.join(dir_name, '*'))
    total_length = 0
    for file_path in files:
        if 'OR' in file_path:
            data = pd.read_csv(file_path, header=0)
            #data.drop(data.columns[[0,1]], axis=1, inplace=True)
            data['MockLocation'].fillna(0,inplace = True)
            data.to_csv(file_path,index = False)
        else:
            data = pd.read_csv(file_path,header = 0)

            # Update MockLocation column: Set to 1 where both columns are null, else 0
            data['MockLocation'] = np.where(data['MockLocation'].isnull() & data['SpeedAccuracyMps'].isnull(), 1, data['MockLocation'])
            data.to_csv(file_path,index = False)