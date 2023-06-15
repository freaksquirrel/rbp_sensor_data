# -*- coding: utf-8 -*-

import os.path

## Path and filenames for sensor data
iofiles_path = '<path to your data files>'

## CO2 sensor (MHZ19B)
mhz19b_co2_fname  = 'mhz19b_co2vals.json'
mhz19b_temp_fname = 'mhz19b_tempvals.json'
mhz19b_co2_log  = os.path.join(iofiles_path, mhz19b_co2_fname)
mhz19b_temp_log = os.path.join(iofiles_path, mhz19b_temp_fname)

## Temperature and humidity sensor (SwitchBot)
switchbot_temphumi_fname  = 'switchbot_temphumivals.json'
switchbot_temphumi_log  = os.path.join(iofiles_path, switchbot_temphumi_fname)

#sensor_val_fname = 'sensor_vals.json'
#othersensor_val_log = os.path.join(iofiles_path, sensor_val_fname)

## Path and filenames for graphs
graphs_path = '<path to you grpah files'
graphs_folder_mhz19b_co2 = 'mhz19b_CO2_graphs'
graphs_folder_switchbot_temphumi = 'switchbot_temphumi_graphs'
graphs_path_mhz19b_co2 = os.path.join(graphs_path, graphs_folder_mhz19b_co2)
graphs_path_switchbot_temphumi = os.path.join(graphs_path, graphs_folder_switchbot_temphumi)
