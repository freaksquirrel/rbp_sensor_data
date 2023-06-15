# -*- coding: utf-8 -*-

import binascii
from bluepy.btle import Scanner, DefaultDelegate
import datetime as dt
import json
import os.path
import switchbot_config as swb_cfg
import rbp_sensor_iofiles as rbps_io


class ScanDelegate(DefaultDelegate):
    #Data goes here for a bit
    scanned_data = []
    
    def __init__(self):
        DefaultDelegate.__init__(self)
    
    def handleDiscovery(self, dev, isNewDev, isNewData):
        disc_time = dt.datetime.now()#.strftime('%H:%M')
        # get the mac addrs of the devices to look for...
        mac_addrs = [sub['macaddr'] for sub in swb_cfg.BTsensors]
        # finish the process if the discovered device is not in the list
        if dev.addr not in mac_addrs : return
        
        for (adtype, desc, value) in dev.getScanData():
            if (adtype != 22): continue
            servicedata = binascii.unhexlify(value[4:])
            battery = (servicedata[2] & 0b01111111)
            temperature = (servicedata[3] & 0b00001111) / 10 + (servicedata[4] & 0b01111111)
            isTemperatureAboveFreezing = (servicedata[4] & 0b10000000)
            if not isTemperatureAboveFreezing:
                temperature = -temperature
            humidity = (servicedata[5] & 0b01111111)
            #
            #print("current address: {}".format(dev.addr))
            # Add the acquired data to a dictionary to be added to a final list
            sensor_info = next((sens_info for sens_info in swb_cfg.BTsensors if sens_info["macaddr"] == dev.addr), None)
            sensor_info['battery'] = battery
            sensor_info['temperature'] = temperature
            sensor_info['humidity'] = humidity
            sensor_info['time'] = disc_time.strftime('%H:%M')
            sensor_info['date'] = disc_time.strftime('%Y-%m-%d')
            # Append the acquired data to the list
            self.scanned_data.append(sensor_info)
            #print('\t'.join(['switchbot.meter.battery', str(battery), str(disc_time) ]))
            #print('\t'.join(['switchbot.meter.temperature', str(temperature), str(disc_time) ]))
            #print('\t'.join(['switchbot.meter.humidity', str(humidity), str(disc_time) ]))
            break
        return


def getTempAndHumidity_SwitchBot( debugprint = False ):
    #create a bluetooth scanner instance
    scanner = Scanner().withDelegate( ScanDelegate() )
    # then get the date/time
    current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    if( debugprint == True) : print( 'Start scanning @ {} \n'.format(current_time) )
    # reset the data (just to be sure )... i mean, I can set this somewhere else in a more efficient way...
    scanner.delegate.scanned_data = []
    # Then start scanning (try ti find the SB sensor)
    scanner.scan(10)
    if( debugprint == True) : print( 'Done scanning @ {} \n'.format(dt.datetime.now().strftime('%Y-%m-%d %H:%M')) )
    acquired_data = scanner.delegate.scanned_data
    # Storage with debug mode on since I intend to call it on a cron-job and want to keep a log
    result = addTempAndHumiEntry( acquired_data, debugprint )
    return result


def addTempAndHumiEntry( datapoint, debugprint = False ):
    #check if datapoint is a dict type (if it is a list then extract the first item)
    if( type(datapoint) is list ): datapoint = datapoint[0]
    if( type(datapoint) is not dict ): return False
    #Get data from file
    try:
        if( os.path.exists(rbps_io.switchbot_temphumi_log) ):
            #Open file in read only mode only
            tempfile = open(rbps_io.switchbot_temphumi_log, 'r')
            tempdata = json.load(tempfile)
            tempfile.close()
            if( debugprint == True) : print('Reading data from file {} \n'.format(rbps_io.switchbot_temphumi_log))
        else:
            tempdata = {}
            if( debugprint == True) : print('New file will be created at {} \n'.format(rbps_io.switchbot_temphumi_log))
    except ValueError:
        if( debugprint == True) : print('File {} was empty \n creating new entry...\n'.format(rbps_io.switchbot_temphumi_log))
        print('Empty temp file')
        tempdata = {}
    except IOError:
        print('Unexpected error: {}'.format(sys.exc_info()[0:2]))

    # Start processing the data
    # Get the date to create a JSON key for searching
    #key = dt.date.today().strftime('%Y-%m-%d')
    key_major = datapoint['date']
    key_minor = datapoint['date'] + ' ' + datapoint['time']
    # Get the desired data from the input
    datasliced = {key:datapoint[key] for key in ['temperature', 'humidity', 'battery', 'macaddr']}
    dataentry = {key_minor: [datasliced]}
    
    #search the date key in the current data
    if( key_major in tempdata ):
        #if available, add datapoint
        tempdata[key_major][0].update(dataentry)
        # consider checking if value for that time is already in the list or not
        if( debugprint == True) : print('Added the datapoint {} to the key {} \n'.format(dataentry, key_major))
    else:
        #if not available, add new date key and add datapoint
        tempdata.update({key_major:[dataentry]})
        # consider checking if value for that time is already in the list or not
        if( debugprint == True) : print('Created the key {} and added the datapoint {} \n'.format(key_major, dataentry))
    #finally, re-write json file
    tempfile = open(rbps_io.switchbot_temphumi_log,'w')
    json.dump(tempdata, tempfile, sort_keys=True)
    if( debugprint == True) : print('Re-wrote data to file {} \n'.format(rbps_io.switchbot_temphumi_log))
    tempfile.close()
    return True


# #----------------           
# scanner = Scanner().withDelegate( ScanDelegate() )
# print(" start scanning" )
# scanner.delegate.scanned_data = []
# scanner.scan(10)
# data = scanner.delegate.scanned_data
# print(" end scanning" )



