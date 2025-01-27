# encoding: utf8   
## Description
# Name: read_km2.py
#
# Author: Rasmus Nielsen, 2013
#

## Updates:
# * (15-03-2022) Fixed no_of_lines to be a integer
# * (15-03-2022) File handle is now opening as "r" instead of "rb"

# Author: Rasmus Nielsen, 2013


import re, pandas as pd
from datetime import timedelta, datetime

def read_kmd2(file_name, save_to_csv):
    """
    Reads a kmd2 file and returns the time series. If save_to_csv is true
    then the time series is stored on the disk.

    return: dictionary with rain_series[start_date] = (minutes of rain,
                                                       time stamps, data)
    """

    # Load kmd2 file
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # List of data frames with the time series
    df_list = []

    # Go through each line and read the appropiate lines of data
    for i, line in enumerate(lines):
        # Check if header is detected
        if re.findall('\d\s\d+\s+\d+\s+\d+\s+\s+\s+\d+\s+\d+\s+\d+\.\d+\s+\d+', line):
            # Set temporary result dictionary
            rain_series = {}

            # Extract the number of minutes of data
            match = re.search('\d\s\d+\s+\d+\s+\d+\s+(\d+)', line)
            no_of_data = int(match.group(1))
            
            # Extract the start data
            match = re.search('\d\s(\d+\s+\d+)', line)
            start_date = datetime.strptime(match.group(1), '%Y%m%d %H%M')
            
            # Store the lines of data
            # Determine how many lines the data spans
            # Each line contains 10 data points in a minutely resolution
            if no_of_data <= 10: # Only 1 line long
                no_of_lines = 1
            # If the span is greater than 10 minutes
            # subtract the remainder from the number 
            # of lines
            else: 
                remainder = no_of_data % 10
                if remainder > 0:
                    no_of_lines = (no_of_data - remainder) / 10 + 1
                else:
                    no_of_lines = no_of_data / 10

            data_raw = lines[i + 1 : i + 1 + int(no_of_lines)]

            # Extract the data to a list
            data = []
            for data_line in data_raw:
                entries = re.findall('\d+\.\d+', data_line) # Find all data entries
                for entry in entries: 
                    data.append(float(entry))
            
            # Add time stamp for each data entry
            time_stamps = [start_date + timedelta(minutes=x) for x in range(0, no_of_data)]

            # Update dictionary
            rain_series[start_date] = (no_of_data, time_stamps, data)

            # Store in data frame list
            df_list.append(pd.DataFrame(data = data, index = time_stamps, columns = 
                                        [file_name.split('.')[0]]))

    # Concatenate the data frames into one
    df = pd.concat(df_list)
    df.index.name = 'index'
    # Write time series to disk
    if save_to_csv: df.to_csv(file_name.split('.')[0] + '.csv')
    return df

read_kmd2("Example data.km2", True)