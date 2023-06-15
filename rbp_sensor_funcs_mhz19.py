# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import datetime as dt
import subprocess
import argparse
import sys
import json
import os.path
import mh_z19
import rbp_sensor_iofiles as rbps_io
import rbp_sensor_plot_data as rbps_pltdata


def addCO2valEntry( datapoint, debugprint = False ):
    #check if datapoint is a dict type
    if( type(datapoint) is not dict ): return False
    #Get data from file
    try:
        if( os.path.exists(rbps_io.mhz19b_co2_log) ):
            #Open file in read only mode only
            tempfile = open(rbps_io.mhz19b_co2_log, 'r')
            tempdata = json.load(tempfile)
            tempfile.close()
            if( debugprint == True) : print('Reading data from file {} \n'.format(rbps_io.mhz19b_co2_log))
        else:
            tempdata = {}
            if( debugprint == True) : print('New file will be created at {} \n'.format(rbps_io.mhz19b_co2_log))
    except ValueError:
        if( debugprint == True) : print('File {} was empty \n creating new entry...\n'.format(rbps_io.mhz19b_co2_log))
        print('Empty temp file')
        tempdata = {}
    except IOError:
        print('Unexpected error: {}'.format(sys.exc_info()[0:2]))                
    
    #Get current date to create a JSON key for searching
    key = dt.date.today().strftime('%Y-%m-%d')
    #search the date key in the current data
    if( key in tempdata ):
        #if available, add datapoint
        tempdata[key][0].update(datapoint)
        # consider checking if value for that time is already in the list or not
        if( debugprint == True) : print('Added the datapoint {} to the key {} \n'.format(datapoint, key))
    else:
        #if not available, add new date key and add datapoint
        tempdata.update({key:[datapoint]})
        # consider checking if value for that time is already in the list or not
        if( debugprint == True) : print('Created the key {} and added the datapoint {} \n'.format(key, datapoint))
    #finally, re-write json file
    tempfile = open(rbps_io.mhz19b_co2_log,'w')
    json.dump(tempdata, tempfile, sort_keys=True)
    if( debugprint == True) : print('Re-wrote data to file {} \n'.format(rbps_io.mhz19b_co2_log))
    tempfile.close()
    return True


def getCO2val():
    # get the time first
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    # then read the CO2 values
    tempdata = {}
    co2_val = mh_z19.read()
    if( co2_val ):     # check if the value returned is valid
        # temp output format
        tempdata = {current_time : int(co2_val['co2'])}
        ## Storage with debug mode on since I intend to call it on a cron-job and want to keep a log
        #result = addCO2valEntry( tempdata, True )
        #return result
    return tempdata


# this function is not tested yet...
def getCO2andTempvals():
    # get the time first
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    # then read the CO2 values
    co2_val = mh_z19.read_all()
    # temp output format
    tempdata = {current_time : int(co2_val['co2'])}
    # Storage with debug mode on since I intend to call it on a cron-job and want to keep a log
    # result = addCO2valEntry( tempdata, True )
    tempdata = {current_time : int(co2_val['temperature'])}
    #Store it somewhere
    return result


# this function is not tested yet... used to work before on a different script though...
def getTempRaspBP( debugprint = False ):
    #Get temperature of raspberry pi (temp only)
    temperature = (subprocess.check_output(["vcgencmd", "measure_temp"])).split("=")[1].strip('\n').split("'")[0]
    #Get current time
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    tempdata = {current_time : float(temperature)}
    if( debugprint == True) : print('Got the temperature value {} C (at {}) \n'.format(tempdata[current_time], current_time))
    return tempdata


