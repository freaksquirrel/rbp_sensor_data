# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import datetime as dt
import os.path
import json
from collections import OrderedDict as ordDict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

# == Plot the CO2 values from the mhz19b sensor
def plotCO2_scatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, 'graph_scatter_co2vals_' + date_key + '.png')
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key][0]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value for key, value in todayvals_sorted.items()]
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on cunstruction....)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.xlim([0,(24)])
    plt.ylim([0,(5000)])
    plt.title('Air Quality @ {}'.format(date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel('CO2 [ppm]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True

# == Plot the temperature and humidity values from the SwitchBot meter
def plotTempHumidity_scatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, 'graph_scatter_temphumivals_' + date_key + '.png')
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key][0]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    #Add the values
    vals_temp = [0.0]*len(todayvals_sorted)
    vals_humi = [0]*len(todayvals_sorted)
    vals_batt = [0]*len(todayvals_sorted)
    vals_maca = ['']*len(todayvals_sorted)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        #print("Index: {} , key: {}, value:{}".format(index,key,value))
        vals_temp[index] = value[0]['temperature']
        vals_humi[index] = value[0]['humidity']
        vals_batt[index] = value[0]['battery']
        vals_maca[index] = value[0]['macaddr']

    #yAxis  = [value for key, value in todayvals_sorted.items()]
    yAxis  = vals_temp
    yAxis2 = vals_humi
    #set the X axis as a float describing the hour of the day (e.g., 13.5 = 13:30) 
    xAxis = [0]*len(yAxis)
    for (index, (key, value)) in enumerate(todayvals_sorted.items()):
        xAxis[index] = (float(key.split(' ')[1].split(':')[0])) + (float(key.split(' ')[1].split(':')[1]) / 60)

    #Format the plot   (this part is still on construction....)
    plt.style.use('dark_background')
    #plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(xAxis,yAxis, color='limegreen', marker='v')
    plt.grid(True)
    plt.title('Temperature / Humidity @ Home office room')
    ax.set_xlabel('Time [%H]')
    ax.set_ylabel('Temp [Celcius]', color='limegreen')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #create the second axis
    ax2 = ax.twinx()
    ax2.plot(xAxis,yAxis2, color='deepskyblue', marker='^')
    #plt.grid(True)
    plt.grid(color = 'deepskyblue', linestyle = '--', linewidth = 0.5)
    ax2.set_ylabel('Humidity [%]',color='deepskyblue')
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    plt.xlim([0,(24)])
    plt.ylim([0,(100)])

    #save the plot!
    plt.savefig(plot_fname)

    return True


#def plotCO2_scatter_all_dates(data_fname='', plot_save_path='./'):
#    Something!
