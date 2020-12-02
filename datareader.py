# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 10:45:12 2020

@author: giamm
"""

import os
from pathlib import Path
import numpy as np
import csv
import math


##############################################################################

# This scripted is used to create methods that properly read files


##############################################################################

# The base path is saved in the variable basepath, it is used to move among
# directories to find the files that need to be read.
basepath = os.path.dirname(os.path.abspath(__file__))

def read_param(filename,delimit,dirname):
    
    ''' The function reads from a .csv file in which some paramters are saved. 
    The file has the parameter's name in the first column, its unit of measure 
    in the second one and its value in the third one.
        
    Inputs:
        filname - string containing the name of the file (extension of the file: .dat)
        delimit - string containing the delimiting element
        
    Outputs:
        data - 2d-array containing the values in the file'
    '''
    
    dirname = dirname.strip()
    if not dirname.startswith('\\'): dirname = '\\' + dirname
    if not dirname.endswith('\\'): dirname = dirname + '\\'

    filename = filename.strip()
    if not filename.endswith('.csv'): filename = filename + '.csv'
    
    fname = basepath + dirname + filename 
    
    varname_list = []
    varval_list = []
    
    try:
        with open(fname, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=delimit,quotechar="'")
            next(csv_reader, None) 
            
            for row in csv_reader:
                varname_list.append(row[0])
                
                try: row[2] = int(row[2])
                except: 
                    try: row[2] = float(row[2])
                    except: row[2] = row[2]
                    
                varval_list.append(row[2])
                
    except:
        
        print('Unable to open this file')
     
    return(varname_list,varval_list)

##############################################################################

# if True:
#     filename = 'loadprof_lux_wde_w'
#     delimit = ';'
#     dirname = 'Input'
    
def read_general(filename,delimit,dirname):
    
    ''' The function reads from a .csv file in which the header is a single row
        
    
    Inputs:
        filname - string containing the name of the file (extension of the file: .dat)
        delimit - string containing the delimiting element
        
    Outputs:
        data - 2d-array containing the values in the file'
    '''
    
    dirname = dirname.strip()
    if not dirname.startswith('\\'): dirname = '\\' + dirname
    if not dirname.endswith('\\'): dirname = dirname + '\\'

    filename = filename.strip()
    if not filename.endswith('.csv'): filename = filename + '.csv'
    
    fname = basepath + dirname + filename 
    
    data_list=[]
    
    try:
        with open(fname, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=delimit)
            next(csv_reader, None) 
            for row in csv_reader:
                
                data_list.append(row)              
                
    except:
        
        print('Unable to open this file')
    
    # Creating a 2D-array containing the data(time in the first column and power in the second one)
    data = np.array(data_list,dtype='float')
    return(data)

##############################################################################

def read_appliances(filename,delimit,dirname):
    
    ''' The function reads from a .csv file that contains all the appliances
    
    Inputs:
        filname - string containing the name of the file (extension of the file: .dat)
        delimit - string containing the delimiting element
        
    Outputs:
        app - 2D-array containing, for each appliance, its attributes' values
        app_ID - dictionary containing for ID (key) the related appliance's name'
        app_attributes - dictionary containing for each attribute (columns in app) its description and unit of measure
    '''
    
    dirname = dirname.strip()
    if not dirname.startswith('\\'): dirname = '\\' + dirname
    if not dirname.endswith('\\'): dirname = dirname + '\\'

    filename = filename.strip()
    if not filename.endswith('.csv'): filename = filename + '.csv'
    
    fname = basepath + dirname + filename 
    
    app_list = [] #list containing, for each appliance,its attributes 
    app_ID = {} #dictionary relating each appliance to an identification number, nickname and type
    
    # Reading the CSV file
    with open(fname, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=delimit)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header = row;
                line_count += 1
                continue
            
            else:
                app_list.append(row[7:])
                app_ID[row[1].lower()]=(int(row[0]),row[2],row[3],row[4].split(','),row[5].split(','),row[6])
            
            line_count += 1
    
    # Creating a dictionary for attributes
    app_attributes = {}
    ii = 0;
    
    for attr in header:
        app_attributes[int(ii)] = attr.lower()
        ii += 1
    
    # Creating a 2D-array containing appliances and attributes
    app = np.array(app_list,dtype='float')
    return(app,app_ID,app_attributes)

##############################################################################

def read_enclasses(filename,delimit,dirname):
    
    ''' The function reads from a .csv file that contains, for each appliance, its yearly energy consumption (kWh/year) for every energetic class
    
    Inputs:
        filname - string containing the name of the file (extension of the file: .dat)
        delimit - string containing the delimiting element
        
    Outputs:
        enclass_en - 2D-array containing, for each appliance (rows), and for each energetic class (columns) the yearly energy consumption (kWh/year)
        enclass_levels - dictionary containing for each energetic class (columns in app) its level 
    '''
    
    apps_ID,apps_attributes = read_appliances('eltdome_report' , ';' , '\Input')[1:]
    
    dirname = dirname.strip()
    if not dirname.startswith('\\'): dirname = '\\' + dirname
    if not dirname.endswith('\\'): dirname = dirname + '\\'

    filename = filename.strip()
    if not filename.endswith('.csv'): filename = filename + '.csv'
    
    fname = basepath + dirname + filename  
    
    enclass_list = [] #list containing, for each appliance,its nominal energy consumption 
        
    # Reading the CSV file
    with open(fname, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=delimit)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                columns=row;
                line_count += 1
                continue
            
            else:
                enclass_list.append([row[1].lower()]+(row[2:]))
                            
            line_count += 1
    
    enclass_ordered = [[-1]*len(enclass_list[0][2:])]*len(apps_ID)
    
    for item in enclass_list:
        app=item[0]
        enclass_ordered[apps_ID[app][0]]=item[2:]
    
    # Creating a dictionary for energetic classes' levels
    enclass_levels = {}
    ii = 0;
    
    for attr in columns[3:]:
        enclass_levels[int(ii)] = attr
        ii += 1
    
    # Creating a 2D-array containing appliances and nominal energy consumptions
    enclass_en = np.array(enclass_ordered,dtype='float') 
    return(enclass_en,enclass_levels)

##############################################################################

def read_energy(filename,delimit,dirname):
    
    ''' The function reads from a .csv file that contains, for each appliance, its yearly energy consumption (kWh/year) for every household.
    
    Inputs:
        filname - string containing the name of the file (extension of the file: .dat)
        delimit - string containing the delimiting element
        
    Outputs:
        enclass_en - 2D-array containing, for each appliance (rows), and for each energetic class (columns) the yearly energy consumption (kWh/year)
        enclass_levels - dictionary containing for each energetic class (columns in app) its level 
    '''
   
    dirname = dirname.strip()
    if not dirname.startswith('\\'): dirname = '\\' + dirname
    if not dirname.endswith('\\'): dirname = dirname + '\\'

    filename = filename.strip()
    if not filename.endswith('.csv'): filename = filename + '.csv'
    
    fname = basepath + dirname + filename 
    
    energy_list = [] #list containing, for each appliance,its nominal energy consumption 
        
    # Reading the CSV file
    with open(fname, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=delimit)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            
            else:
                energy_list.append(row[2:])
                            
            line_count += 1
    
    
    # Creating a 2D-array containing appliances and nominal energy consumptions
    energy = np.array(energy_list,dtype='float')     
    return(energy)

##############################################################################
