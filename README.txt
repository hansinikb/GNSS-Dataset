OR - Original
TT - Turn by turn Attack
EB - Erratic Behaviour
UT - U turn
SR - Signal Replay
JU - Jumps
SI - Signal Interrupt
SC - Speed Change

Steps for preprocessing
1. Run Script.py to convert .txt to .csv files
2. Run Correction.py to make sure Mocklocation is not NULL
3. Run Basic_processing.py for preprocessing steps

* Merge_data.py is a script to merge all files in Processed_Raw and Processed_Fix folders.

20_SL: 
No spoofing. Simply turned of GPS signals.

21_SL:
Gps stopped. Started
Stopped and then spoofed to the opposite direction. 