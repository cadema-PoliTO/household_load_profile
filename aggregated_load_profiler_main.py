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
import parameters_input as inp
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
  
########## Parameters

# Simulation parameters that can be changed

n_hh = 100 #number of households (-)
n_people_avg = 2.7 #average number of members for each household (-)
ftg_avg = 100  #average footage of each household (m2)
location = 'north' #geographical location: 'north' | 'centre' | 'south'
power_max = 3000 #maximum power available from the grid (contractual power) (W)
en_class = 'A+' #energetic class of the appiances: 'A+++' | 'A++' | 'A+' | 'A' | 'B' | 'C' | 'D'

# For appliances which don't have a duty-cycle and do not belong to "continuous"
# type, the time in which they are siwtched on during 24h (T_on) is modified
# exctracting a random duration from a normal distribution (centred in T_on, with
# standard deviation equal to devsta), in a range defined by toll
toll = 15 #tollerance on total time in which the appliance is on (%); default value: 15%
devsta = 2 #standard deviation on total time in which the appliance is on (min); default value: 2 min

# Aggregation parameters that can be changed

dt_aggr = 15 #aggregated data timestep (min) 1 | 5 | 10 | 15 | 10 | 30 | 45 | 60
quantile_min, quantile_med, quantile_max = 15,50,85 #quantils for the evaluation of minimum, medium and maximux power demands for the load profiles

# Plotting parameters that can be changed

time_scale = 'min' #time-scale for plotting: 'min' | 'h' 
power_scale = 'W' #power_scale for plotting: 'W' | 'kW'
energy_scale = 'Wh' #energy_scale for plotting: 'Wh' | 'kWh' | 'MWh' 

########### Parameters update 

message = 'The parameters for the simulation are set to:\n'
print(message)

message = '\nSimulation parameters'
print(message)

varname, varval = datareader.read_param('sim_param.csv',';','Parameters')
for name, val in zip(varname, varval):
    vars()[name] = val
    print(str(name) +': ' + str(val))
    
message = '\nAggregation parameters'
print(message)
    
varname, varval = datareader.read_param('aggr_param.csv',';','Parameters')
for name, val in zip(varname, varval):
    vars()[name] = val
    print(str(name) +': ' + str(val))
    
message = '\nPlotting parameters'
print(message)
    
varname, varval = datareader.read_param('plot_param.csv',';','Parameters')
for name, val in zip(varname, varval):
    vars()[name] = val
    print(str(name) +': ' + str(val))

# ########### Parameters update to user's input

# possibleanswers_yes = ['yes','y','sì','si','s']

# message = 'Would you like to change any parameters?\nPress \'enter\' to skip: '
# flag = input(message).lower().strip()
# if flag in possibleanswers_yes: 

#     message = 'Would you like to change the simulation parameters?\nPress \'enter\' to skip: '
#     flag = input(message).lower().strip()
#     if flag in possibleanswers_yes: 
#         inp.sim_param()
#         varname,varval = datareader.read_param('sim_param.csv',';')
#         for ii in range(len(varname)):
#             vars()[varname[ii]] = varval[ii]
    
         
#     message = 'Would you like to change the aggregation parameters?\nPress \'enter\' to skip: '
#     flag = input(message).lower().strip()
#     if flag in possibleanswers_yes: 
#         inp.aggr_param()
#         varname,varval = datareader.read_param('aggr_param.csv',';')
#         for ii in range(len(varname)):
#             vars()[varname[ii]] = varval[ii]
        
      
#     message = 'Would you like to change the plotting parameters?\nPress \'enter\' to skip: '
#     flag = input(message).lower().strip()
#     if flag in possibleanswers_yes: 
#         inp.plot_param()
#         varname,varval = datareader.read_param('plot_param.csv',';')
#         for ii in range(len(varname)):
#             vars()[varname[ii]] = varval[ii]


message = '\nThank you, the simulation is now starting.\n'
print(message)


########## Time discretization

dt = 1 #timestep of the simulation (min)
time = 1440 #total time of simulation (min)
time_sim = np.arange(0,time,dt) #time vector of the simulation (min)

time_aggr = np.arange(0,time,dt_aggr) #time vector for the aggregation of the results (min)


##########  Loading appliances list and attributes
    
apps,apps_ID,apps_attr = datareader.read_appliances('eltdome_report.csv',';','Input')
# apps is a 2d-array in which, for each appliance (rows) and attribute value is given (columns)
# apps_ID is a dictionary in which, for each appliance (key), its ID number,type,week and seasonal behavior (value)
# apps_attr is a dictionary in which the name of each attribute (value) is linked to its columns number in apps (key)

appliances = {
    'apps': apps,
    'apps_ID': apps_ID,
    'apps_attr': apps_attr,
    }

ec_yearly_energy, ec_levels_dict = datareader.read_enclasses('classenerg_report.csv',';','Input')
energy_classes = {
    'ec_yearly_energy': ec_yearly_energy,
    'ec_levels_dict': ec_levels_dict,
    }

coeff_matrix, seasons_dict = datareader.read_enclasses('coeff_matrix.csv',';','Input')
season_coefficients = {
    'coeff_matrix': coeff_matrix,
    'seasons_dict': seasons_dict,
    }


########## Building the appliances availability matrix

# A 2d-array is built in which, for each household (columns) it is
# shown which appliances are available for the household, according to the 
# distribution factor of each appliance in a given location (1 if available, 0 otherwise)
apps_availability = np.zeros((len(apps_ID),n_hh))

# A dictionary that relates each location (key) to the related columns in apps(for distribution factors)
location_dict = dict({'north':0,'centre':1,'south':2})

# The appliances availability matrix is now built
for app in apps_ID:
    
    distr_fact = apps[apps_ID[app][0], #first index: ID number of the appliance
                location_dict[location]] #second index: position of the attribute in apps
                
    n_apps_app_type=int(np.round(n_hh*distr_fact)) #number of households in which the appliance is available        
    samp = random.sample(list(range(0,n_hh)),n_apps_app_type) #a random sample is extracted from the total number of households
    
    apps_availability[apps_ID[app][0],samp] = 1 #the appliance's' availability is assigned to the households present in the sample


########## Building seasons and week dictionaries 

# This is done in order to explore all the seasons and, for each season two 
# types of days (weekday and weekend)

seasons = dict({'winter':(0,'w'),'summer':(1,'s'),'spring':(2,'ap'),'autumn':(3,'ap')})
days = dict({'week-day':(0,'wd'),'weekend-day':(1,'we')})

#  A reference year is considered, in which the first day (01/01) is a monday. 
# Therefore, conventionally considering that winter lasts from 21/12 to 20/03, 
# spring from 21/03 to 20/06, summer from 21/06 to 20/09 and winter from 21/09
# to 20/12, each seasons has got the following number of weekdays and weekend days.
days_distr = {'winter':{'week-day':64,'weekend-day':26},
             'spring':{'week-day':66,'weekend-day':26},
             'summer':{'week-day':66,'weekend-day':26},
             'autumn':{'week-day':65,'weekend-day':26}
             }


######### Evaluating the load profiles

# Quantile are evaluated for the load profiles. It means that for each timestep
# the maximum power (demanded by less than 15% of the households), the median
# power (demanded by less than 50% of the households) and the minimum (demanded 7
# by less than 85% of the households).
nmin = int(np.round(n_hh*quantile_min/100)) 
nmed = int(np.round(n_hh*quantile_med/100))
nmax = int(np.round(n_hh*quantile_max/100))

# The aggregated load profiles are evaluated for both a week day and a weekend
# day for the four seasons and the seasonal energy consumption from each 
# appliance, for each household are evaluated.

# A random sample of n_samp houses is also extracted in order to plot, for each 
# of them, the load profile during one day for each season, for each day-type.
n_samp = 5
samp = random.sample(list(range(0,n_hh)),n_samp) #A random sample is extracted from the total number of households
# sample_lp = np.zeros((time,n_samp*len(seasons)*len(days))) #The load profiles for the houses in the sample are stored in a proper array
# sample_slicingaux = np.arange(n_samp) #This array is useful for properly slicing the households_lp array and storing the load profiles of the households in the random sample
sample_lp_header = [] #list where to store the header for the .csv file



n_days = len(days)
n_seasons = len(seasons)
n_time_aggr = np.size(time_aggr)
n_apps = len(apps_ID)

load_profiles_types = {
    0: 'Total',
    1: 'Average',
    2: 'Maximum',
    3: 'Medium',
    4: 'Minimum',
    }
n_lps = len(load_profiles_types)

lp_tot_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_avg_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_max_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_med_stor = np.zeros((n_seasons, n_time_aggr, n_days))
lp_min_stor = np.zeros((n_seasons, n_time_aggr, n_days))
energy_stor = np.zeros((n_seasons, n_apps, n_hh))


lp_samp_stor = np.zeros((n_samp, n_seasons, len(time_sim), n_days))


tic()
for season in seasons:

    season_nickname = seasons[season][1]
    ss = seasons[season][0]

    # The energy consumption from all the apps is stored for each season.
    energy_season = np.zeros((len(apps_ID), n_hh))

    # seasonal_avg_quant_lps = np.zeros((len(time_aggr), 4*len(days)))
    # seasonal_tot_lps = np.zeros((len(time_aggr), len(days)))

    for day in days:
        
        day_nickname = days[day][1]
        dd = days[day][0]
        
        ########## The load profile (lp) is generated for all the households, according
        # to the availability of each appliance in the household
        
        households_lp = np.zeros((time, n_hh)) # 2d-array containing the load profile in time (rows) for each household (columns)
        apps_energy = np.zeros((len(apps_ID), n_hh)) # 2d-array containing the energy consumed in one day by each appliance (rows) for each household (columns)
        
        tic()
        # The house_load_profiler routine is applied to each household
        for household in range(0,n_hh):
            
            households_lp[:,household], apps_energy[:,household] = hlp(apps_availability[:, household], day_nickname, season_nickname, appliances, energy_classes, season_coefficients)
            #(W)                      #(Wh/day)
        
        message = '\nLoad profiles evaluated in: {0:.3f} s ({1},{2}).'.format(toc(), season, day)
        print(message)


        ########## Load aggregation and processing of the results
        
        # The load profile is aggregated with a different timestep
        aggr_households_lp = agr(households_lp, dt_aggr)
        
        # Load profiles and quantile
        aggregate_lp = np.sum(aggr_households_lp, axis = 1) #1d-array containing the sum of all the load profiles in time
        average_lp = aggregate_lp/n_hh
        sorted_lp = np.sort(aggr_households_lp, axis = 1) #for each timestep, the values of the power from each households are sorted in an increasing way
        
        quantile_lp_min = sorted_lp[:, nmin]
        quantile_lp_med = sorted_lp[:, nmed]
        quantile_lp_max = sorted_lp[:, nmax]

        # Random sample load profiles
        
        lp_samp_stor[:, ss, :, dd] = households_lp[:, samp].transpose()
        # sample_lp[:, sample_slicingaux + (ss + dd + ss)*n_samp] = households_lp[:, samp]
        sample_lp_header += ['{}, {}'.format(season, day)]*n_samp

        # Saving load profiles and quantile in a file, for each day for each season
        lp_tot_stor[ss, :, dd] = aggregate_lp
        lp_avg_stor[ss, :, dd] = aggregate_lp/n_hh
        lp_max_stor[ss, :, dd] = quantile_lp_max
        lp_med_stor[ss, :, dd] = quantile_lp_med
        lp_min_stor[ss, :, dd] = quantile_lp_min
        

        ########## Energy consumed by the appliances
        n_days_season = days_distr[season][day]
        energy_stor[ss, :, :] += apps_energy*n_days_season

message = '\nSimulation completed in {0:.3f} s.\n'.format(toc())
print(message)


## Saving the results as .csv files
dirname = 'Output'

try: Path.mkdir(basepath / dirname)
except Exception: pass

subdirname = 'Files'

try: Path.mkdir(basepath / dirname / subdirname)
except Exception: pass

message = '\nThe results are ready and are now being saved in {}/{}.\n'.format(dirname, subdirname)
print(message)  

subsubdirname = '{}_{}_{}'.format(location, en_class, n_hh)

try: Path.mkdir(basepath / dirname / subdirname / subsubdirname)
except Exception: pass

tic()
# Running through the seasons to store the load profiles and energy consumptions as .csv files
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





## Post-processing of the results
dirname = 'Output'
subdirname = 'Figures'

message = '\nThe results are now being plotted, figures are saved in {}/{}.\n'.format(dirname, subdirname)
print(message)  

try: Path.mkdir(basepath / dirname / subdirname)
except Exception: pass

subsubdirname = '{}_{}_{}'.format(location, en_class, n_hh)

try: Path.mkdir(basepath / dirname / subdirname / subsubdirname)
except Exception: pass

tic()
# Running through the seasons and calling the methods in plot_generator to create figures to be saved
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



# Total energy by season
energies = np.transpose(np.sum(energy_stor, axis = 2))


plot_specs = {
    'heights': 'Total',
    'labels': 'appliances',
}
fig = plot.seasonal_energy(apps_ID, energies, plot_specs)

filename = '{}_{}_{}_season_tot_energy_apps.png'.format(location, en_class, n_hh)
fpath = basepath / dirname / subdirname / subsubdirname

fig.savefig(fpath / filename)

energies = np.sum(energies, axis = 1)
fig = plot.yearly_energy(apps_ID, energies, plot_specs)

filename = '{}_{}_{}_year_tot_energy_apps.png'.format(location, en_class, n_hh)
fpath = basepath / dirname / subdirname / subsubdirname

fig.savefig(fpath / filename)



# Average energy consumption
plot_specs = {
    'heights': 'Average',
    'labels': 'appliances',
}

energies_nan = np.sum(energy_stor, axis = 0)
energies_nan[energies_nan == 0] = np.nan

energies = np.nanmean(energies_nan, axis = 1)

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