# GNSS-Dataset
Dataset Overview
This dataset consists of GNSS logs collected using two apps: GNSS Logger and LocaEdit. GNSS Logger records real-time location and sensor data, while LocaEdit is used to simulate spoofed location scenarios. The dataset includes both Fix logs (latitude, longitude, altitude) and Raw logs (signal parameters, satellite identifiers, Doppler shift, carrier phase frequency). Data was collected using smartphones such as the Galaxy M34 5G, Oppo Reno7, and Galaxy S23 Ultra.

Data Collection Process
To collect the data, at least two smartphones were used. The first phone recorded GNSS logs of the original route without spoofing, while the second phone simulated spoofing scenarios using LocaEdit. GNSS Logger ran in the background to capture logs during both original and spoofed routes. LocaEdit offers various spoofing options, including static locations, navigation between source and destination, and multi-path routing with adjustable speeds.

Dataset Structure
The dataset is organized into two main types of logs:

Fix Logs: Contain location-based information such as latitude, longitude, and altitude.

Raw Logs: Include detailed signal parameters like satellite identifiers, Doppler shift, and carrier phase frequency.

Each log file is labeled to indicate whether it represents original or spoofed data. Additional metadata, such as the device used and spoofing scenario, is also provided.

Usage
This dataset is intended for research on GNSS spoofing detection, particularly for developing and evaluating machine learning models or signal processing techniques. The combination of original and spoofed logs allows for the creation of robust detection systems. For more details on the data collection process and tools used, refer to the documentation in the repository.
