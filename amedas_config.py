# -*- coding: utf-8 -*-
import os.path

## URL and request format related definitions
url_format = "https://www.jma.go.jp/bosai/amedas/data/map/YYYYMMDDHH0000.json"
replace_target = "YYYYMMDDHH"
area_code = '40201'    #Mito-shi (Note about area codes: you can find the area code you want in the full JSON response ;) )

## Path and filenames for amedas weather data
iofiles_path = '/home/squirrel/repos/rbp_sensor_data/datafiles'
amedas_fname  = 'amedas_vals.json'
amedas_log  = os.path.join(iofiles_path, amedas_fname)


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
