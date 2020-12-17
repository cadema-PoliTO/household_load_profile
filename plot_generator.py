# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:35:26 2020

@author: giamm
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import random
import math

import datareader

###############################################################################


# This script is used to plot the results from the simulation


###############################################################################

# The basepath of the file is stored in a variable 
basepath = Path(__file__).parent

# An /Output/Figures folder is created in order to store the graphs as .png files
 

dirname = 'Output'
subdirname = 'Figures'

try: Path.mkdir(basepath / dirname / subdirname)
except Exception: pass 


########## Input parameters 

# Simulation parameters that can be changed
n_hh = 100 #number of households (-)
n_people_avg = 2.7 #average number of members for each household (-)
ftg_avg = 100  #average footage of each household (m2)
location = 'north' #geographical location: 'north' | 'centre' | 'south'
power_max = 3000 #maximum power available from the grid (contractual power) (W)
en_class = 'A+' #energetic class of the appiances: 'A+++' | 'A++' | 'A+' | 'A' | 'B' | 'C' | 'D'

# Aggregation parameters
quantile_min, quantile_med, quantile_max = 15,50,85 #quantile for the evaluation of minimum, medium and maximux power demands for the load profiles
dt_aggr = 15 # timestep for the aggregation of the results (min)

# Plotting parameters
time_scale = 'h'
power_scale = 'kW'
energy_scale = 'MWh'


########### Parameter update to user's input

varname, varval = datareader.read_param('sim_param.csv',';','Parameters')
for name, val in zip(varname, varval):
    vars()[name] = val
    
varname, varval = datareader.read_param('aggr_param.csv',';','Parameters')
for name, val in zip(varname, varval):
    vars()[name] = val
    
varname, varval = datareader.read_param('plot_param.csv',';','Parameters')
for name, val in zip(varname, varval):
    vars()[name] = val


########## Scale setting

ts_dict = {'min':1/1,'h':1/60}
ps_dict = {'W':1/1,'kW':1/1e3}
es_dict = {'Wh':1/1,'kWh':1/1e3,'MWh':1/1e6}

# ts = ts_dict[time_scale]
# ps = ps_dict[power_scale]
# es = es_dict[energy_scale]


########## Time discretization, adjusting values to time-scale

# dt = 1*ts #timestep of the simulation (min)
# time = 1440*ts #total time of simulation (min)

# dt_aggr = dt_aggr*ts #aggregated data timestep (min)


##########  Loading appliances list and attributes
    
apps,apps_ID,apps_attr = datareader.read_appliances('eltdome_report.csv',';','Input')
# apps is a 2d-array in which, for each appliance (rows) and attribute value is given (columns)
# apps_ID is a dictionary in which, for each appliance (key), its ID number,type,week and seasonal behavior (value)
# apps_attr is a dictionary in which the name of each attribute (value) is linked to its columns number in apps (key)

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


########## Creating a list of different colors

colors = [(230, 25, 75),
        (60, 180, 75),
        (255, 225, 25),
        (0, 130, 200),
        (245, 130, 48),
        (145, 30, 180),
        (70, 240, 240),
        (240, 50, 230),
        (210, 245, 60),
        (250, 190, 212),
        (0, 128, 128),
        (220, 190, 255),
        (170, 110, 40),
        (255, 250, 200),
        (128, 0, 0),
        (170, 255, 195),
        (128, 128, 0),
        (255, 215, 180),
        (0, 0, 128),
        (128, 128, 128)]

colors_rgb = []
for color in colors:
    color_rgb = []
    for value in color:
        color_rgb.append(float(value)/255) 
    colors_rgb.append(tuple(color_rgb))


########## Sheetsizes in inches

mm2inch = 1/25.4
sheetsizes = {'a3' : (297*mm2inch,420*mm2inch), #inch
            'a4' : (210*mm2inch,297*mm2inch), #inch
            'a5' : (148.5*mm2inch,210*mm2inch) #inch
            }

######### Fontsizes

fontsizes_dict = {'small':(8,10,12),
                  'medium':(10,12,14),
                  'large':(14,16,18)}


# ########## Plotting the load profiles

# sheetsize = 'a3'
# orientation = 'horizontal'
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]


# for season in seasons:
#     ss = seasons[season][0]
    
#     # A figure with multiple subplots is created, with as many rows as the seasons,
#     # for each row there two columns (for week-days and weekend-days)
#     fig1, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
    
#     title = '\nAggregated load profiles during one day \nfor %d households with %s energetic class in the %s of Italy' %(n_hh,en_class,location.capitalize())
#     fig1.suptitle(title, fontsize=fontsize_title , fontweight = 'bold')
#     fig1.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
    
#     ymax = 0
#     ymin = 0
    
#     for day in days:
        
#         dd = days[day][0]
        
#         filename = 'aggr_lp' + '_' + season + '_' + days[day][1] + '_' + str(n_hh) + '_' + en_class + '_' + location
#         data = datareader.read_general(filename,';','Output')
#         time_aggr = data[:,0]*ts #adjusted to the selected time-scale
#         lp_aggr = data[:,1]*ps #adjusted to the selected power-scale
        
#         if np.max(lp_aggr) >= ymax: ymax = np.max(lp_aggr)
#         if np.min(lp_aggr) <= ymin: ymin = np.min(lp_aggr)
        
#         leg = season.capitalize() + ', ' + day
#         ax[dd].bar(time_aggr,lp_aggr,width=dt_aggr,align='edge',label=leg)
#         ax[dd].set_title(leg, fontsize=fontsize_title)
        
        
#     for axi in ax.flatten():
#         axi.set_xlabel('Time [' + time_scale + ']', fontsize=fontsize_labels)
#         axi.set_ylabel('Power [' + power_scale + ']', fontsize=fontsize_labels)
#         axi.set_xlim([0,time])
#         axi.set_ylim([0.9*ymin,1.1*ymax])
#         axi.set_xticks(list(time_aggr[::int(60*ts/dt_aggr)]))
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()
        
#     fig1.subplots_adjust(wspace=0.2)
    
#     filename = 'aggr_loadprof_' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
#     fpath = basepath / dirname / subdirname
#     fig1.savefig(fpath / filename)
    
    
# ########## Plotting the load profile quantile

# sheetsize = 'a3'
# orientation = 'horizontal'
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]
# fontsize_pielab = fontsizes_dict[font][-3]


# for season in seasons:
#     ss = seasons[season][0]
    
#     # A figure with multiple subplots is created, with as many rows as the seasons,
#     # for each row there two columns (for week-days and weekend-days)
#     fig2, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
    
#     title = '\nAverage load profile and quantile during one day \nfor %d households with %s energetic class in the %s of Italy' %(n_hh,en_class,location.capitalize())
#     fig2.suptitle(title, fontsize=fontsize_title , fontweight = 'bold')
#     fig2.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
    
#     ymax = 0
#     ymin = 0
    
#     for day in days:
#         dd = days[day][0]
        
#         filename = 'aggr_lp' + '_' + season + '_' + days[day][1] + '_' + str(n_hh) + '_' + en_class + '_' + location
#         data = datareader.read_general(filename,';','Output')
#         time_aggr = data[:,0]*ts #adjusted to the selected time-scale
#         lp_aggr = data[:,1]*ps #adjusted to the selected power-scale
#         lp_avg = lp_aggr/n_hh #average load profile
#         lp_min = data[:,2]*ps #adjusted to the selected power-scale
#         lp_med = data[:,3]*ps #adjusted to the selected power-scale
#         lp_max = data[:,4]*ps #adjusted to the selected power-scale
        
#         if np.max(lp_max) >= ymax: ymax = np.max(lp_max)
#         if np.min(lp_min) <= ymin: ymin = np.min(lp_min)
        
#         leg = season.capitalize() + ', ' + day
#         ax[dd].plot(time_aggr + dt_aggr/2,lp_avg,'rs-',label='Average')
#         ax[dd].bar(time_aggr,lp_max,width=dt_aggr,align='edge',label=str(quantile_max)+'%')
#         ax[dd].bar(time_aggr,lp_med,width=dt_aggr,align='edge',label=str(quantile_med)+'%')
#         ax[dd].bar(time_aggr,lp_min,width=dt_aggr,align='edge',label=str(quantile_min)+'%')
        
#         ax[dd].set_title(leg, fontsize=fontsize_title)
        
        
#     for axi in ax.flatten():
#         axi.set_xlabel('Time [' + time_scale + ']', fontsize=fontsize_labels)
#         axi.set_ylabel('Power [' + power_scale + ']', fontsize=fontsize_labels)
#         axi.set_xlim([0,time])
#         axi.set_ylim([0.9*ymin,1.1*ymax])
#         axi.set_xticks(list(time_aggr[::int(60*ts/dt_aggr)])) #one tick each hour
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()
#         axi.legend(loc='upper left',fontsize=fontsize_legend, ncol = 2)
    
#     filename = 'avg_quant_loadprof_' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
#     fname = basepath / dirname / subdirname
#     fig2.savefig(fpath / filename)
    
    
# ########## Total energy consumption from classes of appliances for season

# # First, the energy consumptions from the various appliances aggregated into
# # energy consumptions from classes of appliances, in order to improve the 
# # readability of the charts. THe class of the various appliances is defined
# # in the apps_ID dictionary.

# energy_w = datareader.read_energy('energy_winter' + '_' + str(n_hh) + '_' + en_class + '_' + location + '.csv',';','Output') #(Wh/year)
# energy_p = datareader.read_energy('energy_spring' + '_' + str(n_hh) + '_' + en_class + '_' + location + '.csv',';','Output')
# energy_s = datareader.read_energy('energy_summer' + '_' + str(n_hh) + '_' + en_class + '_' + location + '.csv',';','Output')
# energy_a = datareader.read_energy('energy_autumn' + '_' + str(n_hh) + '_' + en_class + '_' + location + '.csv',';','Output')

# energy_w_tot = np.sum(energy_w,axis=1)*es #adjusted to the energy scale
# energy_p_tot = np.sum(energy_p,axis=1)*es
# energy_s_tot = np.sum(energy_s,axis=1)*es
# energy_a_tot = np.sum(energy_a,axis=1)*es

# apps_classes = {}
# ii = 0
# for app in apps_ID:
#     if apps_ID[app][5] not in apps_classes: 
#         apps_classes[apps_ID[app][5]] = (ii , colors_rgb[ii] )
#         ii += 1

# energy_w_tot_class = np.zeros(len(apps_classes))
# energy_p_tot_class = np.zeros(len(apps_classes))
# energy_s_tot_class = np.zeros(len(apps_classes))
# energy_a_tot_class = np.zeros(len(apps_classes))

# for app_class in apps_classes:
    
#     apps_list=[]
#     for app in apps_ID:
#         if apps_ID[app][5] == app_class:apps_list.append(apps_ID[app][0])
    
#     energy_w_tot_class[apps_classes[app_class][0]] = np.sum(energy_w_tot[apps_list])
#     energy_p_tot_class[apps_classes[app_class][0]] = np.sum(energy_p_tot[apps_list])
#     energy_s_tot_class[apps_classes[app_class][0]] = np.sum(energy_s_tot[apps_list])
#     energy_a_tot_class[apps_classes[app_class][0]] = np.sum(energy_a_tot[apps_list]) 
    

# # The total energy consumption from the classes of appliances is represented

# sheetsize = 'a3'
# orientation = 'horizontal'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]
# fontsize_pielab = fontsizes_dict[font][-3]

# fig3, ax = plt.subplots(figsize=figsize)
# title = '\nTotal energy consumption from classes of appliances by season\n for %d households with %s energetic class in the %s of Italy' % (n_hh,en_class,location.capitalize())
# fig3.suptitle(title, fontsize =fontsize_title , fontweight = 'bold')
# fig3.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.88, wspace=None, hspace=0.3)

# labels = []
# for apps_class in apps_classes.keys(): labels.append(apps_class.capitalize().replace('_',' '))

# bottoms = np.zeros(len(labels))

# leg = []

# ymax = 0
# text_coord = 0,ymax
# text_toadd = ''

# text_toadd = 'Energy consumption by season\n'
# for season in seasons:
    
#     if season == 'winter': heights = energy_w_tot_class
#     elif season == 'spring': heights = energy_p_tot_class
#     elif season == 'summer': heights = energy_s_tot_class
#     elif season == 'autumn': heights = energy_a_tot_class
    
#     ax.bar(labels,heights,bottom=bottoms)
#     bottoms = bottoms + heights
    
#     if np.max(bottoms) > ymax: ymax = np.max(bottoms)
    
#     leg.append(season.capitalize())
    
#     text_coord = 0,ymax
#     text_toadd = text_toadd + '\n%s: %.3f %s\n' % (season.capitalize(),np.sum(heights),energy_scale) 


# ax.set_ylim([0,1.1*ymax])

# ax.set_ylabel('Energy consumption [' + energy_scale + '/year]', fontsize=fontsize_labels)
# ax.tick_params(axis='both',labelsize=fontsize_labels)
# ax.tick_params(axis='x',labelrotation=45)
# ax.grid(axis='y')

# ax.legend(leg,loc='upper left',ncol=len(seasons),fontsize=fontsize_legend)

# props = dict(boxstyle='square', facecolor=colors_rgb[2], pad = 0.3, alpha=0.5)                     
# ax.text(0.02, 0.9, text_toadd.rstrip(), fontsize=fontsize_text, ha='left', va='top', transform=ax.transAxes ,bbox=props)


# filename = 'total_en_classes__' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
# fpath = basepath / dirname / subdirname
# fig3.savefig(fpath / filename)

  
# ##### The percentage of total energy consumption from the classes of appliances is 
# # represented in a pie chart. One for each seasons
# # The figure is given the size of a sheet of paper (a5, a4, a3)

# sheetsize = 'a3'
# orientation = 'horizontal'
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]
# fontsize_pielab = fontsizes_dict[font][-3]

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fig4, ax = plt.subplots(2,2,figsize=figsize)
# title = '\nPercentage of total energy consumption from classes of appliances by season\n for %d households with %s energetic class in the %s of Italy' % (n_hh,en_class,location.capitalize())
# fig4.suptitle(title, fontsize = fontsize_title , fontweight = 'bold')
# fig4.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.88, wspace=None, hspace=0.1)

# subpl_row = 0
# subpl_col = 0

# for season in seasons:
    
#     labels = []
#     sizes = []
    
#     if season == 'winter': energy_season_tot = energy_w_tot_class
#     elif season == 'spring': energy_season_tot = energy_p_tot_class
#     elif season == 'summer': energy_season_tot = energy_s_tot_class
#     elif season == 'autumn': energy_season_tot = energy_a_tot_class
    
#     if subpl_col > 1: 
#         subpl_row = 1
#         subpl_col = 0

#     tot = np.sum(energy_season_tot)
#     energy_season_perc = energy_season_tot / tot * 100
    
#     for apps_class in apps_classes: 
#           if energy_season_perc[apps_classes[apps_class][0]] > 0: labels.append(apps_class.capitalize().replace('_',' '))
    
#     sizes = list(energy_season_perc[energy_season_perc > 0])
    
#     colors = []
#     for label in labels: colors.append(apps_classes[label.lower().replace(' ','_')][1])
            
#     ax[subpl_row,subpl_col].pie(sizes, autopct='%1.1f%%', pctdistance=0.6, radius=0.8, frame=True, colors = colors , startangle=60, textprops={'fontsize':fontsize_pielab})
#     ax[subpl_row,subpl_col].legend(labels)
#     ax[subpl_row,subpl_col].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
#     ax[subpl_row,subpl_col].set_title(season.capitalize(), loc='left', pad = 0.5, fontsize=fontsize_legend, fontweight='bold')
#     ax[subpl_row,subpl_col].set_xticks([])
#     ax[subpl_row,subpl_col].set_yticks([])
    
#     subpl_col += 1
 
# filename = 'perc_en_classes__' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
# fpath = basepath / dirname / subdirname
# fig4.savefig(fpath / filename)
         
    
# ########## Total and average yearly energy consumption from appliances

# # First the yearly energy consumption from each appliance is analized in 
# # absolute terms.

# energy = datareader.read_energy('energy_winter' + '_' + str(n_hh) + '_' + en_class + '_' + location + '.csv',';','Output') #(Wh/year)

# for season in seasons:
#     if season == 'winter': continue

#     filename = 'energy' + '_' + season + '_' +str(n_hh) + '_' + en_class + '_' + location + '.csv'
#     energy +=  datareader.read_energy(filename,';','Output') #(Wh/year)
    
# energy_tot = np.sum(energy,axis=1)*es #summed for all the appliances and adjusted to the energy-scale
    
    
# # The total energy consumption from the  appliances is represented

# sheetsize = 'a3'
# orientation = 'horizontal'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]

# fig5, ax = plt.subplots(figsize=figsize)
# title = '\nTotal energy consumption from the appliances in a year\n for %d households with %s energetic class in the %s of Italy' %(n_hh,en_class,location.capitalize())
# fig5.suptitle(title, fontsize = fontsize_title , fontweight = 'bold')
# fig5.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.88, wspace=None, hspace=0.3)

# labels_notsort =[]
# for app in apps_ID: labels_notsort.append(app.capitalize().replace('_',' '))
# heights = energy_tot

# heights_sortind = np.argsort(heights)
# heights = heights[heights_sortind]

# labels = labels_notsort.copy()
# for ii in range(len(labels)): labels[ii] = labels_notsort[heights_sortind[ii]]

# ax.bar(labels,heights) 
# ax.set_ylabel('Energy consumption [' + energy_scale + '/year]', fontsize=fontsize_labels)
# ax.set_ylim([0,1.1*np.max(heights)])
# ax.tick_params(axis='both',labelsize=fontsize_labels)
# ax.tick_params(axis='x',rotation=70)
# ax.grid(axis='y')

# for index, value in enumerate(heights):
#     plt.text(index, 1.01*value, '%.f' %(value),ha='center',va='bottom',rotation=0,fontsize=fontsize_text)

# total_energy = np.sum(energy_tot)
# text_toadd = 'Total energy consumption\n %.3f %s/year' % (total_energy,energy_scale)
# props = dict(boxstyle='square', facecolor=colors_rgb[2], pad = 0.3, alpha = 0.5)                     
# ax.text(0.02, 0.95, text_toadd, fontsize=fontsize_text, ha='left', va='top', transform=ax.transAxes ,bbox=props)

# energy_perc = energy_tot/total_energy * 100
# heights = np.sort(energy_perc)

# ax_tw = ax.twinx()
# ax_tw.plot(labels,heights,'rs')
# ax_tw.set_ylabel('Energy consumption [%]',fontsize=fontsize_labels)
# ax_tw.yaxis.label.set_color('r')
# ax_tw.set_ylim([0,1.1*np.max(heights)])

# ax_tw.spines['right'].set_color('r')
# ax_tw.tick_params(axis='y', colors='r',labelsize=fontsize_labels)


# filename = 'total_en_apps__' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
# fpath = basepath / dirname / subdirname
# fig5.savefig(fpath / filename)

   
# ##### Rather than analyzing the results in absolute terms, they are now analyzed
# # for each appliance. Therefore, the average energy consumption from 
# # each appliance needs to take into account the total number of appliances.
# # In order to do that, nanmean is exploited (substituting 0 values with nan)

# energy = datareader.read_energy('energy_winter' + '_' + str(n_hh)+ '_' + en_class + '_' + location + '.csv',';','Output') #(Wh/year)

# for season in seasons:
#     if season == 'winter': continue

#     filename = 'energy' + '_' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.csv'
#     energy +=  datareader.read_energy(filename,';','Output') #(Wh/year)
    
# energy[energy == 0] = np.nan
# energy_avg = np.nanmean(energy,axis=1)*es #averaged and adjusted to the energy-scale

# # The average energy consumption from the  appliances is represented

# sheetsize = 'a3'
# orientation = 'horizontal'
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]


# fig6, ax = plt.subplots(figsize=figsize)
# title = '\nAverage energy consumption from the appliances in a year with %s energetic class' %(en_class)
# fig6.suptitle(title, fontsize = fontsize_title , fontweight = 'bold')
# fig6.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9, wspace=None, hspace=0.3)

# labels_notsort =[]
# for app in apps_ID: labels_notsort.append(app.capitalize().replace('_',' '))

# heights = energy_avg
# heights_sortind = np.argsort(heights)
# heights = heights[heights_sortind]

# labels = labels_notsort.copy()
# for ii in range(len(labels)): labels[ii] = labels_notsort[heights_sortind[ii]]

# ax.bar(labels,heights) 
# ax.set_ylabel('Energy consumption [' + energy_scale + '/year]', fontsize=fontsize_labels)
# ax.set_ylim([0,1.1*np.max(heights)])
# ax.tick_params(axis='both', labelsize=fontsize_labels, pad=15)
# ax.tick_params(axis='x',rotation=70)
# ax.grid(axis='y')

# for index, value in enumerate(heights):
#     plt.text(index, 1.01*value, '%.3f' %(value),ha='center',va='bottom',rotation=70,fontsize=fontsize_text)


# filename = 'avg_en_apps__' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
# fpath = basepath / dirname / subdirname
# fig6.savefig(fpath / filename)





# ########## Plotting the average load profiles in order to compare them in different seasons

# sheetsize = 'a3'
# orientation = 'horizontal'
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]
# fontsize_pielab = fontsizes_dict[font][-3]

# fig7, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
# title = '\nAverage load profiles during one day \nfor %d households with %s energetic class in the %s of Italy' %(n_hh,en_class,location.capitalize())
# fig7.suptitle(title, fontsize=fontsize_title , fontweight = 'bold')
# fig7.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)

# ymax = 0
# ymin = 0

# for day in days:
#     dd = days[day][0]

#     for season in seasons:
#         ss = seasons[season][0]
   
#         filename = 'aggr_lp' + '_' + season + '_' + days[day][1] + '_' + str(n_hh) + '_' + en_class + '_' + location
#         data = datareader.read_general(filename,';','Output')
#         time_aggr = data[:,0]*ts #adjusted to the selected time-scale
#         lp_aggr = data[:,1]*ps #adjusted to the selected power-scale
#         lp_avg = lp_aggr/n_hh #average load profile
#         # lp_min = data[:,2]*ps #adjusted to the selected power-scale
#         # lp_med = data[:,3]*ps #adjusted to the selected power-scale
#         # lp_max = data[:,4]*ps #adjusted to the selected power-scale
        
#         if np.max(lp_max) >= ymax: ymax = np.max(lp_max)
#         if np.min(lp_min) <= ymin: ymin = np.min(lp_min)

#         ax[dd].plot(time_aggr + dt_aggr/2,lp_avg, color = colors_rgb[ss], linestyle='-', marker = 's', label=season)
#         # ax[dd].bar(time_aggr,lp_max,width=dt_aggr,align='edge',label=str(quantile_max)+'%')
#         # ax[dd].bar(time_aggr,lp_med,width=dt_aggr,align='edge',label=str(quantile_med)+'%')
#         # ax[dd].bar(time_aggr,lp_min,width=dt_aggr,align='edge',label=str(quantile_min)+'%')
        
#     leg = day.capitalize()
#     ax[dd].set_title(leg, fontsize=fontsize_title)
     
# for axi in ax.flatten():
#     axi.set_xlabel('Time [' + time_scale + ']', fontsize=fontsize_labels)
#     axi.set_ylabel('Power [' + power_scale + ']', fontsize=fontsize_labels)
#     axi.set_xlim([0,time])
#     axi.set_ylim([0.9*ymin,1.1*ymax])
#     axi.set_xticks(list(time_aggr[::int(60*ts/dt_aggr)])) #one tick each hour
#     axi.tick_params(axis='both',labelsize=fontsize_labels)
#     axi.tick_params(axis='x',labelrotation=0)
#     axi.grid()
#     axi.legend(loc='upper left',fontsize=fontsize_legend, ncol = 2)
    
#     filename = 'avg_loadprof_comparison' + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
#     fname = basepath / dirname / subdirname
#     fig7.savefig(fpath / filename)



# ########## Plotting the random sample load profiles

# sheetsize = 'a3'
# orientation = 'horizontal'
# font = 'large'

# figsize = sheetsizes[sheetsize]
# if orientation == 'horizontal': figsize = figsize[::-1]

# fontsize_title = fontsizes_dict[font][-1]
# fontsize_legend = fontsizes_dict[font][-1]
# fontsize_labels = fontsizes_dict[font][-2]
# fontsize_text = fontsizes_dict[font][-2]
# fontsize_pielab = fontsizes_dict[font][-3]


# filename = 'randomsample_lp' + '_' + str(n_hh) + '_' + en_class + '_' + location
# data = datareader.read_general(filename,';','Output')
    
# time_plot = data[:,0]*ts #adjusted to the selected time-scale

# #One columns is not taken into account since it contains the time vector, the remaining columns 
# # are divided by the total number of days in order to get the size of the random sample (in terms of households)
# n_samp = int((np.size(data, axis=1) - 1)/(len(seasons)*len(days))) 
# sample_slicingaux = np.arange(n_samp) #This array is useful for properly slicing the data array

# for season in seasons:
#     ss = seasons[season][0]
    
#     # A figure with multiple subplots is created, with as many rows as the seasons,
#     # for each row there two columns (for week-days and weekend-days)
#     fig8, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
    
#     title = '\nRandom sample load profiles during one day \nfor %d households with %s energetic class in the %s of Italy' %(n_hh,en_class,location.capitalize())
#     fig8.suptitle(title, fontsize=fontsize_title , fontweight = 'bold')
#     fig8.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
    
#     ymax = 0
#     ymin = 0
    
#     for day in days:
#         dd = days[day][0]
        
#         start = 1 + (ss+dd+ss)*n_samp #index where to start slicing (in the first column there's the time vector)
#         randomsample_lp = data[: , start + sample_slicingaux]*ps #adjusted to the selected power-scale
       
#         if np.max(randomsample_lp) >= ymax: ymax = np.max(randomsample_lp)
#         if np.min(randomsample_lp) <= ymin: ymin = np.min(randomsample_lp)
        
#         leg = season.capitalize() + ', ' + day

#         for ii in range(n_samp):
#             ax[dd].plot(time_plot,randomsample_lp[:,ii], color=colors_rgb[ii])
        
#         ax[dd].set_title(leg, fontsize=fontsize_title)
        
        
#     for axi in ax.flatten():
#         axi.set_xlabel('Time [' + time_scale + ']', fontsize=fontsize_labels)
#         axi.set_ylabel('Power [' + power_scale + ']', fontsize=fontsize_labels)
#         axi.set_xlim([0,time])
#         axi.set_ylim([0.9*ymin,1.1*ymax])
#         axi.set_xticks(list(time_plot[::int(60*ts/dt)])) #one tick each hour
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()
    
#     filename = 'randomsample_loadprof_' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
#     fname = basepath / dirname / subdirname
#     fig8.savefig(fpath / filename)
    






########## Plotting the load profiles

# def aggr_load_profile(time, powers, season, **params):

#     #Default parameters
#     def_params = {
#     'time_scale': 'h',
#     'power_scale': 'kW',
#     'energy_scale': 'MWh',
#     'figsize': (297/25.4 , 420/25.4),
#     'orientation': 'horizontal',
#     'font_small': 14,
#     'font_medium': 16,
#     'font_large': 18,
#     }
    
#     # The parameters that are not specified when the function is called are set to the default value
#     for param in def_params: 
#         if param not in params: params[param] = def_params[param]

#     # Scales setup: factors needed to turn the values of time, power and energy in the correct scale
#     time_scale = params['time_scale']
#     power_scale = params['power_scale']
#     energy_scale = params['energy_scale']

#     ts = ts_dict[time_scale]
#     ps = ps_dict[power_scale]
#     es = es_dict[energy_scale]

#     # Time and power are adjusted to the proper scales
#     time = time*ts
#     powers = powers*ps

#     # Figure setup: figure size and orientatio, font-sizes 
#     figsize = params['figsize']
#     orientation = params['orientation']

#     if orientation == 'horizontal': figsize = figsize[::-1]

#     fontsize_title = params['font_large']
#     fontsize_legend = params['font_medium']
#     fontsize_labels = params['font_medium']
#     fontsize_text = params['font_medium']
#     fontsize_ticks = params['font_small']
        
#     # A figure with multiple subplots is created, with as many rows as the seasons,
#     # for each row there two columns (for week-days and weekend-days)
#     fig, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
        
#     suptitle = '\nAggregated load profiles during one day \nfor {} households with {} energetic class in the {} of Italy'.format(n_hh,en_class,location.capitalize())
#     fig.suptitle(suptitle, fontsize=fontsize_title , fontweight = 'bold')
#     fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
    
#     ymax = 0
#     ymin = 0

#     # Evaluating the time-step of the time-vector in order to set the bars' width
#     dt = (time[-1] - time[0])/np.size(time)
    
#     for day in days:

#         # Number corresponding to the type of day (0: week-day, 1: week-end -day)
#         dd = days[day][0] 

#         if np.max(powers[:,dd]) >= ymax: ymax = np.max(powers[:,dd])
#         if np.min(powers[:,dd]) <= ymin: ymin = np.min(powers[:,dd])
        

        
#         # Title of the subplot
#         title = season.capitalize() + ', ' + day
#         ax[dd].bar(time, powers[:,dd], width=dt, align='edge')
#         ax[dd].set_title(title, fontsize=fontsize_title)
        
    
#     for axi in ax.flatten():
#         axi.set_xlabel('Time [{}]'.format(time_scale), fontsize=fontsize_labels)
#         axi.set_ylabel('Power [{}]'.format(power_scale), fontsize=fontsize_labels)
#         axi.set_xlim([time[0],time[-1]])
#         axi.set_ylim([0.9*ymin,1.1*ymax])
#         # Set one tick each hour on the x-axis
#         axi.set_xticks(list(time[::int(60*ts/dt)]))
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()
        
#     fig.subplots_adjust(wspace=0.2)

#     return(fig)


# ########## Plotting the load profile quantile

# def load_profiles(time, powers, plot_specs, season, **params)



#    #Default parameters
#     def_params = {
#     'time_scale': 'h',
#     'power_scale': 'kW',
#     'energy_scale': 'MWh',
#     'figsize': (297/25.4 , 420/25.4),
#     'orientation': 'horizontal',
#     'font_small': 14,
#     'font_medium': 16,
#     'font_large': 18,
#     }
    
#     # The parameters that are not specified when the function is called are set to the default value
#     for param in def_params: 
#         if param not in params: params[param] = def_params[param]

#     # Scales setup: factors needed to turn the values of time, power and energy in the correct scale
#     time_scale = params['time_scale']
#     power_scale = params['power_scale']
#     energy_scale = params['energy_scale']

#     ts = ts_dict[time_scale]
#     ps = ps_dict[power_scale]
#     es = es_dict[energy_scale]

#     # Time and power are adjusted to the proper scales
#     time = time*ts
#     powers= powers*ps

#     # Figure setup: figure size and orientatio, font-sizes 
#     figsize = params['figsize']
#     orientation = params['orientation']

#     if orientation == 'horizontal': figsize = figsize[::-1]

#     fontsize_title = params['font_large']
#     fontsize_legend = params['font_medium']
#     fontsize_labels = params['font_medium']
#     fontsize_text = params['font_medium']
#     fontsize_ticks = params['font_small']
#     fontsize_pielabels = params['font_small']

    
#     # A figure with multiple subplots is created, with as many rows as the seasons,
#     # for each row there two columns (for week-days and weekend-days)
#     fig, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
    
#     suptitle = '\nAverage load profile and quantile during one day \nfor %d households with %s energetic class in the %s of Italy' %(n_hh,en_class,location.capitalize())
#     fig.suptitle(suptitle, fontsize=fontsize_title , fontweight = 'bold')
#     fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
    
  

#     # Evaluating the time-step of the time-vector in order to set the bars' width
#     dt = (time[-1] - time[0])/np.size(time)

    
#     # Evaluating the number of profiles passed to the function for each day-type 
#     # It is given for ganted that only two day-types are considered
#     n_lps =  int(np.size(powers, axis=1)/np.size(days))

#     #This array is useful for properly slicing the powers-array
#     powers_slicingaux = np.arange(n_lps) 
    
#     for day in days:

#         # Number corresponding to the type of day (0: week-day, 1: week-end -day)
#         dd = days[day][0] 
    

#         # Index needed for slicing the powers-array, according to the day of the week
#         start = dd*n_lps 

#         title = season.capitalize() + ', ' + day

#         for lp in range(n_lps):

#             if plot_specs[lp][0] == 'plot':
#             ax[dd].plot(time + dt/2, powers[:, start + lp], color  = colors[lp], linestyle = '-', label = plot_specs[lp][1])
 
#             elif plot_specs[lp][0] == 'bar':
#             ax[dd].bar(time, powers[:, start + lp], width=dt, align='edge', label= plot_specs[lp][1])

        
#         ax[dd].set_title(leg, fontsize=fontsize_title)
        
#       for axi in ax.flatten():
#         axi.set_xlabel('Time [{}]'.format(time_scale), fontsize=fontsize_labels)
#         axi.set_ylabel('Power [{}]'.format(power_scale), fontsize=fontsize_labels)
#         axi.set_xlim([time[0],time[-1]])
#         axi.set_ylim([0.9*ymin,1.1*ymax])
#         # Set one tick each hour on the x-axis
#         axi.set_xticks(list(time[::int(60*ts/dt)]))
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()

#     for axi in ax.flatten():
#         axi.set_xlabel('Time [' + time_scale + ']', fontsize=fontsize_labels)
#         axi.set_ylabel('Power [' + power_scale + ']', fontsize=fontsize_labels)
#         axi.set_xlim([time[0], time[-1]])
#         axi.set_ylim([0.9*ymin, 1.1*ymax])
#         axi.set_xticks(list(time[::int(60*ts/dt_aggr)])) #one tick each hour
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()
#         axi.legend(loc='upper left',fontsize=fontsize_legend, ncol = 2)
    
#     filename = 'avg_quant_loadprof_' + season + '_' + str(n_hh) + '_' + en_class + '_' + location + '.png'
#     fname = basepath / dirname / subdirname
#     fig2.savefig(fpath / filename)



# plot_specs = {
#     0: ['plot', 'Average'],
#     1: ['bar', '{} %'.format(quantile_max),],
#     2: ['bar', '{} %'.format(quantile_med),],
#     3: ['bar', '{} %'.format(quantile_min),],
# }




def seasonal_load_profiles(time, powers, plot_specs, season, **params):

   #Default parameters
    def_params = {
    'time_scale': 'h',
    'power_scale': 'kW',
    'energy_scale': 'MWh',
    'figsize': (297/25.4 , 420/25.4),
    'orientation': 'horizontal',
    'font_small': 14,
    'font_medium': 16,
    'font_large': 18,
    }
    
    # The parameters that are not specified when the function is called are set to the default value
    for param in def_params: 
        if param not in params: params[param] = def_params[param]

    # Scales setup: factors needed to turn the values of time, power and energy in the correct scale
    time_scale = params['time_scale']
    power_scale = params['power_scale']
    energy_scale = params['energy_scale']

    ts = ts_dict[time_scale]
    ps = ps_dict[power_scale]
    es = es_dict[energy_scale]

    # Time and power are adjusted to the proper scales
    time = time*ts
    powers= powers*ps

    # Figure setup: figure size and orientatio, font-sizes 
    figsize = params['figsize']
    orientation = params['orientation']

    if orientation == 'horizontal': figsize = figsize[::-1]

    fontsize_title = params['font_large']
    fontsize_legend = params['font_medium']
    fontsize_labels = params['font_medium']
    fontsize_text = params['font_medium']
    fontsize_ticks = params['font_small']
    fontsize_pielabels = params['font_small']

    
    # A figure with multiple subplots is created, with as many rows as the seasons,
    # for each row there two columns (for week-days and weekend-days)
    fig, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
    
    suptitle = '\nAverage load profile and quantile during one day {}'.format(
        '\nfor {} households with {} energetic class in the {} of Italy'.format(n_hh,en_class,location.capitalize()))
    fig.suptitle(suptitle, fontsize=fontsize_title , fontweight = 'bold')
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
   

    # Evaluating the time-step of the time-vector in order to set the bars' width
    dt = float((time[-1] - time[0])/(np.size(time)-1))
    print(type(dt))
    print(dt)

    # Evaluating the number of profiles passed to the function for each day-type 
    # It is given for ganted that only two day-types are considered
    n_lps =  int(np.size(powers, axis=1)/len(days))
    
    for day in days:

        # Number corresponding to the type of day (0: week-day, 1: week-end -day)
        dd = days[day][0] 
    
        # Index needed for slicing the powers-array, according to the day of the week
        start = dd*n_lps 


        for lp in range(n_lps):

            power = powers[:,start + lp]
            plot_type = plot_specs[lp][0]
            legend = plot_specs[lp][1]

            if plot_type == 'plot':
                ax[dd].plot(time + dt/2, power, color  = colors_rgb[lp], linestyle = '-', label = legend)
 
            elif plot_type == 'bar':
                ax[dd].bar(time, power, color  = colors_rgb[lp], width=dt, align='edge', label = legend)
        
        title = '{}, {}'.format(season.capitalize(),day)
        ax[dd].set_title(title, fontsize=fontsize_title)
        

    for axi in ax.flatten():
        axi.set_xlabel('Time [{}]'.format(time_scale), fontsize = fontsize_labels)
        axi.set_ylabel('Power [{}]'.format(power_scale), fontsize = fontsize_labels)
        axi.set_xlim([time[0], time[-1]])
        ymin = np.min(powers); ymax = np.max(powers)
        axi.set_ylim([0.9*ymin, 1.1*ymax])
        # Set one tick each hour on the x-axis
        axi.set_xticks(list(time[::int(60*ts/dt)]))
        axi.tick_params(axis='both',labelsize=fontsize_labels)
        axi.tick_params(axis='x',labelrotation=0)
        axi.grid()
        axi.legend(loc='upper left',fontsize=fontsize_legend, ncol = 2)
    
    
    return(fig)




########## Total energy consumption from classes of appliances for season

# First, the energy consumptions from the various appliances aggregated into
# energy consumptions from classes of appliances, in order to improve the 
# readability of the charts. THe class of the various appliances is defined
# in the apps_ID dictionary.

es = 1

energy_w = np.random.randint(100, size = (len(apps_ID),n_hh))
energy_p = np.random.randint(100, size = (len(apps_ID),n_hh))
energy_s = np.random.randint(100, size = (len(apps_ID),n_hh))
energy_a = np.random.randint(100, size = (len(apps_ID),n_hh))

energy_w_tot = np.sum(energy_w,axis=1)*es #adjusted to the energy scale
energy_p_tot = np.sum(energy_p,axis=1)*es
energy_s_tot = np.sum(energy_s,axis=1)*es
energy_a_tot = np.sum(energy_a,axis=1)*es

apps_classes = {}
ii = 0
for app in apps_ID:
    if apps_ID[app][5] not in apps_classes: 
        apps_classes[apps_ID[app][5]] = (ii , colors_rgb[ii] )
        ii += 1

energy_w_tot_class = np.zeros(len(apps_classes))
energy_p_tot_class = np.zeros(len(apps_classes))
energy_s_tot_class = np.zeros(len(apps_classes))
energy_a_tot_class = np.zeros(len(apps_classes))

for app_class in apps_classes:
    
    apps_list=[]
    for app in apps_ID:
        if apps_ID[app][5] == app_class:apps_list.append(apps_ID[app][0])
    
    energy_w_tot_class[apps_classes[app_class][0]] = np.sum(energy_w_tot[apps_list])
    energy_p_tot_class[apps_classes[app_class][0]] = np.sum(energy_p_tot[apps_list])
    energy_s_tot_class[apps_classes[app_class][0]] = np.sum(energy_s_tot[apps_list])
    energy_a_tot_class[apps_classes[app_class][0]] = np.sum(energy_a_tot[apps_list]) 
    

# The total energy consumption from the classes of appliances is represented


def seasonal_energy(energies, plot_specs, **params):

   #Default parameters
    def_params = {
    'time_scale': 'h',
    'power_scale': 'kW',
    'energy_scale': 'MWh',
    'figsize': (297/25.4 , 420/25.4),
    'orientation': 'horizontal',
    'font_small': 14,
    'font_medium': 16,
    'font_large': 18,
    }
    
    # The parameters that are not specified when the function is called are set to the default value
    for param in def_params: 
        if param not in params: params[param] = def_params[param]

    # Scales setup: factors needed to turn the values of time, power and energy in the correct scale
    time_scale = params['time_scale']
    power_scale = params['power_scale']
    energy_scale = params['energy_scale']

    ts = ts_dict[time_scale]
    ps = ps_dict[power_scale]
    es = es_dict[energy_scale]

    # Energies are adjusted to the proper scales
    energies = energies*es

    # Figure setup: figure size and orientatio, font-sizes 
    figsize = params['figsize']
    orientation = params['orientation']

    if orientation == 'horizontal': figsize = figsize[::-1]

    fontsize_title = params['font_large']
    fontsize_legend = params['font_medium']
    fontsize_labels = params['font_medium']
    fontsize_text = params['font_medium']
    fontsize_ticks = params['font_small']
    fontsize_pielabels = params['font_small']


    fig, ax = plt.subplots(figsize=figsize)
    suptitle = '\nTotal energy consumption from classes of appliances by season {}'.format(
        '\n for {} households with {} energetic class in the {} of Italy'.format(n_hh,en_class,location.capitalize()))
    fig.suptitle(suptitle, fontsize =fontsize_title , fontweight = 'bold')
    fig.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.88, wspace=None, hspace=0.3)

    labels = [apps_class.capitalize().replace('_',' ') for apps_class in apps_classes]
    # 
    #for apps_class in apps_classes.keys(): labels.append(apps_class.capitalize().replace('_',' '))

    bottoms = np.zeros(len(labels))
    print(np.shape(bottoms))

    leg = []

    ymax = 0
    text_coord = 0,ymax
    text_toadd = ''

    text_toadd = 'Energy consumption by season\n'
    for season in seasons:
        
        # Number corresponding to the season (0: winter, 1: summer, 2: spring, 3: autumn)
        ss = seasons[season][0]

        # Energies corresponding to the seasonal consumption
        heights = energies[ss, :]
        print(np.shape(heights))
        print(np.shape(bottoms))
        
        ax.bar(labels,heights,bottom=bottoms)
        bottoms = bottoms + heights
        
        if np.max(bottoms) > ymax: ymax = np.max(bottoms)
        
        leg.append(season.capitalize())
        
        text_coord = 0,ymax
        text_toadd = text_toadd + '\n%s: %.3f %s\n' % (season.capitalize(),np.sum(heights),energy_scale) 


    ax.set_ylim([0,1.1*ymax])

    ax.set_ylabel('Energy consumption [' + energy_scale + '/year]', fontsize=fontsize_labels)
    ax.tick_params(axis='both',labelsize=fontsize_labels)
    ax.tick_params(axis='x',labelrotation=45)
    ax.grid(axis='y')

    ax.legend(leg,loc='upper left',ncol=len(seasons),fontsize=fontsize_legend)

    props = dict(boxstyle='square', facecolor=colors_rgb[2], pad = 0.3, alpha=0.5)                     
    ax.text(0.02, 0.9, text_toadd.rstrip(), fontsize=fontsize_text, ha='left', va='top', transform=ax.transAxes ,bbox=props)


    return(fig)

f=input()




energies = np.array((energy_w_tot_class,energy_s_tot_class,energy_p_tot_class,energy_a_tot_class))
print(np.shape(energies))
print(np.shape(energies[0,:,]))
fig = seasonal_energy(energies,'a')
fig.savefig('shish.png')


















    
time_aggr=np.arange(0,1440,15)
lp1_aggr=np.random.randint(100,size=np.shape(time_aggr))
lp2_aggr=np.random.randint(100,size=np.shape(time_aggr))

powers = np.column_stack((lp1_aggr,lp2_aggr))

mm2inch = 1/25.4
params = {
    'figsize': (297*mm2inch,420*mm2inch),
    'orientation': 'horizontal'
}

fontsizes_dict = {
    'font_small': 14,
    'font_medium': 16,
    'font_large': 18
}

plot_params = {
    'time_scale': 'h',
    'power_scale': 'kW',
    'energy_scale': 'MWh'
}

plot_specs = {
    0: ['plot', 'Total'],
   
}

fig = seasonal_load_profiles(time_aggr,powers,plot_specs,'winter',**params,**fontsizes_dict,**plot_params)

fig.savefig('eeeh.png')