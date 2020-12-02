# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:46:24 2020

@author: giamm
"""

import os
import numpy as np
from scipy.interpolate import interp1d
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
basepath = os.path.dirname(os.path.abspath(__file__))

basedir = basepath[basepath.rfind('\\'):] + '\\' #DIrectory where to take the files from

basepath = basepath[:basepath.rfind('\\')] #Path where the main is

dirname = '\\Input\\' #Directory where to save the files

########## Washing machine (wm) and tumble-drier (td): duty-cycle (dc)

dt=1 # timestep (min)

time = np.array([0,4,10,12,30,39,41,50,55,57,58,59,61,65,67,69,73,74,76,77,84,85,86,90,100,110],dtype='float') #(min)
power = np.array([0,200,200,2000,2000,2000,400,400,400,600,0,0,300,300,0,400,400,0,0,400,400,0,800,800,800,0],dtype='float') #(W)

f = interp1d(time,power, kind='linear')

time_dc = np.linspace(0,time[-1],int(time[-1]/dt+1));
duty_cycle = f(time_dc)

# dirname = '\\Input\\'
filename = 'dutycycle_wm.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as dcwm_file:
    dcwm_writer = csv.writer(dcwm_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    dcwm_writer.writerow(['Time [min]', 'Power [W]'])
    
    for ii in range(np.size(time_dc)):
        dcwm_writer.writerow([time_dc[ii],duty_cycle[ii]])
        
# dirname = '\\Input\\'
filename = 'dutycycle_td.csv'
fname = basepath + dirname + filename
           
with open(fname, mode='w', newline='') as dctd_file:
    dctd_writer = csv.writer(dctd_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    dctd_writer.writerow(['Time [min]', 'Power [W]'])
    
    for ii in range(np.size(time_dc)):
        dctd_writer.writerow([time_dc[ii],duty_cycle[ii]])
        

########## Dish-washer (dw): duty-cycle (dc)

dt=1 # timestep (min)

time = np.array([0,1,40,41,60,61,86,105,106,108,110],dtype='float') #(min)
power = np.array([0,330,330,2200,2200,330,330,2200,660,660,0],dtype='float') #(W)

f = interp1d(time,power, kind='linear')

time_dc = np.linspace(0,time[-1],int(time[-1]/dt+1));
duty_cycle = f(time_dc)

# dirname = '\\Input\\'
filename = 'dutycycle_dw.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as dcdw_file:
    dcdw_writer = csv.writer(dcdw_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    dcdw_writer.writerow(['Time [min]', 'Power [W]'])
    
    for ii in range(np.size(time_dc)):
        dcdw_writer.writerow([time_dc[ii],duty_cycle[ii]])


########## Air-conditioner (ac): load profile (lp)

dt = 10 #timestep (min)
time = 1440 #total time (min)


# These profiles have been computed from a consumption assessment performed by
# Enea (pg.99). For the daily energy consumption, the data is taken from EURECO
    
ACjuly_time = np.array([0,3,6,9,12,15,18,21,22.5,24]) #(h)
ACjuly_power = np.array([1490,900,800,1250,1900,1400,1100,1500,1800,1490]) #(W)
ACsept_time = np.array([0,3,6,9,12,15,18,21,24]) #(h)
ACsept_power = np.array([1480,900,800,1300,1500,1250,1350,1800,1550]) #(W)

# Interpolation in order to get a value for each minute
    
time_lp = np.arange(0,time,dt)/60 #(h)
ACjuly_lp = interp_profile(ACjuly_time,ACjuly_power,time_lp)
ACsept_lp = interp_profile(ACsept_time,ACsept_power,time_lp)

# The values are averaged

ACmean_lp = (ACjuly_lp+ACsept_lp)/2

# Data is adjusted to the average value of total energy consumed in one day,
# according to EURECO (average between 3.08 and 6.57 kWh/day)

ACmean_lp = ACmean_lp/(np.trapz(ACmean_lp,time_lp))
ACmean_lp = ACmean_lp*(3.08+6.57)*1000/2

# dirname = '\\Input\\'
filename = 'loadprof_ac_wde_sawp.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as lpac_file:
    lpac_writer = csv.writer(lpac_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    lpac_writer.writerow(['Time [h]', 'Power [W]'])
    
    for ii in range(np.size(time_lp)):
        lpac_writer.writerow([time_lp[ii],ACmean_lp[ii]])

    
######### Electric (elo) and microwave (mwo) ovens: frequency density (fq) profiles

dt = 10 #timestep (min)
time = 1440 #total time (min)

# Data from REMODECE november 2008

# Week-day (wd) profile

oven_time = np.array([0,3,6,9,12,15,18,21,24])
oven_power = np.array([0,0,10,9,20,40,70,40,5])
time_fq = np.arange(0,time,dt)/60 #(h)

power_fq = interp_profile(oven_time,oven_power,time_fq)

# dirname = '\\Input\\'
filename = 'freqdens_elo_wd_sawp.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as fqelo_file:
    fqelo_writer = csv.writer(fqelo_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    fqelo_writer.writerow(['Time [h]', 'Power [W]'])
    
    for ii in range(np.size(time_fq)):
        fqelo_writer.writerow([time_fq[ii],power_fq[ii]])
 
        
# dirname = '\\Input\\'
filename = 'freqdens_mwo_wd_sawp.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as fqmwo_file:
    fqmwo_writer = csv.writer(fqmwo_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    fqmwo_writer.writerow(['Time [h]', 'Power [W]'])
    
    for ii in range(np.size(time_fq)):
        fqmwo_writer.writerow([time_fq[ii],power_fq[ii]])

# Week-end (we) profile

oven_time = np.array([0,3,6,9,12,15,18,21,24])
oven_power = np.array([0,0,10,0,110,30,100,80,30])

time_fq = np.arange(0,time,dt)/60 #(h)

power_fq = interp_profile(oven_time,oven_power,time_fq)

# dirname = '\\Input\\'
filename = 'freqdens_elo_we_sawp.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as fqelo_file:
    fqelo_writer = csv.writer(fqelo_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    fqelo_writer.writerow(['Time [h]', 'Power [W]'])
    
    for ii in range(np.size(time_fq)):
        fqelo_writer.writerow([time_fq[ii],power_fq[ii]])
 
        
# dirname = '\\Input\\'
filename = 'freqdens_mwo_we_sawp.csv'
fname = basepath + dirname + filename

with open(fname, mode='w', newline='') as fqmwo_file:
    fqmwo_writer = csv.writer(fqmwo_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

    fqmwo_writer.writerow(['Time [h]', 'Power [W]'])
    
    for ii in range(np.size(time_fq)):
        fqmwo_writer.writerow([time_fq[ii],power_fq[ii]])
        

########## Appliances: frequency density profiles or load profile

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
    
    if val[2] == 0 and val[3] == 0: # apps from 1 to 5 and from 8 to 15
        
        fname_week = 'all'
        fname_season = 'all'
            
        hour = []
        data = []
        
        # Reading the .dat file and storing its values
    
        filename= fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
        fname = basepath + basedir + filename
        
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
        
        filename = fname_type + '_' + val[1] + '_' + 'wde' + '_' + 'sawp' + '.csv'
        fname = basepath + dirname + filename
        
        with open(fname, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time [W]', 'Power [W]'])
    
            for ii in range(np.size(hour)):
                csv_writer.writerow([hour[ii],data[ii]])
        
    if val[2] == 1 and val[3] == 0: # apps 1,6 and 7
    
        # For week-day profile
        fname_week = 'wd'
        fname_season = 'all'
        
        hour = []
        data = []
        
        # Reading the .dat file and storing its values
        filename= fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
        fname = basepath + basedir + filename

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
        
        filename = fname_type + '_' + val[1] + '_' + 'wd' + '_' + 'sawp' + '.csv'
        fname = basepath + dirname + filename
        
        with open(fname, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time [W]', 'Power [W]'])
    
            for ii in range(np.size(hour)):
                csv_writer.writerow([hour[ii],data[ii]])
          
        # For week-end profile
        fname_week = 'we'
        fname_season = 'all'
        
        hour = []
        data = []
        
        # Reading the .dat file and storing its values
        filename= fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
        fname = basepath + basedir + filename
        
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
        
        filename = fname_type + '_' + val[1] + '_' + 'we' + '_' + 'sawp' + '.csv'
        fname = basepath + dirname + filename
        with open(fname, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time [W]', 'Power [W]'])
    
            for ii in range(np.size(hour)):
                csv_writer.writerow([hour[ii],data[ii]])
                
                
########## Lighting (lux): load profile (lp)

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

aux_dict = dict({0:('su','s'),1:('wi','w'),2:('sa','ap')})

for jj in range(3):
    
    fname_season = aux_dict[jj][0]
    
    hour = []
    data = []
        
    # Reading the .dat file and storing its values
    filename= fname_type + '_' + fname_el + '_' + fname_week + '_' + fname_season + '.dat'
    fname = basepath + basedir + filename
    
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
        
    filename = fname_type + '_' + val[1] + '_' + 'wde' + '_' + aux_dict[jj][1] + '.csv'
    fname = basepath + dirname + filename
    
    with open(fname, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['Time [h]', 'Power [W]'])
    
        for ii in range(np.size(hour)):
            csv_writer.writerow([hour[ii],data[ii]]) 
    




