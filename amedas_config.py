# -*- coding: utf-8 -*-
import os.path

## URL and request format related definitions
url_format = "https://www.jma.go.jp/bosai/amedas/data/map/YYYYMMDDHHMM00.json"  # Format of the URL time  -> YYYYMMDDHHMMSS
replace_target = "YYYYMMDDHHMM"
area_code = '40201'    #I use "Mito-shi" as default (Note about area codes: you can find the area code you want in the full JSON response ;) )

## Path and filenames for amedas weather data
iofiles_path = '/home/squirrel/repos/rbp_sensor_data/datafiles'
amedas_fname  = 'amedas_vals.json'
amedas_log  = os.path.join(iofiles_path, amedas_fname)

## Path and filenames for graphs
graphs_path = '/var/www/html/freaksquirrel/plots/amedas/'

#"40201":{
#    "temp":[22.8,0],
#    "humidity":[93,0],
#    "snow":[null,5],
#    "weather":[7,0],
#    "sun10m":[0,0],
#    "sun1h":[0.0,0],
#    "precipitation10m":[0.0,0],
#    "precipitation1h":[0.5,0],
#    "precipitation3h":[2.0,0],
#    "precipitation24h":[7.0,0],
#    "windDirection":[2,0],
#    "wind":[4.2,0]},"

# res_  = {'normalPressure': [1000.4, 0], 'snow6h': [0, 6], 'wind': [1.3, 0], 'snow1h': [0, 6], 'snow': [None, 5], 'snow12h': [0, 6], 'sun1h': [0.0, 0], 'precipitation1h': [0.0, 0], 'precipitation3h': [0.0, 0], 'precipitation24h': [0.0, 0], 'weather': [1, 0], 'temp': [24.3, 0], 'precipitation10m': [0.0, 0], 'sun10m': [0, 0], 'windDirection': [3, 0], 'pressure': [996.9, 0], 'snow24h': [0, 6], 'humidity': [82, 0], 'visibility': [16790.0, 0]}
