# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 19:46:39 2020

@author: giamm
"""

import numpy as np
import math
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

import datareader #routine created to properly read the files needed in the following 
from cumulative_frequency import cum_freq #routine created to evaluate the cumulative frequency for a given appliance, over 24h
from profile_interpolation import interp_profile #routine created to interpolate a profile

###############################################################################   
 
   
# This file contains a method that, for a given appliance (considering its 
# frequency density, its cumulative frequency, its duty cycle and its nominal
# yearly energy consumption) returns the load profile for the appliance during 
# one day (1440 min), with a resolution of 1 minute.


###############################################################################

######### Input parameters

# en_class='A+++'
# toll = 15
# devsta = 2.0
# ftg_avg=100.0


########## Parameters update to user's input

varname,varval = datareader.read_param('sim_param.csv',';','Parameters')

for ii in range(len(varname)):
    vars()[varname[ii]] = varval[ii]

    
########## Routine
 
def load_profiler(app,day,season):
    
    ''' The method returns a load profile for a given appliance in a total simulation time of 1440 min, with a timestep of 1 min.
    
    Inputs:
        app - name of the appliance(str)
        day - type of day (weekday:'wd'|weekend:'we')
        season - season (summer:'s',winter:'w',autumn or spring:'ap')
    
    Outputs:
        load_profile - load profile for the appliance (W) 
    '''
    
    dt = 1 #timestep of the simulation (min)
    time = 1440 #total simulation time (min)
    time_sim = np.arange(0,time,dt) #time vector of the simulation (min) from 00:00 to 23:59
    

    ##########  Loading appliances list and attributes
    
    apps,apps_ID,apps_attr = datareader.read_appliances('eltdome_report.csv',';','Input')
    # apps is a 2d-array in which, for each appliance (rows) and attribute value is given (columns)
    # apps_ID is a dictionary in which, for each appliance (key), its ID number,type,week and seasonal behavior (value)
    # apps_attr is a dictionary in which the name of each attribute (value) is linked to its columns number in apps (key)
    
    # Loading nominal yearly energy consumption for each appliance, for each energetic class
    
    ec_yearly_energy,ec_levels_dict = datareader.read_enclasses('classenerg_report.csv',';','Input')
    # ec_yearly_energy is a 2d-array in which for each appliance, its yearly energy consumption is presented for each energetic class
    # ec_levels_dict is a dictionary that links each energetic level (value) to its columns number in ec_yearly_energy
    
    # Loading the coefficient matrix, related to how utents use an appliance in a certain season
    
    coeff_matrix,seasons_dict = datareader.read_enclasses('coeff_matrix.csv',';','Input')
    # coeff_matrix is a 2d-array in which for each appliance, its coefficient k, related to utent's behavior in different seasons, is presented
    # seasons_dict is a dictionary that links each season (value) to its columns number in coeff_matrix
    
    
    ########## Extracting the correct data for the appliance from the applinces's attributes
    
    # T_on: duration of the time period in which an appliance is switched on during a day (min)
    T_on = apps[apps_ID[app][0], #first index: ID number of the appliance
                list(apps_attr.keys())[list(apps_attr.values()).index('time_on[min/day]')] #second index: position of the attribute in the dictionary
                -(len(apps_attr)-np.size(apps,1))] #this is needed because non-numeric attributes are not considered in the matrix apps
    
    # energy: yearly energy consumption (kWh/year)
    energy = ec_yearly_energy[apps_ID[app][0], #first index: ID number of the appliance
                list(ec_levels_dict.keys())[list(ec_levels_dict.values()).index(en_class)]] #second index: number corresponding to the energy class in dictionary
    
    # kk: utent's seasonal behavior coefficient (-)
    kk = coeff_matrix[apps_ID[app][0], #first index: ID number of the appliance
                list(seasons_dict.keys())[list(seasons_dict.values()).index(season)]] #second index: number corresponding to the energy class in dictionary
    
    # k_ftg: coefficient that adapts the consumption from ac and lux 
    # ("continuous" type appliances) to the actual footage of the household
    # since the data is given for a 100 m2 household
    k_ftg = ftg_avg/100 #(m2/m2)
    
    # The nominal power is evaluated, according to the yearly energy 
    # consumption (kWh/year) and the time-period in which the appliance is 
    # switched on during a day (min/day). The first one is given in kWh/year
    # and it is multiplied by 1000 and divided by 365 in order to get Wh/day.
    # The second one is given in minutes and it is divided by 60 to get hours.
    
    pow = (energy*1000/365)/(T_on/60) #(W)
    
    
    ########## Selecting the correct data-file to load, according to the 
    # appliance's type, day type and season
    # This also results in the routine that will be followed
    
    app_nickname = apps_ID[app][1] #nickname: 2 or 3 characters string identifying the appliance
    app_type = apps_ID[app][2] #type: 'continuous'|'no_duty_cycle'|'duty_cycle'|
    app_wbe = apps_ID[app][3] #wbe (week behavior): 'wde'|'we','wd'
    app_sbe = apps_ID[app][4] #sbe (seasonal behavior): 'sawp'|'s','w','ap'
    
    # The name of the file to be loaded (fname) can now be built
    
    fname_nickname = app_nickname
    fname_day = 'wde' #default choice: if the appliance has got different profiles in different days of the week, this will be changed
    fname_season = 'sawp' #default choice: if the appliance has got different profiles in different seasons, this will be changed
    
    if len(app_wbe) > 1:
        fname_day = day
    
    if len(app_sbe) > 1:
        fname_season = season
    
    
    ########## Routine to be followed for appliances which belong to "continuous" type (ac and lux)
    # The load profile has already been evaluated therefore it only needs to be
    # loaded and properly managed
    
    if app_type == 'continuous':
        
        fname_type = 'loadprof'
        filename = fname_type + '_' + fname_nickname + '_' + fname_day + '_' + fname_season + '.csv'
        
        data_lp = datareader.read_general(filename,';','Input')
        time_lp = data_lp[:,0] #(h)
        time_lp = time_lp*60 #conversion to minutes
        power_lp = data_lp[:,1] #(W)
        load_profile = power_lp
        
        # Profile's interpolation if it has a different time-resolution
        if (time_lp[-1])/(np.size(time_lp)-1) != dt: 
            
            load_profile = interp_profile(time_lp,power_lp,time_sim)
                   
        load_profile = load_profile*kk*k_ftg #adjustment according to users' seasonal behavior and household's footage
        return(load_profile)
   
     
    ########## Routine to be followed for appliances which belong to "duty cycle"
    # or "no duty cycle" types.
    # The load profile has to be evaluated according to the duration of the 
    # time-period in which they are switched on (T_on) and to the frequency density
    # of their usage during the day
     
    # The profile of the duty-cycle is loaded for those appliances which have one
    if app_type =='duty_cycle':
        
        fname_type = 'dutycycle'
        filename = fname_type + '_' + fname_nickname + '.csv'
        
        data_dc = datareader.read_general(filename,';','Input')
        time_dc = data_dc[:,0] #(min)
        power_dc = data_dc[:,1] #(W)
        duty_cycle = power_dc
        
        # Duty-cycle's interpolation if it has a different time resolution
        if (time_dc[-1])/(np.size(time_dc)-1) != dt:
            f = interp1d(time_dc,power_dc, kind='linear', bounds_error = False, fill_value = 'extrapolate')
            time_dc = np.arange(0,time_dc[-1]+dt,dt)
            duty_cycle = f(time_dc)
      
    # A uniform duty-cycle is built for appliances that use a constant power
    # according to the time-period in a day in which they are used (T_on)  
    if app_type == 'no_duty_cycle':
       
        if T_on != time: #not valid for appliances which are used constantly
        
            # A randomly variating (in a normal distribution) cycle-duration is 
            # assumed for appliances which don't have a specified duty-cycle
            
            # T_on = math.round(duration_gauss(T_on,2,15)) # This can be replaced by the following lines, so no need for another function
            d = T_on
            lim_up = d+(toll*(d)/100)        
            lim_low = d-(toll*(d)/100)
            lim_up , lim_low = np.clip((lim_up,lim_low),0,time) #in order not to exceed the simulation time with T_on
            T_on = 0
            
            while (T_on > lim_up or T_on < lim_low):
                T_on = int(np.random.normal(d,devsta))
                
        time_dc = np.linspace(0,T_on,int(T_on/dt+1))
        duty_cycle = np.ones(np.shape(time_dc))
        
        # The duty cycle is given with the same shape as "duty_cycle" type appliances, 
        # meaning that the first value for the power is 0
        duty_cycle[0] = 0
     
        
    # Creating a new duty cycle, that takes into account the actual nominal power 
    # and the users' habits (coefficient kk, varying according to the season)
    duty_cycle = duty_cycle/np.mean(duty_cycle)*pow*kk
    
    ########## The frequency distribution for the usage of the appliance during
    # the day is loaded and managed in order to get a cumulative frequency
    
    fname_type = 'freqdens'
    filename = fname_type + '_' + fname_nickname + '_' + fname_day + '_' + fname_season + '.csv'
    data_fq = datareader.read_general(filename,';','Input')
    time_fq = data_fq[:,0] #(h)
    time_fq = time_fq*60 #conversion to minutes
    power_fq = data_fq[:,1] #(W)
    freq_dens = power_fq
    
    # Frequency density's interpolation if it has a different time resolution
    if (time_fq[-1])/(np.size(time_fq)-1) != dt:
            freq_dens = interp_profile(time_fq,power_fq,time_sim)
    
    # Cumulative frquency of appliance'usage in 24h (with the same time resolution as the current simulation)
    cumfreq = cum_freq(time_sim,freq_dens)
 
    
    ######### The load profile is built, selecting a random istant in which
    # the appliances starts working (according to the cumulative frequency) 
    # and using its duty-cycle (uniform for those appliances which don't have a duty-cycle)
    
    # Selecting a random instant when to make the appliance start its cycle, 
    # according to the frequency density and the cumulative frequency
    random_probability = np.random.rand()
    
    # Basing on the random probability research, a time instant at which the 
    # appliance starts its cycle is evaluated through the cumulative frequency
    time_instant = time_sim[cumfreq >= random_probability][0]
    instant_index = int(np.where(time_sim == time_instant)[0]) 
    
    load_profile=np.zeros(np.shape(time_sim))
    
    # The load profile is built using the appliances' duty-cycle.
    # Whenever the index tt (associated at a certain time moment in time_sim)
    # exceeeds the total time of simulation, the latter is subtracted so that
    # the value of the power in that instant is added starting from the beginning
    # of the vector
    
    for ii in range(0, len(time_dc)):
         
        tt=instant_index+ii
        if (tt>=len(time_sim)):
                tt=tt-len(time_sim)
               
        load_profile[tt]=duty_cycle[ii]
    
    
    return (load_profile)


# # ##### Uncomment the following lines to test the function (comment def and return)
# # app = 'vacuum_cleaner'
# app = 'air_conditioner'
# # app = 'electric_oven'
# # app = 'microwave_oven'
# # app = 'fridge'
# # app = 'freezer'
# # app = 'washing_machine'
# # app = 'dish_washer'
# # app = 'tumble_drier'
# # app = 'electric_boiler'
# # app = 'hifi_stereo'
# # app = 'dvd_reader'
# # app = 'tv'
# # app = 'iron'
# # app = 'pc'
# # app = 'laptop'
# # app = 'lighting'

# day = 'we'
# season = 's'

# dt = 1 
# time = 1440 
# time_lp = np.arange(0,time,dt)
# load_profile=load_profiler(app,day,season)
# # plt.bar(time_lp,load_profile,width=time_lp[-1]/np.size(time_lp))
# plt.plot(time_lp,load_profile)