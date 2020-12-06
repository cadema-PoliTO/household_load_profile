# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:09:48 2020

@author: giamm
"""

from pathlib import Path
import csv
import datareader

##############################################################################


# This file is used to let the user enter the input parameters from keyboard.
# If a value is not given by the user, a default value is assigned.


##############################################################################

# The base path is saved in the variable basepath, it is used to move among
# directories to find the files that need to be read.
basepath = Path(__file__).parent

# A /Parameters folder is created in order to store the parameters as .csv files
dirname = 'Parameters'

try: Path.mkdir(basepath / dirname)
except Exception: pass 


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
quantile_curr = [quantile_min, quantile_med, quantile_max]

# Plotting parameters that can be changed
time_scale = 'min' #time-scale for plotting: 'min' | 'h' 
power_scale = 'W' #power_scale for plotting: 'W' | 'kW'
energy_scale = 'Wh' #energy_scale for plotting: 'Wh' | 'kWh' | 'MWh' 


########### Parameters update 

# Simulation parameters
varname,varval = datareader.read_param('sim_param.csv',';','Parameters')
for ii in range(len(varname)):
    vars()[varname[ii]] = varval[ii]
    # print(str(varname[ii]) +': ' + str(varval[ii]))
    
# Aggregation parameters
varname,varval = datareader.read_param('aggr_param.csv',';','Parameters')
for ii in range(len(varname)):
    vars()[varname[ii]] = varval[ii]
    
# Plotting parameters
varname,varval = datareader.read_param('plot_param.csv',';','Parameters')
for ii in range(len(varname)):
    vars()[varname[ii]] = varval[ii]


########### Parameters update to user's input

def sim_param():
    
    sim_param_dict = {}
    
    message = '''\n\nThe simulation is going to start soon. Please, enter the 
    values for some simulation parameters that can be changed. 
    Press 'enter' to assign them their default values.\n'''
    print(message)


    message = '\nPlease, enter the total number of households to be considered - currently: %d\n' %(n_hh)
    n_hh_inp = input(message) #number of households (-)
    
    while True: 
        if n_hh_inp == '': n_hh_inp = n_hh; break
        try: n_hh_inp = int(n_hh_inp)
        except: n_hh_inp = input('Please, enter an integer: ');continue
        
        if n_hh_inp >= 1 and n_hh_inp <= 1000: break
        else: n_hh_inp = input('Please, enter an integer between 1 and 1000: ');continue
        
    sim_param_dict['n_hh'] = ('-' , n_hh_inp)

      
    message = '\nPlease, insert the average number of people per household - currently: %.1f\n' %(n_people_avg)
    n_people_avg_inp = input(message) #average number of members for each household (-)
    
    while True: 
        if n_people_avg_inp == '': n_people_avg_inp = n_people_avg; break
        try: n_people_avg_inp = float(n_people_avg_inp)
        except: n_people_avg_inp = input('Please, enter a number: ');continue
        
        if n_people_avg_inp >= 1.0 and n_people_avg_inp <= 10.0: break
        else: n_people_avg_inp = input('Please, enter a number between 1 and 10: ');continue
     
    sim_param_dict['n_people_avg'] = ('-' , n_people_avg_inp)
    
    
    message = '\nPlease, insert the average square footage of the households (m2) - currently: %.1f m2\n' %(ftg_avg)
    ftg_avg_inp = input(message) #average  square footage of each household (m2)
    
    while True: 
        if ftg_avg_inp == '': ftg_avg_inp = ftg_avg; break
        try: ftg_avg_inp = float(ftg_avg_inp)
        except: ftg_avg_inp = input('Please, enter a number: ');continue
        
        if ftg_avg_inp >= 1.0 and ftg_avg_inp <= 1000.0: break
        else: ftg_avg_inp = input('Please, enter a number between 1 and 1000: ');continue
     
    sim_param_dict['ftg_avg'] = ('m2' , ftg_avg_inp)
    
    
    message = '\nPlease, select the geographical location between \'north\', \'centre\', \'south\' - currently: %s \n' %(location)
    location_inp = input(message).lower().strip().strip("'").strip('"') #geographical location: 'north' | 'centre' | 'south'
    
    while True: 
        if location_inp == 'center': location_inp = 'centre'
        if location_inp == '': location_inp = location; break
            
        if location_inp == 'north' or location_inp == 'centre' or location_inp == 'south': break
        else: location_inp = input('Please, choose between \'north\', \'centre\', \'south\': ').lower().strip().strip("'").strip('"');continue
    
    sim_param_dict['location'] = ('/' , location_inp)
    
    
    message = '\nPlease, insert the maximum available power for each household (W) - currently: %.0f W\n' %(power_max)
    power_max_inp = input(message) #maximum power available from the grid (contractual power) (W)
    
    while True: 
        if power_max_inp == '': power_max_inp = power_max;break
        try: power_max_inp = float(power_max_inp)
        except: power_max_inp = input('Please, enter a number: ');continue
        
        if power_max_inp >= 1e3 and power_max_inp <= 1e4: break
        else: power_max_inp = input('Please, enter a number between 1e3 and 1e4: ');continue
    
    sim_param_dict['power_max'] = ('W' , power_max_inp)
    
    
    message = '\nPlease, select the energetic class of the appliances from \'A+++\' to \'D\' (or from 0 to 6)- currently: %s \n' %(en_class)
    en_class_inp = input(message).upper().strip().strip("'").strip('"') #energetic class of the appiances: 'A+++' | 'A++' | 'A+' | 'A' | 'B' | 'C' | 'D'
    
    en_class_dict = {'A+++':0,'A++':1,'A+':2,'A':3,'B':4,'C':5,'D':6}
    
    while True: 
        if en_class_inp == '': en_class_inp = en_class; break
        if en_class_inp in en_class_dict.keys(): break
        if int(en_class_inp) in en_class_dict.values(): en_class_inp = list(en_class_dict.keys())[list(en_class_dict.values()).index(int(en_class_inp))];break
        else: en_class_inp = input('Please, enter an energetic class from \'A+++\' to \'D\' (or from 0 to 6)').upper().strip().strip("'").strip('"');continue
    
    sim_param_dict['en_class'] = ('/' , en_class_inp)
    
    
    message = '''\n\nFor appliances which don\'t have a duty-cycle and do not belong to
    "continuous" type, the time in which they are siwtched on during 24h (T_on)
    is modified exctracting a random duration from a normal distribution
    (centred in T_on, with standard deviation equal to devsta), in a range
    defined by toll).\n'''
    print(message)
    
    message = '\nPlease, insert the value for the tollerance on the duration range (%%) - currently: %d %%\n' %(toll)
    toll_inp = input(message) #tollerance on total time in which the appliance is on (%); default value: 15%
    
    while True: 
        if toll_inp == '': toll_inp = toll;break
        try: toll_inp = int(toll_inp)
        except: toll_inp = input('Please, enter an integer: ');continue
        
        if toll_inp >= 0 and toll_inp <= 100: break
        else: toll_inp = input('Please, enter an integer between 0 and 100: ');continue
    
    sim_param_dict['toll'] = ('%' , toll_inp)
    
    
    message = '\nPlease, insert the value for the standard deviation on the durations distribution (min) - currently: %.1f min\n' %(devsta)
    devsta_inp = input(message) #standard deviation on total time in which the appliance is on (min); default value: 2 min
    
    while True: 
        if devsta_inp == '': devsta_inp = devsta;break
        try: devsta_inp = float(devsta_inp)
        except: devsta_inp = input('Please, enter a number: ');continue
        
        if devsta_inp >= 1.0 and devsta_inp <= 10.0: break
        else: devsta_inp = input('Please, enter a number between 1 and 10: ');continue
        
    sim_param_dict['devsta'] = ('min' , devsta_inp)
    
     
    filename = 'sim_param.csv'
    fpath = basepath / dirname 
    with open(fpath / filename , mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

        csv_writer.writerow(['Parameter name', 'Unit of measure' , 'Value'])
    
        for key in sim_param_dict:
            csv_writer.writerow([key , sim_param_dict[key][0] , sim_param_dict[key][1]])
    

##############################################################################

########## Results postprocessing parameters that can be changed

def aggr_param():
    
    aggr_param_dict = {}

    message = '''\n\nThe load profile from the electric appliances are evaluated 
    for each household. Then, the aggregated load profile is going to be evaluated
    by summing, for each time-interval, the power demand from all the households.
    Press 'enter' to assign them their default values.\n'''
    print(message)
    
    
    message = '\nThe load profiles are evaluated with a 1 min timestep. Anyway, the\
        final results can be aggregated with a different timestep.\n'
    print(message)
    
    message = '\nPlease, select a timestep for the aggregation of the final results (min)\
        - currently: %d min\n' %(dt_aggr)
    dt_aggr_inp = input(message) #aggregated data timestep (min)
    
    dt_aggr_list = [1,5,10,15,20,30,45,60]
    
    while True: 
        if dt_aggr_inp == '': dt_aggr_inp = dt_aggr; break
        try: dt_aggr_inp = int(dt_aggr_inp)
        except: dt_aggr_inp = input('Please, enter an integer: ');continue
        
        if dt_aggr_inp in dt_aggr_list: break
        else: dt_aggr_inp = input('Please, choose a value in [1,5,10,15,20,30,45,60]: ');continue
    
    aggr_param_dict['dt_aggr'] = ('min' , dt_aggr_inp)
    
    
    message = '\nThe minimum, medium and maximum power demands are evaluated as quantile.\n'
    print(message)
    
    message = '''\nPlease, insert the quantile to be used for evaluating minimum, medium
    and maximum power demands in the load profiles - currently: %d - %d - %d %%\n''' %(quantile_curr[0],quantile_curr[1],quantile_curr[2])
    print(message)
    
    quantile = []
    for ii in range(len(quantile_curr)):
        
        if ii == 0: message = 'Minimum: '
        elif ii == 1: message = 'Medium: '
        else: message = 'Maximum: '
        quantile.append(input(message)) #quantile for the evaluation of minimum, medium and maximux power demands for the load profiles
    
        while True: 
            if quantile[ii] == '': quantile[ii] = quantile_curr[ii];break
            try: quantile[ii] = int(quantile[ii])
            except: quantile[ii] = input('Please, enter an integer: ');continue
            
            
            if quantile[ii] >= 0 and quantile[ii] <= 100: break
            else: quantile[ii] = input('Please, enter an integer between 0 and 100: ');continue
            
    quantile.sort()
    
    quantile_min = quantile[0]
    quantile_med = quantile[1]
    quantile_max = quantile[2]
           
    aggr_param_dict['quantile_min'] = ('%' , quantile_min)
    aggr_param_dict['quantile_med'] = ('%' , quantile_med)
    aggr_param_dict['quantile_max'] = ('%' , quantile_max)
    
    filename = 'aggr_param.csv'
    fpath = basepath / dirname 
    with open(fpath / filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

        csv_writer.writerow(['Parameter name', 'Unit of measure' , 'Value'])
    
        for key in aggr_param_dict:
            csv_writer.writerow([key , aggr_param_dict[key][0] , aggr_param_dict[key][1]])
    

##############################################################################

########## Plotting parameters that can be changed

def plot_param():
    
    plot_param_dict = {}
    
    message = '''\n\nPlease, enter some plotting paramters that can be changed.
    Press 'enter' to assign them their default values.\n'''
    print(message)
    
    
    message = '\nThe time-scale can be changed.'
    print(message)
    
    message = 'Please, select the time-scale to be used in the graphs, choose between \'min\' and \'h\' - currently: %s \n' %(time_scale)
    time_scale_inp = input(message).lower().strip().strip("'").strip('"') #time-scale for plotting: 'min' | 'h' 
    
    while True: 
        if time_scale_inp == '': time_scale_inp = time_scale;break
            
        if time_scale_inp == 'min' or time_scale_inp == 'h': break
        else: time_scale_inp = input('Please, choose between \'min\' and \'h\': ').lower().strip().strip("'").strip('"');continue
    
    plot_param_dict['time_scale'] = ('/' , time_scale_inp)
    
    
    message = '\nThe power-scale can be changed.'
    print(message)
    
    message = 'Please, select the power-scale to be used in the graphs, choose between \'W\' and \'kW\' - currently: %s \n' %(power_scale)
    power_scale_inp = input(message).upper().strip().strip("'").strip('"') #power_scale for plotting: 'W' | 'kW' 
    
    while True: 
        if power_scale_inp == '': power_scale_inp = power_scale; break
        if power_scale_inp == 'KW': power_scale_inp = 'kW';break
            
        if power_scale_inp == 'W' or power_scale_inp == 'kW': break
        else: power_scale_inp = input('Please, choose between \'W\' and \'kW\': ').upper().strip().strip("'").strip('"');continue
    
    plot_param_dict['power_scale'] = ('/' , power_scale_inp)
    
    
    message = '\nThe energy-scale can be changed.'
    print(message)
    
    message = 'Please, select the energy-scale to be used in the graphs, choose between \'Wh\', \'kWh\' and \'MWh\' - currently: %s \n' %(energy_scale)
    energy_scale_inp = input(message).lower().strip().strip("'").strip('"') #energy_scale for plotting: 'Wh' | 'kWh' | 'MWh' 
    
    while True: 
        if energy_scale_inp == '': energy_scale_inp = energy_scale; break
        if energy_scale_inp == 'wh': energy_scale_inp = 'Wh';break
        elif energy_scale_inp == 'kwh': energy_scale_inp = 'kWh';break
        elif energy_scale_inp == 'mwh': energy_scale_inp = 'MWh';break
            
        if energy_scale_inp == 'Wh' or energy_scale_inp == 'kWh' or energy_scale_inp == 'MWh': break
        else: energy_scale_inp = input('Please, choose between choose between \'Wh\', \'kWh\' and \'MWh\': ').upper().strip().strip("'").strip('"');continue
        
    plot_param_dict['energy_scale'] = ('/' , energy_scale_inp)
    
    filename = 'plot_param.csv'
    fpath = basepath / dirname 
    with open(fpath / filename , mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

        csv_writer.writerow(['Parameter name', 'Unit of measure' , 'Value'])
    
        for key in plot_param_dict:
            csv_writer.writerow([key , plot_param_dict[key][0] , plot_param_dict[key][1]])