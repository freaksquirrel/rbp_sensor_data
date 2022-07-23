# -*- coding: utf-8 -*-

import argparse
import sys
import os.path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import datetime as dt
import json
import amedas_config as a_cfg
import amedas_funcs as a_fnc



if __name__ == '__main__':
    parser = argparse.ArgumentParser( description="Get weather data from AMEADAS api...",  )
    parser.add_argument("-a", "--area", type = int, default = 0, help="Specific area to request weather data")
    parser.add_argument("--date",  help="YYYY-MM-DD format date")
    parser.add_argument("--time",  help="HH time format")
    parser.add_argument("--datetime",  help="YYYY-MM-DD-HH-MM format")
    parser.add_argument("-p", action='store_true', help="Print out values on terminal")
    parser.add_argument("--batch", action='store_true', help="Get each 10 min weather values for last hour")
    args = parser.parse_args()

    # set the date for the weather data query
    if args.date:
        try:
            entry_date = dt.datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            entry_date = dt.datetime.now()
    else:
        entry_date = dt.datetime.now()

    # set the time for the weather data query
    if args.time:
        try:
            entry_time = dt.datetime.strptime(args.time, '%H:%M')
        except ValueError:
            entry_time = dt.datetime.now()
    else:
        entry_time = dt.datetime.now()

    # set the region for the weather data query
    if args.area != 0 :
        area_code = args.area
    else:
        area_code = a_cfg.area_code

    if args.p:
        weather_data = a_fnc.request_weather_data()
        #check if datapoint is valid
        if( weather_data ):
            print('What data -> {}'. format(weather_data))
        else:
            print('error... did not receive the kind of results I was expecting')
            
    elif args.batch:
        target_datetime = dt.datetime.now() - dt.timedelta(hours = 1)
        for minute in range(6):
            query_datetime = dt.datetime.strptime(target_datetime.strftime('%Y%m%d%H'+str(minute)+'0'), '%Y%m%d%H%M')
            print('Time {} and code {}'. format(query_datetime, a_cfg.area_code))
            res = a_fnc.requestAndStoreWeatherInfo( query_datetime, a_cfg.area_code )
            
    else:
        weather_data = a_fnc.request_weather_data()
        if( weather_data ):
            # Storage with debug mode... will call it on a cron-job and keep a log
            res = a_fnc.addWeatherValEntry( weather_data, True, area_code, entry_date, entry_time )
            print('Got data for the area {} at @ ({} {}) = {}'.format(area_code, entry_date, entry_time, res))
        else:
            print('Error! not able to get data for the area {} at @ ({} {}) = {}'.format(area_code, entry_date, entry_time, res))
        
    sys.exit(0)
