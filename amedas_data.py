# -*- coding: utf-8 -*-

import argparse
import sys
import os.path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import datetime as dt
import json
import amedas_config as a_cfg

#url_format = "https://www.jma.go.jp/bosai/amedas/data/map/YYYYMMDDHH0000.json"
#req_url = "https://www.jma.go.jp/bosai/amedas/data/map/20220715160000.json"

def create_req_url_from_datetime( target_datetime = "" ):
    if( not isinstance(target_datetime, dt.datetime) ): target_datetime = dt.datetime.now()
    #datetime_str = target_datetime.strftime('%Y%m%d%H')
    datetime_str = target_datetime.strftime('%Y%m%d%H00')
    amedas_req_url = a_cfg.url_format.replace(a_cfg.replace_target, datetime_str)
    return amedas_req_url

#Note: seems like past data is only available for the 10 days previous to current data 
def create_req_url_from_str( target_datetime = "" ):
    #if( target_datetime == ""): target_datetime = dt.datetime.now().strftime('%Y%m%d%H')
    if( target_datetime == ""): target_datetime = dt.datetime.now().strftime('%Y%m%d%H00')
    amedas_req_url = a_cfg.url_format.replace(a_cfg.replace_target, target_datetime)
    return amedas_req_url

def request_weather_data( target_datetime = "", area_code = 0, req_url = "" ):
    if( req_url == ""):
        if( isinstance(target_datetime, dt.datetime) ):
            req_url = create_req_url_from_datetime(target_datetime)
        else:
             req_url = create_req_url_from_str(target_datetime)   
    
    try:
        weather_response = urlopen(req_url)
    except HTTPError as e:
        print('HTTP ERROR... code: ', e.code)
        area_weather_info = "ERROR"
    except URLError as e:
        print('URL ERROR... reason: ', e.reason)
        area_weather_info = "ERROR"
    else:
        raw_data = json.loads(weather_response.read().decode("utf-8"))
        if( area_code == 0 ): area_code = a_cfg.area_code
        if( area_code in raw_data ):
            area_weather_info = raw_data[area_code]
        else:
            area_weather_info = "NAN"
            
    return area_weather_info


def addWeatherValEntry( datapoint, debugprint = False, area_code = 0, entry_date = "", entry_time = "" ):
    #check if datapoint is a dict type
    if( type(datapoint) is not dict ): return False
    #Get data from file
    try:
        if( os.path.exists(a_cfg.amedas_log) ):
            #Open file in read only mode only
            tempfile = open(a_cfg.amedas_log, 'r')
            tempdata = json.load(tempfile)
            tempfile.close()
            if( debugprint == True) : print('Reading data from file {} \n'.format(a_cfg.amedas_log))
        else:
            tempdata = {}
            if( debugprint == True) : print('New file will be created at {} \n'.format(a_cfg.amedas_log))
    except ValueError:
        if( debugprint == True) : print('File {} was empty \n creating new entry...\n'.format(a_cfg.amedas_log))
        print('Empty temp file')
        tempdata = {}
    except IOError:
        print('Unexpected error: {}'.format(sys.exc_info()[0:2]))


    if( isinstance(entry_time, dt.datetime) and isinstance(entry_date, dt.datetime)):
        #Get the entry datetime to create a JSON key for searching
        entry_time_key = entry_time.strftime('%Y-%m-%d %H:00')
        #Get the entry date to create a JSON key for searching
        entry_date_key = entry_date.strftime('%Y-%m-%d')
        #search the date key in the current data

        if( area_code == 0 ): area_code = a_cfg.area_code

        #datapoint_tmp = {entry_time_key : {"40201":datapoint}}
        datapoint_tmp = {entry_time_key : {str(area_code):datapoint}}
        
        if( entry_date_key in tempdata ):
            #if( entry_time_key in tempdata[entry_date_key] ):
            tempdata[entry_date_key].update(datapoint_tmp)
            # consider checking if value for that time is already in the list or not
            if( debugprint == True) :print('Added the datapoint {} to the key {} \n'.format(datapoint_tmp, entry_date_key))
        else:
            #if not available, add new date key and add datapoint
            tempdata.update({entry_date_key:datapoint_tmp})
            # consider checking if value for that time is already in the list or not
            if( debugprint == True) : print('Created the key {} and added the datapoint {} \n'.format(entry_date_key, datapoint_tmp))
        #finally, re-write json file
        tempfile = open(a_cfg.amedas_log,'w')
        json.dump(tempdata, tempfile, sort_keys=True)
        if( debugprint == True) : print('Re-wrote data to file {} \n'.format(a_cfg.amedas_log))
        tempfile.close()
        return True
    else:
        print("error")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description="Get weather data from AMEADAS api...",  )
    parser.add_argument("-a", "--area", type = int, default = 0, help="Specific area to request weather data")
    parser.add_argument("--date",  help="YYYY-MM-DD format date")
    parser.add_argument("--time",  help="HH time format")
    parser.add_argument("-p", action='store_true', help="Print out values on terminal")
    args = parser.parse_args()

    if args.date:
        try:
            entry_date = dt.datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            entry_date = dt.datetime.now()
    else:
        entry_date = dt.datetime.now()

    if args.time:
        try:
            entry_time = dt.datetime.strptime(args.time, '%H:%M')
        except ValueError:
            entry_time = dt.datetime.now()
    else:
        entry_time = dt.datetime.now()
    
    if args.area != 0 :
        area_code = args.area
    else:
        area_code = a_cfg.area_code

    if args.p:
        weather_data = request_weather_data()
        #check if datapoint is valid
        if( weather_data ):
            print('What data -> {}'. format(weather_data))
        else:
            print('error... did not receive the kind of results I was expecting')
    else:
        weather_data = request_weather_data()
        if( weather_data ):
            # Storage with debug mode... will call it on a cron-job and keep a log
            res = addWeatherValEntry( weather_data, True, area_code, entry_date, entry_time )
            print('Got data for the area {} at @ ({} {}) = {}'.format(area_code, entry_date, entry_time, res))
        else:
            print('Error! not able to get data for the area {} at @ ({} {}) = {}'.format(area_code, entry_date, entry_time, res))
        
    sys.exit(0)
    


# res_  = {'normalPressure': [1000.4, 0], 'snow6h': [0, 6], 'wind': [1.3, 0], 'snow1h': [0, 6], 'snow': [None, 5], 'snow12h': [0, 6], 'sun1h': [0.0, 0], 'precipitation1h': [0.0, 0], 'precipitation3h': [0.0, 0], 'precipitation24h': [0.0, 0], 'weather': [1, 0], 'temp': [24.3, 0], 'precipitation10m': [0.0, 0], 'sun10m': [0, 0], 'windDirection': [3, 0], 'pressure': [996.9, 0], 'snow24h': [0, 6], 'humidity': [82, 0], 'visibility': [16790.0, 0]}

# test = {current_time : [ {"41201":[res_]}]}

# test = {current_time : {"41201":res_}}


    

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
