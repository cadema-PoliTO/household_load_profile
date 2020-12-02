# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 18:37:58 2020

@author: giamm
"""

# from tictoc import tic, toc

import numpy as np
# import matplotlib.pyplot as plt

import datareader #routine created to properly read the files needed in the following 
from load_profiler import load_profiler as lp

###############################################################################


# This file contains a method that, for a given household (considering its 
# availability of each appliance considered in this study) returns the electric
# load profile for the household during one day (1440 min), with a resolution
# of 1 minute.

###############################################################################

########## Input parameters

# en_class = 'A+'
# toll = 15
# devsta = 2
# ftg_avg = 100
# power_max = 3000 #[W]


########## Parameters update to user's input

varname,varval = datareader.read_param('sim_param.csv',';','Parameters')

for ii in range(len(varname)):
    vars()[varname[ii]] = varval[ii]


########## Routine

def house_load_profiler(apps_availability,day,season):
    
    ''' The method returns a load profile for a given household in a total simulation time of 1440 min, with a timestep of 1 min.
    
    Inputs:
        Power_max - maximum available power from the grid (W)
        day - type of day (weekday:'wd'|weekend:'we')
        season - season (summer:'s',winter:'w',autumn or spring:'ap')
        en_class - energetic class of the appliance (from 'A+++' to 'D')
        toll (optional) - tollerance on total time in which the appliance is on (%); default value: 15%
        devsta (optional) - standard deviation on total time in which the appliance is on (min); default value: 2 min
        ftg (optional) - footage of the households (m2), since "continuous" appliances' consumptions are normaized to 100 m2
        
    Outputs:
        house_load_profile - load profile for the household (W)
        energy - energy consumed by each appliance in 24h (Wh/day)
        
    '''
    
    
    ##########  Loading appliances list and attributes
    
    apps,apps_ID,apps_attr = datareader.read_appliances('eltdome_report.csv',';','Input')
    # apps is a 2d-array in which, for each appliance (rows) and attribute value is given (columns)
    # apps_ID is a dictionary in which, for each appliance (key), its ID number,type,week and seasonal behavior (value)
    # apps_attr is a dictionary in which the name of each attribute (value) is linked to its columns number in apps (key)

    
    ########## Time discretization

    dt = 1 #timestep for the simulation (min)
    time = 1440 #total simulation time (min)
    time_sim = np.arange(0,time,dt) #vector of simulation time with the given time-resolution (min
    
    
    ########## Generating the load profile for the house, considering all the appliances
    house_load_profile = np.zeros(np.shape(time_sim)) #load profile in time (W)
    energy = np.zeros(len(apps_ID)) #energy consumed in 24h by each appliance
    
    # The load_profiler method (lp) is used in order to get the load profile for
    # each appliance    
    for app in apps_ID:        
        
        if apps_availability[apps_ID[app][0]] == 0:
            continue
        
        load_profile = lp(app,day,season) #load_profile has to outputs (time and power)
        
        # In case the instantaneous power exceedes the maximum power, some tries
        # are made in order to change the moment in which the next appliance is
        #  switched on (since it is evaluated randomly, according to the cumulative
        #  frequency of utilization for that appliance)
        count = 0
        maxtries = 10
        
        while np.max(house_load_profile[:] + load_profile) > power_max and count < maxtries:
        
            load_profile = lp(app,day,season)
            count += 1
        
        # The energy consumption from each appliance is evaluated by integrating
        # the load profile over the time. Since the time is in minutes, the
        # result is divided by 60 in order to obtain Wh.
        energy[apps_ID[app][0]] = np.trapz(load_profile,time_sim)/60
        
        # The power demand from each appliance is injected into the load profile
        # of the house
        house_load_profile[:] = house_load_profile[:] + load_profile
        
        
    # In case the which loop failed, the instantaneous power is saturated to the
    # maximum power anyway. This may happen because the last appliance to be considered
    # is the lighting, which is of "continuous" type, therefore its profile does 
    # not depend on a cumulative frequency (they are always on) 
    house_load_profile[house_load_profile > power_max] = power_max
    
    return(house_load_profile,energy)

# # Uncomment the following lines to test the function
# apps_availability = np.ones(17)
# day = 'wd'
# season = 's'
# dt = 1
# time = 1440
# time_sim = np.arange(0,time,dt)
# house_load_profile,energy = house_load_profiler(apps_availability,day,season)
# plt.bar(time_sim,house_load_profile,width=dt,align='edge')
        
    