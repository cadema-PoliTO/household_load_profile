# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:46:24 2020

@author: giamm
"""
import os
from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import csv
import matplotlib.pyplot as plt
import math

from profile_interpolation import interp_profile

##############################################################################


# This script is used to create some .csv files where to store the duty-cycles
# for appliances like the washing-machine and the dish-washer and the load
# profile for aplliances like the aire-conditioner and the lighting

# The base path is saved in the variable basepath, it is used to move among
# directories to find the files that need to be read.
basepath = Path(__file__).parent.parent
basedir = Path(__file__).parent #Directory where the input files for this script are to be found
dirname = 'Input' #Directory where to save the files created in this script


## Washing machine (wm) and tumble-drier (td): duty-cycle (dc)

dt = 1 # timestep (min)

# time = np.array([0,4,10,12,30,39,41,50,55,57,58,59,61,65,67,69,73,74,76,77,84,85,86,90,100,110],dtype='float') #(min)
# power = np.array([0,200,200,2000,2000,2000,400,400,400,600,0,0,300,300,0,400,400,0,0,400,400,0,800,800,800,0],dtype='float') #(W)

# Data derived from CESI
time = np.array([0,1,10,11,16,18,20,37,40,55,56,57,58,59,60,65,66,67,68,72,73,74,75,80,81,83,84,85,86,88,89,90], dtype='float') #(min)
power = np.array([0,10,10,100,100,80,100,100,20,20,30,30,0,0,15,15,0,0,20,20,0,0,20,20,15,15,0,0,40,40,0,0], dtype='float') # (%)

# Interpolating
f = interp1d(time,power, kind='linear')

time_dc = np.linspace(0,time[-1],int(time[-1]/dt+1))
duty_cycle = f(time_dc)

# Saving the result
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'dutycycle_wm.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (min)', 'Power (W)'])
    
    for ii in range(np.size(time_dc)):
        csv_writer.writerow([time_dc[ii],duty_cycle[ii]])
        
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'dutycycle_td.csv'
fname = Path(basepath / dirname / filename)
           
with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (h)', 'Power (W))'])
    
    for ii in range(np.size(time_dc)):
        csv_writer.writerow([time_dc[ii],duty_cycle[ii]])
      

## Dish-washer (dw): duty-cycle (dc)

dt = 1 # timestep (min)

# Data from CESI (Ferro: Pnom = 2200 W)
time = np.array([0,1,25,26,27,35,36,59,60,80,81,82,83,89,90,91,92,104,105,108,109,110], dtype='float') #(min)
power = np.array([0,15,15,0,15,15,100,100,15,15,0,0,100,100,0,0,100,100,30,30,0,0], dtype='float') # (%)

# Interpolating
f = interp1d(time,power, kind='linear')

time_dc = np.linspace(0,time[-1],int(time[-1]/dt+1))
duty_cycle = f(time_dc)

# Saving the result
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'dutycycle_dw.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (min)', 'Power (W)'])
    
    for ii in range(np.size(time_dc)):
        csv_writer.writerow([time_dc[ii],duty_cycle[ii]])


## Air-conditioner (ac): average daily load profile (lp)

dt = 10 #timestep (min)
time = 1440 #total time (min)

# # These profiles have been computed from a consumption assessment performed by
# # RSE Enea (pg.99). For the daily energy consumption, the data is taken from EURECO
# ACjuly_time = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,21.5,22,22.5,23,24]) #(h)
# ACjuly_power = np.array([250,250,250,250,125,100,100,100,100,125,250,500,625,650,625,800,850,850,800,500,250,250,400,650,650,500,250]) #(W)
# ACsept_time = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,12.5,13,14,15,16,17,18,19,20.5,21,21.5,22,22.5,23,24]) #(h)
# ACsept_power = np.array([250,250,250,100,100,100,100,100,100,125,125,250,500,500,250,250,500,500,850,850,500,250,250,500,500,500,250,250]) #(W)

# Data derived from REMODECE (two profiles, one for weekday and one for weekend)
ACwd_time = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]) #(h)
ACwd_power = np.array([350,340,330,300,300,300,250,160,140,160,140,175,190,190,300,325,300,230,215,200,150,200,270,320,350]) #(h)
ACwe_time = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]) #(h)
ACwe_power = np.array([275,280,290,250,225,250,200,150,140,150,150,150,120,200,260,280,275,220,190,175,230,240,240,275,275]) #(h)

# Interpolation in order to get a value for each minute
time_lp = np.arange(0,time,dt)/60 #(h)
# ACjuly_lp = interp_profile(ACjuly_time,ACjuly_power,time_lp)
# ACsept_lp = interp_profile(ACsept_time,ACsept_power,time_lp)
# ACwd_lp = interp_profile(ACwd_time,ACwd_power,time_lp)
# ACwe_lp = interp_profile(ACwe_time,ACwe_power,time_lp)

f_wd= CubicSpline(ACwd_time, ACwd_power, bc_type='periodic')
ACwd_lp = f_wd(time_lp)

f_we = CubicSpline(ACwe_time, ACwe_power, bc_type='periodic')
ACwe_lp = f_we(time_lp)


# The values are averaged
# ACmean_lp = (ACjuly_lp+ACsept_lp)/2
ACmean_lp = (ACwd_lp*5 + ACwe_lp*2)/7

# Data is adjusted to the average value of total energy consumed in one day,
# according to EURECO (average between 3.08 and 6.57 kWh/day)
# ACmean_lp = ACmean_lp/(np.trapz(ACmean_lp,time_lp))
# ACmean_lp = ACmean_lp*(3.08+6.57)*1000/2

# Saving the result
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'avg_loadprof_ac_wde_sawp.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (h)', 'Power (W)'])
    
    for ii in range(np.size(time_lp)):
        csv_writer.writerow([time_lp[ii],ACmean_lp[ii]])

    
## Electric (elo) and microwave (mwo) ovens: average daily load profiles (lp)

dt = 10 #timestep (min)
time = 1440 #total time (min)

# Week-day (wd) 

# Data from REMODECE november 2008 (no more available online)
oven_time = np.array([0,3,6,9,12,15,18,21,24])
oven_power = np.array([0,0,10,9,20,40,70,40,5])

# # Data from REMODECE final (available but for Europe)
# oven_time_wd = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
# oven_power_wd = np.array([1,1,1,1,2,2.3,2.6,3,3,2,2.3,5,6,4,3.5,3.3,2.5,2.8,4.3,5.8,3.3,3,2.2,2,1])

# Interpolating
time_lp = np.arange(0, time, dt)/60 #(h)
power_lp = interp_profile(oven_time,oven_power,time_lp)

# Saving the results for electric oven (weekday)
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'avg_loadprof_elo_wd_sawp.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (h)', 'Power (W)'])
    
    for ii in range(np.size(time_lp)):
        csv_writer.writerow([time_lp[ii],power_lp[ii]])
 
# Saving the results for microwave oven (weekday)
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'avg_loadprof_mwo_wd_sawp.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (h)', 'Power (W)'])
    
    for ii in range(np.size(time_lp)):
        csv_writer.writerow([time_lp[ii],power_lp[ii]])

# Week-end (we) 

# Data from REMODECE november 2008 (no more available online)
oven_time = np.array([0,3,6,9,12,15,18,21,24])
oven_power = np.array([0,0,10,0,110,30,100,80,30])

# Interpolating
time_lp = np.arange(0, time, dt)/60 #(h)
power_lp = interp_profile(oven_time,oven_power,time_lp)

# Saving the results for electric oven (weekend)
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'avg_loadprof_elo_we_sawp.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (h)', 'Power (W)'])
    
    for ii in range(np.size(time_lp)):
        csv_writer.writerow([time_lp[ii],power_lp[ii]])
 
# Saving the results for microwave oven (weekend)
# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
filename = 'avg_loadprof_mwo_we_sawp.csv'
fname = Path(basepath / dirname / filename)

with open(fname, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    csv_writer.writerow(['Time (h)', 'Power (W)'])
    
    for ii in range(np.size(time_lp)):
        csv_writer.writerow([time_lp[ii],power_lp[ii]])
        

########## Appliances: average daily load profiles

# app_dict: key: app_ID, value:(app name|app nickname|entries for different days in the week|entries for different seasons)
app_dict = dict({
    0:('vacuum_cleaner','vc',1,0),
    1:('air_conditioner','ac',0,0),
    2:('electric_oven','elo',0,0),
    3:('microwave_oven','mwo',0,0),
    4:('fridge','frg',0,0),
    5:('freezer','frz',0,0),
    6:('washing_machine','wm',1,0),
    7:('dish_washer','dw',1,0),
    8:('tumble_drier','td',1,0),
    9:('electric_boiler','bo',0,0),
    10:('hifi_stereo','hs',0,0),
    11:('dvd_reader','vr',0,0),
    12:('tv','tv',0,0),
    13:('iron','ir',0,0),
    14:('pc','pc',0,0),
    15:('laptop','lap',0,0),
    16:('lighting','lux',0,2)
    })

# dirname = 'Input' #Uncomment this in case you want to save the file in a different folder
fname_type = 'freqdens'

for key in app_dict:
    
    val = app_dict[key]
    
    app_name = val[0]
    app_nickname= val[1]
    
    # The procedure is not needed for ovens and air-conditioner (data already in the correct format), and lighting (different procedure)
    if app_name == 'electric_oven' or app_name == 'microwave_oven' or app_name == 'air_conditioner' or app_name == 'lighting': continue
    
    # Some appliances use the same data as other ones
    if app_name == 'vacuum_cleaner' or app_name == 'tumble_drier': app_nickname = 'wm'
    elif app_name == 'hifi_stereo': app_nickname = 'vr'
    elif app_name == 'iron': app_nickname = 'tv'
    elif app_name == 'laptop': app_nickname = 'pc'
    
    fname_el = app_nickname
    
    if val[2] == 0 and val[3] == 0: # apps with the same load profiles for different days and seasons
        
        fname_week = 'all'
        fname_season = 'all'
            
        hour = []
        data = []
        
        # Reading the .dat file and storing its values
        filename= fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
        fname = Path(basepath / basedir / filename)
        
        with open(fname) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for line_count, row in enumerate(csv_reader):
                
                t = float(row[0])
                if not t.is_integer():
                    t = math.floor(t) + (t - math.floor(t))*100/60
                    # The previous operation was needed to convert the hour value 
                    # in a sexagesimal system
                        
                hour.append(float(t))
                data.append(float(row[1]))                   
            
        hour = np.array(hour)
        data = np.array(data)
        
        # Writing the .csv file
        filename = 'avg_loadprof' + '_' + val[1] + '_' + 'wde' + '_' + 'sawp' + '.csv'
        fname = Path(basepath / dirname / filename)
        
        with open(fname, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time (h)', 'Power (W)'])
    
            for ii in range(np.size(hour)):
                csv_writer.writerow([hour[ii],data[ii]])
        
    if val[2] == 1 and val[3] == 0: # apps with different load profile in different days of the week
    
        # For week-day profile
        fname_week = 'wd'
        fname_season = 'all'
        
        hour = []
        data = []
        
        # Reading the .dat file and storing its values
        filename= fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
        fname = Path(basepath / basedir / filename)

        with open(fname) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for line_count, row in enumerate(csv_reader):
                
                t = float(row[0])
                if not t.is_integer():
                    t = math.floor(t) + (t - math.floor(t))*100/60
                    # The previous operation was needed to convert the hour value 
                    # in a sexagesimal system
                        
                hour.append(float(t))
                data.append(float(row[1]))
                               
        hour = np.array(hour)
        data = np.array(data)
        
        # Writing the .csv file
        filename = 'avg_loadprof' + '_' + val[1] + '_' + 'wd' + '_' + 'sawp' + '.csv'
        fname = Path(basepath / dirname / filename)
        
        with open(fname, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time (h)', 'Power (W)'])
    
            for ii in range(np.size(hour)):
                csv_writer.writerow([hour[ii],data[ii]])
          
        # For week-end profile
        fname_week = 'we'
        fname_season = 'all'
        
        hour = []
        data = []
        
        # Reading the .dat file and storing its values
        filename = fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
        fname = Path(basepath / basedir / filename)
        
        with open(fname) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for line_count, row in enumerate(csv_reader):
                
                t = float(row[0])
                if not t.is_integer():
                    t = math.floor(t) + (t - math.floor(t))*100/60
                    # The previous operation was needed to convert the hour value 
                    # in a sexagesimal system
                        
                hour.append(float(t))
                data.append(float(row[1]))
                             
        hour = np.array(hour)
        data = np.array(data)
        
        # Writing the .csv file
        filename = 'avg_loadprof' + '_' + val[1] + '_' + 'we' + '_' + 'sawp' + '.csv'
        fname = Path(basepath / dirname / filename)
        with open(fname, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time (h)', 'Power (W)'])
    
            for ii in range(np.size(hour)):
                csv_writer.writerow([hour[ii],data[ii]])
                
                
########## Lighting (lux): average daily load profile (lp)

dt = 1 #timestep (min)
time = 1440 #total time (min)

val_list = list(app_dict.values()) 
ii = 0
for tup in val_list:
    if tup[0] == 'lighting':
        key = ii 
        break
    ii += 1  # this lines are used to get the key corresponding to lighting
    
fname_type = 'loadprof'
fname_el = app_dict[key][1]
fname_week = 'all'
# Dirname = 'Input' #Uncomment this in case you want to save the file in a different folder

aux_dict = dict({0:('su','s'),1:('wi','w'),2:('sa','ap')})

for jj in range(len(aux_dict)):
    
    fname_season = aux_dict[jj][0]
    
    hour = []
    data = []
        
    # Reading the .dat file and storing its values
    filename = fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
    fname = Path(basepath / basedir / filename)
    
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for line_count, row in enumerate(csv_reader):
                
            t = float(row[0])
            if not t.is_integer():
                t = math.floor(t) + (t - math.floor(t))*100/60
                # The previous operation was needed to convert the hour value 
                # in a sexagesimal system
                        
            hour.append(float(t))
            data.append(float(row[1]))
                            
    hour = np.array(hour)
    data = np.array(data)
        
    # Writing the .csv file
    filename = 'avg_loadprof' + '_' + val[1] + '_' + 'wde' + '_' + aux_dict[jj][1] + '.csv'
    fname = Path(basepath / dirname / filename)
    
    with open(fname, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['Time (h)', 'Power (W)'])
    
        for ii in range(np.size(hour)):
            csv_writer.writerow([hour[ii],data[ii]]) 
    




