# Read KMD2-formatted files from the Danish SVK-raingauges

## Description

Reads the KMD2 input file and saves it to a CSV-file. Function can be included
into existing scripts or used separately.

### Input

* file_name:   Name of the input file.
* save_to_csv: Boolean, if "True", a csv file will be written to disk.

### User guide
Type the following command into the terminal:

python3 water_level.py <station_number> <start_date> <end_date>
Date format: dd-mm-yyyy

Example:        
python3 water_level.py 20253 01-01-2018 01-01-2019
