# GNSS-Dataset

# GNSS Spoofing Detection Dataset

## Description
This repository contains a dataset of GNSS logs (Fix and Raw) collected using GNSS Logger and LocaEdit. The dataset is designed for research on GNSS spoofing detection and includes both original and spoofed location data. The logs are preprocessed and ready for use in developing and evaluating machine learning models or signal processing techniques.

## Dataset Details

### Data Collection
#### Tools Used:
- **GNSS Logger**: Records real-time location and sensor data.
- **LocaEdit**: Simulates spoofed location scenarios (static locations, navigation between points, multi-path routing, and speed modification).

#### Devices:
- Galaxy M34 5G
- Oppo Reno7
- Galaxy S23 Ultra

#### Log Types:
- **Fix Logs**: 13,828 rows containing location-based information (latitude, longitude, altitude, speed, bearing, accuracy).
- **Raw Logs**: 298,363 rows containing signal parameters (satellite identifiers, Doppler shift, carrier frequency, signal strength).

### Preprocessing
#### Fix Dataset:
- Selected 7 key features: `latitude`, `longitude`, `altitude`, `speed`, `bearing`, `accuracy`, and a `mock location` indicator.
- Calculated relative latitude, longitude, altitude, and bearing by taking differences between consecutive rows.
- Replaced null values using linear interpolation.
- Normalized speed and accuracy using Min-Max scaling.

#### Raw Dataset:
- Selected 11 key features: `time`, `satellite ID`, `state`, `signal strength (Cn0DbHz, SnrInDb)`, `pseudorange`, `carrier frequency`, and more.
- Approximated spoofing labels (`MockLocationAppx`) by aligning Fix and Raw logs using timestamps.
- Replaced null values using linear interpolation.
- Encoded categorical features (e.g., satellite state) using Ordinal Encoding.
- Scaled numerical features using Standard Scaler.

## Dataset Structure
The dataset is organized into two main folders:
- **Fix Logs**: Contains preprocessed Fix data in `.csv` format.
- **Raw Logs**: Contains preprocessed Raw data in `.csv` format.

Each file is labeled to indicate whether it represents original or spoofed data. Metadata (e.g., device used, spoofing scenario) is included for reference.

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GNSS-Dataset.git
   ```
2. Load the dataset in Python:
   ```python
   import pandas as pd
   fix_data = pd.read_csv('Fix Logs/fix_data.csv')
   raw_data = pd.read_csv('Raw Logs/raw_data.csv')
   ```
3. Analyze or preprocess further as needed for your research.


## Contact
For questions or collaborations, please contact [Hansini KB] at [hansinikb@gmail.com].
