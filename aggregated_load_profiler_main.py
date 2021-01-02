# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:53:11 2020

@author: giamm
"""

import numpy as np
# import matplotlib.pyplot as plt
import random
# import math
import csv
from pathlib import Path

import datareader
import parameters_input_new as inp
import plot_generator  as plot
from house_load_profiler import house_load_profiler as hlp
from load_profile_aggregator import aggregator as agr
from tictoc import tic, toc

###############################################################################


# This is the _main_ file of a routine that generates the electric load-profile
# for an aggregate of a certain number of households. The total simulation time 
# is 1440 min, while the resolution (timestep) is 1 min.
# The load profile and the daily energy consumption are evaluated for a number
# of households and appliances, according to the availability of each appliance
# in each household (depending on a distribution factor and on the geographical
# location that is chosen). The load profile from all the households is then 
# aggregated and the result is shown with a different time resolution (dt_aggr).
# This is done for each season, both for weekdays and weekend days. The energy 
# consumption from each appliance during the whole year is also evaluated.


###############################################################################
tic()

# The basepath of the file is stored in a variable 
basepath = Path(__file__).parent

# # An /Output folder is created in order to store the results as .csv files
# dirname = 'Output'

# try: Path.mkdir(basepath / dirname)
# except Exception: pass 
  

## Parameters

# Updating the parameters according to user's input by calling the parameters_input() method
params = inp.parameters_input()

# Updating the parameters' values

# Number of households considered (-)
n_hh = params['n_hh']

# Average number of people, for each household (-)
n_people_avg = params['n_people_avg']

# Average square footage of the households (m2)
ftg_avg = params['ftg_avg']  

# Geographical location: 'north' | 'centre' | 'south'
location = params['location']

# Maximum power available from the grid (contractual power) (W)
power_max = params['power_max']

# Energetic class of the appiances: 'A+++' | 'A++' | 'A+' | 'A' | 'B' | 'C' | 'D'
en_class = params['en_class']

# For appliances which don't have a duty-cycle and do not belong to "continuous"
# type, the time in which they are siwtched on during 24h (T_on) is modified
# exctracting a random duration from a normal distribution (centred in T_on, with
# standard deviation equal to devsta), in a range defined by toll

# Tollerance on total time in which the appliance is on (duration) (%)
toll = params['toll']

# Standard deviation on total time in which the appliance is on (duration) (min)
devsta = params['devsta']

# Time-step used to aggregated the results (min): 1 | 5 | 10 | 15 | 10 | 30 | 45 | 60
dt_aggr = params['dt_aggr']

# Quantile for the evaluation of maximum, medium and minimum power demands at each time-step
q_max = params['q_max']
q_med = params['q_med']
q_min = params['q_min']

# Time-scale for plotting: 'min' | 'h' 
time_scale = params['time_scale'] 

# Power_scale for plotting: 'W' | 'kW' | 'MW'
power_scale = params['power_scale'] 

# Energy_scale for plotting: 'Wh' | 'kWh' | 'MWh' 
energy_scale = params['energy_scale']


## Time 
# Time discretization for the simulation    

# Time-step, total time and vector of time from 00:00 to 23:59 (one day) (min)
dt = 1 
time = 1440 
time_sim = np.arange(0,time,dt) 

# Time vector for the aggregation of the results (min)
time_aggr = np.arange(0,time,dt_aggr) 

## Input data for the appliances
# Appliances' attributes, energy consumptions and user's coefficients 

apps, apps_ID, apps_attr = datareader.read_appliances('eltdome_report.csv', ';', 'Input')
# apps is a 2d-array in which, for each appliance (rows) and attribute value is given (columns)
# apps_ID is a dictionary in which, for each appliance (key), its ID number,type,week and seasonal behavior (value)
# apps_attr is a dictionary in which the name of each attribute (value) is linked to its columns number in apps (key)

ec_yearly_energy, ec_levels_dict = datareader.read_enclasses('classenerg_report.csv', ';', 'Input')
# ec_yearly_energy is a 2d-array in which for each appliance, its yearly energy consumption is given for each energetic class
# ec_levels_dict is a dictionary that links each energetic level (value) to its columns number in ec_yearly_energy

coeff_matrix, seasons_dict = datareader.read_enclasses('coeff_matrix.csv',';','Input')
# coeff_matrix is a 2d-array in which for each appliance, its coefficient k, related to user's behaviour in different seasons, is given
# seasons_dict is a dictionary that links each season (value) to its columns number in coeff_matrix

# Creating a dictionary to pass such data to the various methods
appliances_data = {
    'apps': apps,
    'apps_ID': apps_ID,
    'apps_attr': apps_attr,
    'ec_yearly_energy': ec_yearly_energy,
    'ec_levels_dict': ec_levels_dict,
    'coeff_matrix': coeff_matrix,
    'seasons_dict': seasons_dict,
    }


## Building the appliances availability matrix
# A 2d-array is built in which, for each household (columns) it is
# shown which appliances are available for the household, according to the 
# distribution factor of each appliance in a given location (1 if available, 0 otherwise)

# Initializing the array
apps_availability = np.zeros((len(apps_ID),n_hh))

# A dictionary that relates each location (key) to the related columns in apps(for distribution factors)
location_dict = {
    'north': apps_attr['distribution_north'] - (len(apps_attr) - np.size(apps, 1)), 
    'centre': apps_attr['distribution_centre'] - (len(apps_attr) - np.size(apps, 1)), 
    'south': apps_attr['distribution_south'] - (len(apps_attr) - np.size(apps, 1)),
    }

# Building the matrix
for app in apps_ID:

    # The ID number of the appliance is stored in a variable since it will be used man times
    app_ID = apps_ID[app][apps_attr['id_number']]  
    
    # Extracting the distribution factor for the appliance in the current geographical location
    distr_fact = apps[app_ID, location_dict[location]] 

    # Evaluating the number of households in which the appliance is available      
    n_apps_app_type = int(np.round(n_hh*distr_fact))   

    # Extracting randomly the households in which the appliance is available, from the total number of households  
    samp = random.sample(list(range(0, n_hh)), n_apps_app_type) 
    
    # Assigning the appliance's availability to the households present in the sample
    apps_availability[apps_ID[app][0],samp] = 1 


## Building seasons and week dictionaries 
# This is done in order to explore all the seasons and, for each season two types of days (weekday and weekend)

seasons = {'winter': (0, 'w'), 'summer': (1, 's'), 'spring': (2, 'ap'), 'autumn': (3, 'ap')}
days = {'week-day': (0, 'wd'), 'weekend-day': (1, 'we')}

#  A reference year is considered, in which the first day (01/01) is a monday. 
# Therefore, conventionally considering that winter lasts from 21/12 to 20/03, 
# spring from 21/03 to 20/06, summer from 21/06 to 20/09 and winter from 21/09
# to 20/12, each seasons has got the following number of weekdays and weekend days.
days_distr = {'winter': {'week-day': 64, 'weekend-day': 26},
             'spring': {'week-day': 66, 'weekend-day': 26},
             'summer': {'week-day': 66, 'weekend-day': 26},
             'autumn': {'week-day': 65, 'weekend-day': 26}
             }


### Evaluating the load profiles for all the households
# The aggregated load profiles are evaluated for both a week day and a weekend
# day for the four seasons and the seasonal energy consumption from each 
# appliance, for each household are evaluated.

# First, some quantities are initialized, that will be useful for storing the results

# Quantile are evaluated for the load profiles. It means that for each timestep
# the maximum power (demanded by less than 15% of the households), the median
# power (demanded by less than 50% of the households) and the minimum (demanded 7
# by less than 85% of the households).
nmax = int(np.round(n_hh*q_max/100))
nmed = int(np.round(n_hh*q_med/100))
nmin = int(np.round(n_hh*q_min/100)) 


# A random sample of n_samp houses is also extracted in order to plot, for each 
# of them, the load profile during one day for each season, for each day-type.
n_samp = 5

# A random sample is extracted from the total number of households
samp = random.sample(list(range(0, n_hh)), n_samp) 

# A list where to store the header for a .csv file is initialized
sample_lp_header = [] 

# sample_lp = np.zeros((time,n_samp*len(seasons)*len(days))) #The load profiles for the houses in the sample are stored in a proper array
# sample_slicingaux = np.arange(n_samp) #This array is useful for properly slicing the households_lp array and storing the load profiles of the households in the random sample

# Storing some useful quantities into variables
n_seasons = len(seasons)
n_days = len(days)
n_apps = len(apps_ID)
n_time_sim = np.size(time_sim)
n_time_aggr = np.size(time_aggr)

# Specifying which quantities (load profiles) are going to be stored and plotted
load_profiles_types = {
    0: 'Total',
    1: 'Average',
    2: 'Maximum',
    3: 'Medium',
    4: 'Minimum',
    }

# Number of load profiles that are going to be stored and plotted
n_lps = len(load_profiles_types)

# Creating 3d-arrays where to store each type of load profile, for each season (axis = 0),
# each time-step (axis = 1) and type of day (axis = 2)
lp_tot_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_avg_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_max_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_med_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_min_stor = np.zeros((n_seasons, n_time_aggr, n_days))

# Creating a 3d.array where to store the energy consumption, for each season (axis = 0),
# each appliance (axis = 1) and household (axis = 2)
energy_stor = np.zeros((n_seasons, n_apps, n_hh))

# Creating a 4d-array where to store the load profiles for the random sample households (axis = 0)
# for each season (axis = 1), each time-step (axis = 2) and type of day (axis = 3)
lp_samp_stor = np.zeros((n_samp, n_seasons, n_time_sim, n_days))


## Evaluating the load profiles for the households, using the methods created, for each season and type of day
tic()

# Running through the seasons using a for loop
for season in seasons:

    # Season ID number and nickname to be used in the following
    ss = seasons[season][0]
    season_nickname = seasons[season][1]
    
    # Initializing a vector that accounts for the seasonal energy consumption from each household, from each appliance
    energy_season = np.zeros((n_apps, n_hh))

    # Running through the day-types using a for loop
    for day in days:
        
        # Day-type ID number and nickname to be used in the following
        dd = days[day][0]
        day_nickname = days[day][1]
        
        ## Generating the load profile (lp) for all the households, 
        # according to the availability of each appliance in the household
        
        # A 2d-array is initalized, containing the load profile in time (axis = 0) for each household (axis = 1)
        households_lp = np.zeros((n_time_sim, n_hh)) 

        # A 2d-array is initialized, containing the energy consumed in one day by each appliance (axis = 0) for each household (axis = 1)
        apps_energy = np.zeros((n_apps, n_hh)) 
        

        # The house_load_profiler routine is applied to each household
        tic()

        for household in range(0, n_hh):
            households_lp[:, household], apps_energy[:, household] = hlp(apps_availability[:, household], day_nickname, season_nickname, appliances_data, **params)
                                
        message = '\nLoad profiles evaluated in: {0:.3f} s ({1},{2}).'.format(toc(), season, day)
        print(message)


        ## Aggregating the load profiles and storing the results
    
        # Aggregating the load profiles with a different timestep
        aggr_households_lp = agr(households_lp, dt_aggr)

        # Evaluating the sum of all the load profiles, for each time-step
        aggregate_lp = np.sum(aggr_households_lp, axis = 1) 

        # Evaluating the  the average load profile, for each time-step
        average_lp = aggregate_lp/n_hh

        # Sorting the values of the power from all the households in an increasing way, for each time-step
        sorted_lp = np.sort(aggr_households_lp, axis = 1) 
        
        # Evaluating the maximum, medium and minimum load profiles (quantile), for each time-step
        quantile_lp_max = sorted_lp[:, nmax]
        quantile_lp_med = sorted_lp[:, nmed]
        quantile_lp_min = sorted_lp[:, nmin]

        # Evaluating and storing the random sample load profiles for the current season and day-type
        lp_samp_stor[:, ss, :, dd] = households_lp[:, samp].transpose()
        sample_lp_header += ['{}, {}'.format(season, day)]*n_samp

        # Saving all the load profiles in the proper array for the current season and day-type
        lp_tot_stor[ss, :, dd] = aggregate_lp
        lp_avg_stor[ss, :, dd] = aggregate_lp/n_hh
        lp_max_stor[ss, :, dd] = quantile_lp_max
        lp_med_stor[ss, :, dd] = quantile_lp_med
        lp_min_stor[ss, :, dd] = quantile_lp_min
        

        ## Evaluating the energy consumed by the appliances in the current season for all the days of the current day-type
        n_days_season = days_distr[season][day]
        energy_stor[ss, :, :] += apps_energy*n_days_season

message = '\nSimulation completed in {0:.3f} s.\n'.format(toc())
print(message)


### Saving the results as .csv files

# Creating an /Output folder, if not already existing
dirname = 'Output'

try: Path.mkdir(basepath / dirname)
except Exception: pass

# Creating an /Output/Files folder, if not already existing
subdirname = 'Files'

try: Path.mkdir(basepath / dirname / subdirname)
except Exception: pass

message = '\nThe results are ready and are now being saved in {}/{}.\n'.format(dirname, subdirname)
print(message)  

# Creating a subfolder, if not already existing
subsubdirname = '{}_{}_{}'.format(location, en_class, n_hh)

try: Path.mkdir(basepath / dirname / subdirname / subsubdirname)
except Exception: pass


## Running through the seasons and the day-types
# Storing the load profiles and energy consumptions as .csv files
tic() 

for season in seasons:
    ss = seasons[season][0]

    for day in days:
        dd = days[day][0]
        day_nickname = days[day][1]

        # Saving the total, average, maximum, medium, minimum (i.e. quantile) load profiles in a .csv file
        filename = '{}_{}_{}_{}_{}_lps_aggr.csv'.format(location, en_class, n_hh, season, day_nickname)
        fpath = basepath / dirname / subdirname / subsubdirname
            
        with open(fpath / filename, mode = 'w', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ';', quotechar = "'", quoting = csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(['Time (min)', 'Total load (W)', 'Average load (W)', 'Maximum load (W)','Medium load (W)','Minimum load (W)'])

            for ii in range(np.size(time_aggr)):
                csv_writer.writerow([time_aggr[ii], lp_tot_stor[ss, ii, dd], lp_avg_stor[ss, ii, dd], lp_max_stor[ss, ii, dd], lp_med_stor[ss, ii, dd], lp_min_stor[ss, ii, dd]])


        # Saving the random sample load profiles in a file, after giving a different time-step
        filename = '{}_{}_{}_{}_{}_lps_sample.csv'.format(location, en_class, n_hh, season, day_nickname)
        fpath = basepath / dirname / subdirname / subsubdirname

        with open(fpath / filename, mode = 'w', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ';', quotechar = "'", quoting = csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(sample_lp_header)

            for ii in range(np.size(time_sim)):
                csv_writer.writerow([time_sim[ii]] + list(lp_samp_stor[:, ss, ii, dd]))
               
                # csv_writer.writerow([time_sim[ii]] + list(sample_lp[ii,:]))


    # Saving the energy consumed by the appliances in each household, for each season
    filename = '{}_{}_{}_{}_energy.csv'.format(location, en_class, n_hh, season)
    fpath = basepath / dirname / subdirname / subsubdirname
    
    with open(fpath / filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['App_name', 'App_nickname'] + list(range(0,n_hh)))
    
        for app in apps_ID:
            csv_writer.writerow([app,apps_ID[app][1]]+list(energy_stor[ss, apps_ID[app][0], :]))   

message = 'Results saved in .csv files in {0:.3f}s.\n'.format(toc())
print(message)


### Post-processing of the results
dirname = 'Output'

# Creating an /Output/Figures folder, if not already existing
subdirname = 'Figures'

message = '\nThe results are now being plotted, figures are saved in {}/{}.\n'.format(dirname, subdirname)
print(message)  

try: Path.mkdir(basepath / dirname / subdirname)
except Exception: pass

# Creating a subfolder, if not already existing
subsubdirname = '{}_{}_{}'.format(location, en_class, n_hh)

try: Path.mkdir(basepath / dirname / subdirname / subsubdirname)
except Exception: pass


## Running through the seasons and calling the methods in plot_generator to create figures to be saved
tic()
for season in seasons:

    ss = seasons[season][0]

    # Total load profiles       
    plot_specs = {
    0: ['bar', 'Total'],
    }

    powers = lp_tot_stor[np.newaxis, ss, :, :]
                        
    fig = plot.seasonal_load_profiles(time_aggr, powers, plot_specs, season)

    filename = '{}_{}_{}_{}_aggr_loadprof.png'.format(location, en_class, season, n_hh)
    fpath = basepath / dirname / subdirname / subsubdirname
    
    fig.savefig(fpath / filename) 

    # Average load profile and quantiles
    plot_specs = {
    0: ['plot', 'Average'],
    1: ['bar', 'Max'],
    2: ['bar', 'Med'],
    3: ['bar', 'Min']
    }

    powers = np.stack((lp_avg_stor[ss, :, :],
                    lp_max_stor[ss, :, :],
                    lp_med_stor[ss, :, :],
                    lp_min_stor[ss, :, :]),
                    axis = 0)

    fig = plot.seasonal_load_profiles(time_aggr, powers, plot_specs, season)

    filename = '{}_{}_{}_{}_avg_quant_loadprof.png'.format(location, en_class, season, n_hh)
    fpath = basepath / dirname / subdirname / subsubdirname
    
    fig.savefig(fpath / filename)

    # Random sample load profiles
    plot_specs = {}
    for ii in range(n_samp):
        plot_specs[ii] = ['plot','Household: {}'.format(samp[ii])]

    powers = lp_samp_stor[:, ss, :, :]

    fig = plot.seasonal_load_profiles(time_sim, powers, plot_specs, season)

    filename = '{}_{}_{}_{}_sample_loadprof.png'.format(location, en_class, season, n_hh)
    fpath = basepath / dirname / subdirname / subsubdirname
    
    fig.savefig(fpath / filename)

# Total energy consumption by season
energies = np.transpose(np.sum(energy_stor, axis = 2))

plot_specs = {
    'heights': 'Total',
    'labels': 'appliances',
}

fig = plot.seasonal_energy(apps_ID, energies, plot_specs)

filename = '{}_{}_{}_season_tot_energy_apps.png'.format(location, en_class, n_hh)
fpath = basepath / dirname / subdirname / subsubdirname

fig.savefig(fpath / filename)

# Yearly total energy consumption
energies = np.sum(energies, axis = 1)
fig = plot.yearly_energy(apps_ID, energies, plot_specs)

filename = '{}_{}_{}_year_tot_energy_apps.png'.format(location, en_class, n_hh)
fpath = basepath / dirname / subdirname / subsubdirname

fig.savefig(fpath / filename)

# Yearly average energy consumption
energies_nan = np.sum(energy_stor, axis = 0)
energies_nan[energies_nan == 0] = np.nan

energies = np.nanmean(energies_nan, axis = 1)

plot_specs = {
    'heights': 'Average',
    'labels': 'appliances',
}

fig = plot.yearly_energy(apps_ID, energies, plot_specs)

filename = '{}_{}_{}_year_avg_energy_apps.png'.format(location, en_class, n_hh)
fpath = basepath / dirname / subdirname / subsubdirname

fig.savefig(fpath / filename)

# Percentage over total energy consumption
energies_perc = np.transpose(np.sum(energy_stor, axis = 2))
energies_perc = energies_perc/np.sum(energies_perc)*100

fig = plot.seasonal_energy_pie(apps_ID, energies_perc)
filename = '{}_{}_{}_season_perc_energy_apps.png'.format(location, en_class, n_hh)
fpath = basepath / dirname / subdirname / subsubdirname

fig.savefig(fpath / filename)


# # The appliances are now divided into classes of appliances, according to the
# # class specified in apps_ID in the position corresponding to "class" in apps_attr
# apps_classes = {}
# ii = 0


# for app in apps_ID:


    
#     if apps_ID[app][list(apps_attr.keys())[list(apps_attr.values()).index('class')] - 1] not in apps_classes: 
#         apps_classes[apps_ID[app][list(apps_attr.keys())[list(apps_attr.values()).index('class')] - 1]] = ii
#         ii += 1

# print(apps_classes)

# energy_class_stor = np.zeros((n_seasons, len(apps_classes), n_hh))

# for season in seasons:
#     ss = seasons[season][0]
#     for app_class in apps_classes:
    
#         apps_list=[]
#         for app in apps_ID:
#             if apps_ID[app][5] == app_class: apps_list.append(apps_ID[app][0])
    

#     energy_class_stor[ss, apps_classes[app_class], :] = np.sum(energy_stor[ss, apps_list, :], axis = 1)

# print(apps_classes)
# print(energy_class_stor.shape)
    





message = 'Results plotted and figures saved in {0:.3f}s.\n'.format(toc())
print(message)


message = '\nEnd.\nTotal time: {0:.3f} .\n'.format(toc())
print(message)