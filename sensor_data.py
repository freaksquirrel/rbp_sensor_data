# -*- coding: utf-8 -*-

import time
import subprocess
import argparse
import sys
import json
import os.path
import mh_z19

TEMPFILE = '<change this path>.dat'

def addCO2valEntry( datapoint, debugprint = False ):
    #check if datapoint is a dict type
    if( type(datapoint) is not dict ): return False
    #Get data from file
    try:
        if( os.path.exists(TEMPFILE) ):
            #Open file in read only mode only
            tempfile = open(TEMPFILE,'r')
            tempdata = json.load(tempfile)
            tempfile.close()
            if( debugprint == True) : print('Reading data from file {} \n'.format(TEMPFILE))
        else:
            #open in write put a flag
            #tempfile = open(TEMPFILE,'w')
            #tempfile.close()
            tempdata = {}
            if( debugprint == True) : print('New file will be created at {} \n'.format(TEMPFILE))
    except ValueError:
        if( debugprint == True) : print('File {} was empty \n creating new entry...\n'.format(TEMPFILE))
        print('Empty temp file')
        tempdata = {}
    except IOError:
        print('Unexpected error: {}'.format(sys.exc_info()[0:2]))                
    
    #Get current date to create a JSON key for searching
    key = time.strftime("%Y-%m-%d", time.localtime())
    #search the date key in the current data
    if( key in tempdata ):
        #if available, add datapoint
        #tempdata[key].append(datapoint)
        tempdata[key][0].update(datapoint)
        # consider checking if value for that time is already in the list or not
        if( debugprint == True) : print('Added the datapoint {} to the key {} \n'.format(datapoint, key))
    else:
        #if not available, add new date key and add datapoint
        tempdata.update({key:[datapoint]})
        # consider checking if value for that time is already in the list or not
        if( debugprint == True) : print('Created the key {} and added the datapoint {} \n'.format(key, datapoint))
    #finally, re-write json file
    tempfile = open(TEMPFILE,'w')
    json.dump(tempdata, tempfile, sort_keys=True)
    if( debugprint == True) : print('Re-wrote data to file {} \n'.format(TEMPFILE))
    tempfile.close()
    return True


def getCO2val():
    # get the time first
    current_time = time.strftime("%H:%M", time.localtime())
    # then read the CO2 values
    co2_val = mh_z19.read()
    # temp output format
    tempdata = {current_time : int(co2_val['co2'])}
    result = addCO2valEntry( tempdata)
    return result


def getTempRaspBP( debugprint = False ):
    #Get temperature of raspberry pi (temp only)
    temperature = (subprocess.check_output(["vcgencmd", "measure_temp"])).split("=")[1].strip('\n').split("'")[0]
    #Get current time
    current_time = time.strftime("%H:%M", time.localtime())
    tempdata = {current_time : float(temperature)}
    if( debugprint == True) : print('Got the temperature value {} C (at {}) \n'.format(tempdata[current_time], current_time))
    return tempdata
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description="Get values from sensors...",  )
    parser.add_argument("--co2", action="store_true", help="Get CO2 values from MH-Z19B sensor")
    parser.add_argument("--mz_z19_all", action='store_true', help="Get CO2 and temperature values from MH-Z19B sensor")
    
    args = parser.parse_args()
    
    if args.co2:
        res = getCO2val()
        print('Got CO2 values and the store results was: {}'.format(res))
    elif args.mz_z19_all:
        # nothing yet
        print("CO2 and temperature values")
    else:
        print("Please select an option... I dont have a default behavior yet...")
        
    sys.exit(0)
