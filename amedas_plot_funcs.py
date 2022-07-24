# -*- coding: utf-8 -*-

import datetime as dt
import os.path
import json
from collections import OrderedDict as ordDict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import amedas_config as a_cfg

def plotAmedasTempScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_temp_' + date_key + '.png')
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['temp'][0] for key, value in todayvals_sorted.items()]
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
    #plt.ylim([0,(40)])
    plt.title('Temperature @ {}'.format(date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel('Temp [Celcius]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True

def plotAmedasHumidityScatter(data_fname='', date_key='', plot_save_path='./'):
    #if there is no file given, then do nothing
    if( not data_fname ): return False
    #if a date was not specified, then go and look for today's data
    if( not date_key ): date_key = dt.date.today().strftime('%Y-%m-%d')

    #create a file name for the plot
    plot_fname = os.path.join(plot_save_path, 'graph_scatter_amedas_humidity_' + date_key + '.png')
    #get the data from the json file
    allvals = json.load(open(data_fname, 'r'))
    if date_key not in allvals.keys():
        print('Date ({}) does not exists in the JSON file. Graph will not be created.'.format(date_key))
        return False
    todayvals = allvals[date_key]
    todayvals_sorted = ordDict(sorted(todayvals.items()))
    yAxis  = [value[a_cfg.area_code]['humidity'][0] for key, value in todayvals_sorted.items()]
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
    #plt.ylim([0,(40)])
    plt.title('Temperature @ {}'.format(date_key))
    plt.xlabel('Time [%H]')
    plt.ylabel('Humidity [%]')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=24))
    #save the plot!
    plt.savefig(plot_fname)

    return True


#def plotCO2_scatter_all_dates(data_fname='', plot_save_path='./'):
#    Something!
