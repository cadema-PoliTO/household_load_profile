# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:09:48 2020

@author: giamm
"""

from pathlib import Path
import csv
import datareader
from levenshtein_distance import Leven_dist_comparison

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


# ########## Parameters

# # Simulation parameters that can be changed
# n_hh = 100 #number of households (-)
# n_people_avg = 2.7 #average number of members for each household (-)
# ftg_avg = 100  #average footage of each household (m2)
# location = 'north' #geographical location: 'north' | 'centre' | 'south'
# power_max = 3000 #maximum power available from the grid (contractual power) (W)
# en_class = 'A+' #energetic class of the appiances: 'A+++' | 'A++' | 'A+' | 'A' | 'B' | 'C' | 'D'

# # For appliances which don't have a duty-cycle and do not belong to "continuous"
# # type, the time in which they are siwtched on during 24h (T_on) is modified
# # exctracting a random duration from a normal distribution (centred in T_on, with
# # standard deviation equal to devsta), in a range defined by toll
# toll = 15 #tollerance on total time in which the appliance is on (%); default value: 15%
# devsta = 2 #standard deviation on total time in which the appliance is on (min); default value: 2 min

# # Aggregation parameters that can be changed
# dt_aggr = 15 #aggregated data timestep (min) 1 | 5 | 10 | 15 | 10 | 30 | 45 | 60
# quantile_min, quantile_med, quantile_max = 15,50,85 #quantils for the evaluation of minimum, medium and maximux power demands for the load profiles
# quantile_curr = [quantile_min, quantile_med, quantile_max]

# # Plotting parameters that can be changed
# time_scale = 'min' #time-scale for plotting: 'min' | 'h' 
# power_scale = 'W' #power_scale for plotting: 'W' | 'kW'
# energy_scale = 'Wh' #energy_scale for plotting: 'Wh' | 'kWh' | 'MWh' 


## Creating a method to change the parameters entering their values from keyboard
# All the parameters that can be changed are declared as keys of param_dict, while
# the value for each key contains the type (int, float, str) of the parameter, its
# defualt value and its boundaries/possible values and its unit of measure (the latter
# is just to be written in the .csv file where the parameters will be saved).
# The current values of the parameters are read from a .csv file that has been 
# created previously and given as values in a dictionary. If the file does not exist yet,
# default values are applied.
# The user is then asked if there is any change desired in the parameters' values.

def parameters_input():

    # Creating a dictionary that contains all the parameters, their type, default values, etc.
    param_dict = {
        'n_hh': {'type': int, 'default_val': 100, 'min_val': 1, 'max_val': 10000, 'uom': '(households)'},
        'toll': {'type': int, 'default_val': 15., 'min_val': 0., 'max_val': 100, 'uom': '(min)'},
        'devsta': {'type': int, 'default_val': 2, 'min_val': 1, 'max_val': 100, 'uom': '(min)'},
        'q_max': {'type': int, 'default_val': 85, 'min_val': 1, 'max_val': 100, 'uom': '(%)'},
        'q_med': {'type': int, 'default_val': 50, 'min_val': 1, 'max_val': 100, 'uom': '(%)'},
        'q_min': {'type': int, 'default_val': 15, 'min_val': 1, 'max_val': 100, 'uom': '(%)'},
        'dt_aggr':{'type': int, 'default_val': 60, 'possible_values': [5, 10, 15, 20, 30, 45, 60], 'uom': '(min)'},
        'n_people_avg': {'type': float, 'default_val': 2.7, 'min_val': 1., 'max_val': 10., 'uom': '(people/household)'},
        'ftg_avg': {'type': float, 'default_val': 100., 'min_val': 10., 'max_val': 1000., 'uom': '(m2)'},
        'power_max': {'type': float, 'default_val': 3000., 'min_val': 1000., 'max_val': 10000., 'uom': '(W)'},
        'location': {'type': str, 'default_val': 'north', 'possible_values': ['north', 'south', 'centre'], 'uom': '(/)'},
        'en_class': {'type': str, 'default_val': 'A+', 'possible_values': ['A+++', 'A++', 'A+', 'A', 'B', 'C', 'D'], 'uom': '(/)'},
        'time_scale': {'type': str, 'default_val': 'h', 'possible_values': ['min', 'h'], 'uom': '(/)'},
        'power_scale': {'type': str, 'default_val': 'kW', 'possible_values': ['W', 'kW', 'MW'], 'uom': '(/)'},
        'energy_scale': {'type': str, 'default_val': 'MWh', 'possible_values': ['Wh', 'kWh', 'MWh'], 'uom': '(/)'},
        }

    # Creating a list that contains all the parameters names (usefull for the inputs from keyboard)
    param_list = list(param_dict.keys())

    # Creating a list of possible commands that will stop the execution of the code
    stop_commands = ['', 'stop', 'done', 'no', 'none']

    # The current values for the parameters a re read from the file parameters.csv. If it does not exist yet
    # default values are assigned to the parameters
    params = datareader.read_param('parameters', ';', 'Input')

    if not bool(params):
        for param in param_dict: params[param] = param_dict[param]['default_val']

    # Printing the current values for the parameters
    message = 'The parameters for the simulation are currently set as follows\n'
    print(message)

    for param in params: print('{}: {}'.format(param, params[param]))

    # Starting the procedure for updating the values of the parameters
    while True:

        # Asking for a command-line input in order to change a parameter's value
        param_change = input('\nWould you like to change any parameter(write the whole expression)?: ')

        # Exiting the loop if a "stop-command" is given
        if param_change.lower().strip() in stop_commands: break

        # Finding the equality sign in the expression entered by the user, in order to
        # divide the parameter's name from the value

        index = param_change.find('=')
        param_name = param_change[:index].lower().strip("',.=\" ")
        param_val = param_change[index + 1:].lower().strip("',.=\" ")

        # Assessing if the parameter's name entered by the user is in the parameter's list;
        # otherwise the Leven_dist_comparison method is used to suggest the closest match 
        count = 0
        count_max = 3
        while param_name not in param_list and count < count_max:
            options = Leven_dist_comparison(param_name, param_list)
            
            if len(options) == 1: message = 'Do you mean {}? (rewrite the name): '.format(options[0])
            else : message = 'Do you mean {}? (rewrite the name): '.format(('? Or ').join(options))
            
            param_name = input(message)

            if param_name.lower().strip() in stop_commands: break
            count += 1

        if param_name.lower().strip() in stop_commands: break
        elif param_name not in param_list: continue


        # After identifying the parameter that is going to be changed, the value entered by the user
        # is checked to be consistent with the possible values the parameter can assume
        if param_dict[param_name]['type'] == int:

            while True: 
                if param_val.lower().strip() in stop_commands: param_val = param_dict[param_name]['default_val']; break

                try: param_val = int(param_val)
                except: param_val = input('Please, enter an integer value for {}: '.format(param_name)); continue
                
                if 'possible_values' not in param_dict[param_name]:
                    
                    low_lim = param_dict[param_name]['min_val']
                    up_lim = param_dict[param_name]['max_val']

                    if param_val >= low_lim and param_val <= up_lim: break
                    else: param_val = input('Please, enter an integer between {} and {}: '.format(low_lim, up_lim)); continue

        
                else:
                    
                    possible_values = param_dict[param_name]['possible_values']
                
                    if param_val in possible_values: break
                    else: param_val = input('Please, enter an integer in {}: '.format(possible_values)); continue
       
        elif param_dict[param_name]['type'] == float:

            low_lim = param_dict[param_name]['min_val']
            up_lim = param_dict[param_name]['max_val']
        
            while True: 
                if param_val.lower().strip() in stop_commands: param_val = param_dict[param_name]['default_val']; break

                try: param_val = float(param_val)
                except: param_val = input('Please, enter a number: '); continue
                
                if param_val >= low_lim and param_val <= up_lim: break
                else: param_val = input('Please, enter a number between {} and {}: '.format(low_lim, up_lim)); continue
   
        elif param_dict[param_name]['type'] == str:

            possible_values = param_dict[param_name]['possible_values']
            
            possible_values_low = []
            for value in possible_values: possible_values_low.append(value.lower())
            
            while True: 
                
                if param_val.lower().strip() in stop_commands: param_val = param_dict[param_name]['default_val']; break
        
                if param_val.lower().strip() in possible_values_low: param_val = possible_values[possible_values_low.index(param_val.lower().strip())]; break
                else: param_val = input('Please, choose between {}: '.format(possible_values)); continue
            
        # Updating the parameter's value
        params[param_name] = param_val

    # Storing the parameters (updated) in a .csv file
    filename = 'parameters.csv'
    fpath = basepath / dirname 
    with open(fpath / filename , mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)

        csv_writer.writerow(['Name', 'Value', 'Unit of measure'])

        for param in params:
            csv_writer.writerow([param , params[param], param_dict[param]['uom']])

    # Returning a dictionary with the updated values for the parameters
    return(params)
    