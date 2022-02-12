# -*- coding: utf-8 -*-

import os.path

## Path and filenames for sensor data
iofiles_path = '/home/squirrel/repos/rbp_sensor_data/datafiles'
mhz19b_co2_fname  = 'mhz19b_co2vals.json'
mhz19b_temp_fname = 'mhz19b_tempvals.json'
mhz19b_co2_log  = os.path.join(iofiles_path, mhz19b_co2_fname)
mhz19b_temp_log = os.path.join(iofiles_path, mhz19b_temp_fname)
#sensor_val_fname = 'sensor_vals.json'
#othersensor_val_log = os.path.join(iofiles_path, sensor_val_fname)

## Path and filenames for graphs
graphs_path = '/home/squirrel/repos/rbp_sensor_data/datafiles'
