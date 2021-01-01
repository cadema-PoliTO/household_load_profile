import numpy as np
import matplotlib.pyplot as plt
# import datareader
from pathlib import Path
import csv

basepath = Path(__file__).parent


seasons = dict({'winter':(0,'w'),'summer':(1,'s'),'spring':(2,'ap'),'autumn':(3,'ap')})
days = dict({'week-day':(0,'wd'),'weekend-day':(1,'we')})

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

# Simulation parameters that can be changed
n_hh = 100 #number of households (-)
n_people_avg = 2.7 #average number of members for each household (-)
ftg_avg = 100  #average footage of each household (m2)
location = 'north' #geographical location: 'north' | 'centre' | 'south'
power_max = 3000 #maximum power available from the grid (contractual power) (W)
en_class = 'A+' #energetic class of the appiances: 'A+++' | 'A++' | 'A+' | 'A' | 'B' | 'C' | 'D'



# Plotting parameters
time_scale = 'h'
power_scale = 'kW'
energy_scale = 'MWh'

ts_dict = {'min':1/1,'h':1/60}
ps_dict = {'W':1/1,'kW':1/1e3}
es_dict = {'Wh':1/1,'kWh':1/1e3,'MWh':1/1e6}

########## Plotting the load profiles

# def aggr_load_profile(time_aggr, power_aggr, season, **params):

#     for key in params:
#         print('{}: {}, {}'.format(key,params[key],type(params[key])))




    # # Scales setup: factors needed to turn the values of time, power and energy in the correct scale
    # time_scale = params['time_scale']
    # power_scale = params['power_scale']
    # energy_scale = params['energy_scale']

    # ts = ts_dict[time_scale]
    # ps = ps_dict[power_scale]
    # es = es_dict[energy_scale]

    # # Figure setup: figure size and orientatio, font-sizes 
    # figsize = params['figsize']
    # orientation = params['orientation']

    # if orientation == 'horizontal': figsize = figsize[::-1]

    # fontsize_title = params['font_large']
    # fontsize_legend = params['font_medium']
    # fontsize_labels = params['font_medium']
    # fontsize_text = params['font_medium']
    # fontsize_ticks = params['font_small']
        
    # # A figure with multiple subplots is created, with as many rows as the seasons,
    # # for each row there two columns (for week-days and weekend-days)
    # fig, ax = plt.subplots(2,1,sharex=False,sharey=False,figsize=figsize)
        
    # suptitle = '\nAggregated load profiles during one day \nfor {} households with {} energetic class in the {} of Italy'.format(n_hh,en_class,location.capitalize())
    # fig.suptitle(suptitle, fontsize=fontsize_title , fontweight = 'bold')
    # fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.85, wspace=None, hspace=0.3)
    
    # ymax = 0
    # ymin = 0

    # #Evaluating the time-step of the time-vector in order to set the bars' width
    # dt_aggr = (time_aggr[-1] - time_aggr[0])/np.size(time_aggr)
    
    # for day in days:
        
    #     # Number corresponding to the type of day (0: week-day, 1: week-end -day)
    #     dd = days[day][0] 
        
    #     if np.max(power_aggr) >= ymax: ymax = np.max(power_aggr)
    #     if np.min(power_aggr) <= ymin: ymin = np.min(power_aggr)
        
    #     # Title of the subplot
    #     title = season.capitalize() + ', ' + day
    #     ax[dd].bar(time_aggr*ts, power_aggr*ps, width=dt_aggr, align='edge')
    #     ax[dd].set_title(title, fontsize=fontsize_title)
        
        
    # for axi in ax.flatten():
    #     axi.set_xlabel('Time [{}]'.format(time_scale), fontsize=fontsize_labels)
    #     axi.set_ylabel('Power [{}]'.format(power_scale), fontsize=fontsize_labels)
    #     axi.set_xlim([time_aggr[0],time_aggr[-1]])
    #     axi.set_ylim([0.9*ymin,1.1*ymax])
    #     axi.set_xticks(list(time_aggr[::int(60*ts/dt_aggr)]))
    #     axi.tick_params(axis='both',labelsize=fontsize_labels)
    #     axi.tick_params(axis='x',labelrotation=0)
    #     axi.grid()
        
    # fig.subplots_adjust(wspace=0.2)

    # return(fig1)

    
# time_aggr=np.arange(0,1440,15)
# lp_aggr=np.random.randint(100,size=np.shape(time_aggr))

# mm2inch = 1/25.4
# params = {
#     'figsize': (297*mm2inch,420*mm2inch),
#     'orientation': 'horizontal'
# }

# fontsizes_dict = {
#     'font_small': 14,
#     'font_medium': 16,
#     'font_large': 18
# }

# plot_params = {
#     'time_scale': 'h',
#     'power_scale': 'kW',
#     'energy_scale': 'MWh'
# }

# aggr_load_profile(time_aggr,lp_aggr,'winter',**params,**fontsizes_dict,**plot_params)


# # params = **plot_params,fontsizes_dict,params

# #Default parameters
# def_params = {
#     'time_scale': 'h',
#     'power_scale': 'kW',
#     'energy_scale': 'MWh',
#     'figsize': (297/25.4 , 420/25.4),
#     'orientation': 'horizontal',
#     'font_small': 14,
#     'font_medium': 16,
#     'font_large': 18,
# }

# print(params)
# print(def_params)


# for param in def_params: 
#     if param not in params: params[param] = def_params[param]

# print(params)

# def eeh(x, y, **kwarg):

#     print('{}, {}'.format(x,type(x)))
#     print('{}, {}'.format(y,type(y)))

#     [print('{}, {}'.format(arg,type(arg))) for arg in kwarg]
#     [print('{}, {}'.format(argval,type(argval))) for argval in kwarg.values()]

#     for argval in kwarg.values():

#         if type(argval) is dict:

#             for key in argval: print('{}: {}'.format(key, argval[key]))



# eeh('a',45, cinque = 'eeh', d = 5, e = 'g', vilnius = 'banana' , hilsen = [1,2,3,'g']  , paita = {1:5, 2:'y', '3': 55})



# def load_profiles(time, powers, plot_specs, season, **params):

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
    
#     ymin = np.min(powers)
#     ymax = np.max(powers)

#     # Evaluating the time-step of the time-vector in order to set the bars' width
#     dt = float((time[-1] - time[0])/(np.size(time)-1))
#     print(type(dt))
#     print(dt)

#     # Evaluating the number of profiles passed to the function for each day-type 
#     # It is given for ganted that only two day-types are considered
#     n_lps =  int(np.size(powers, axis=1)/len(days))
    
#     for day in days:

#         # Number corresponding to the type of day (0: week-day, 1: week-end -day)
#         dd = days[day][0] 
    
#         # Index needed for slicing the powers-array, according to the day of the week
#         start = dd*n_lps 

#         title = season.capitalize() + ', ' + day

#         for lp in range(n_lps):

#             power = powers[:,start + lp]
#             plot_type = plot_specs[lp][0]
#             legend = plot_specs[lp][1]

#             if plot_type == 'plot':
#                 ax[dd].plot(time + dt/2, power, color  = colors_rgb[lp], linestyle = '-', label = legend)
 
#             elif plot_type == 'bar':
#                 ax[dd].bar(time, power, color  = colors_rgb[lp], width=dt, align='edge', label = legend)
        
#         ax[dd].set_title(title, fontsize=fontsize_title)
        

#     for axi in ax.flatten():
#         axi.set_xlabel('Time [' + time_scale + ']', fontsize=fontsize_labels)
#         axi.set_ylabel('Power [' + power_scale + ']', fontsize=fontsize_labels)
#         axi.set_xlim([time[0], time[-1]])
#         axi.set_ylim([0.9*ymin, 1.1*ymax])
#         # Set one tick each hour on the x-axis
#         axi.set_xticks(list(time[::int(60*ts/dt)]))
#         axi.tick_params(axis='both',labelsize=fontsize_labels)
#         axi.tick_params(axis='x',labelrotation=0)
#         axi.grid()
#         axi.legend(loc='upper left',fontsize=fontsize_legend, ncol = 2)
    
    
#     return(fig)


# quantile_min, quantile_med, quantile_max = 15,50,85 #quantile for the evaluation of minimum, medium and maximux power demands for the load profiles

# plot_specs = {
#     0: ['plot', 'Average'],
#     1: ['bar', '{} %'.format(quantile_max),],
#     2: ['bar', '{} %'.format(quantile_med),],
#     3: ['bar', '{} %'.format(quantile_min),],
# }

# time=np.arange(0,1440,15).reshape(int(1440/15),)
# lp1_1 = np.random.randint(100,size=np.shape(time))
# lp1_2 = np.random.randint(100,size=np.shape(time))
# lp1_3 = np.random.randint(100,size=np.shape(time))
# lp1_4 = np.random.randint(100,size=np.shape(time))
# lp2_1 = np.random.randint(100,size=np.shape(time))
# lp2_2 = np.random.randint(100,size=np.shape(time))
# lp2_3 = np.random.randint(100,size=np.shape(time))
# lp2_4 = np.random.randint(100,size=np.shape(time))

# powers = np.column_stack((lp1_1, lp1_2, lp1_3, lp1_4,
#                    lp2_1, lp2_2, lp2_3, lp2_4,))



# print(time)
# print(np.shape(powers))
# print(type(time))

# plt.figure()
# plt.bar(time,lp1_1)
# plt.show()

# # print(powers)
# # print(np.shape(powers))

# mm2inch = 1/25.4
# params = {
#     'figsize': (297*mm2inch,420*mm2inch),
#     'orientation': 'horizontal'
# }

# fontsizes_dict = {
#     'font_small': 14,
#     'font_medium': 16,
#     'font_large': 18
# }

# plot_params = {
#     'time_scale': 'h',
#     'power_scale': 'kW',
#     'energy_scale': 'MWh'
# }

# # params = **plot_params,fontsizes_dict,params

# fig = load_profiles(time,powers,plot_specs,'winter',**params,**fontsizes_dict,**plot_params)

# fig.savefig('aaa.png')













# suptitle = '\nAverage load profile and quantile during one day {}'.format(
#         '\nfor {} households with {} energetic class in the {} of Italy'.format(n_hh,en_class,location.capitalize()))

# print(suptitle)






# apps,apps_ID,apps_attr = datareader.read_appliances('eltdome_report.csv',';','Input')


# apps_classes = {}
# ii = 0
# for app in apps_ID:
#     if apps_ID[app][5] not in apps_classes: 
#         apps_classes[apps_ID[app][5]] = (ii , colors_rgb[ii] )
#         ii += 1


# labels = [apps_class.capitalize().replace('_',' ') for apps_class in apps_classes]
# print(labels)






# energies = np.array([[[1,2,5,6],
#                       [3,4,70,8],
#                       [4,5,8,9]
#                      ],
                     
#                      [[1,2,5,6],
#                       [3,4,7,8],
#                       [400,5,8,9]
#                      ],
#                     ])

# print(np.shape(energies))
# print(energies[0,1,2])
# print(energies[1,2,0])

# # seasonal_energy=np.dstack((np.array([[1,2,5,6], [3,4,70,8], [4,5,8,9]]), np.array([[1,2,5,6], [3,4,7,8], [400,5,8,9]])))
# seasonal_energy = np.array((np.array([[1,2,5,6], [3,4,70,8], [4,5,8,9]]), np.array([[1,2,5,6], [3,4,7,8], [400,5,8,9]])))

# print(energies)
# print(seasonal_energy)

# print(seasonal_energy==energies)

# from tictoc import tic, toc

# tic()
# a = [x for x in seasons]
# print(toc())
# print(a)

# tic()
# b = list(seasons.keys())
# print(toc())
# print(b)



# energies = np.random.randint(100, size=(24, 4))
# print(np.shape(energies))

# total_heights = np.sum(energies, axis = 1)
# print(np.shape(total_heights))





# energies = np.random.randint(100, size=(17, 4))
# print(energies)
# energies_tot = np.sum(energies, axis = 0)
# print(energies_tot)
# energies_perc = energies/energies_tot*100
# print(energies_perc)

# print(np.sum(energies_perc, axis = 0))

# print(energies_perc)


# x = np.zeros((24, 2*4))


# for dd in range(2):
#     print(dd)
#     print(np.arange(4) + dd*4)
#     x[: , np.arange(4) + dd*4] = np.random.randint(100, size = (24, 4))

# print(x)




# arrays = [np.random.randn(3, 4) for _ in range(10)]
# stack1 = np.stack(arrays, axis=0)
# stack2 = np.stack(arrays, axis=1)
# stack3 = np.stack(arrays, axis=2)

# print(stack1)
# print(stack1.shape)
# print(stack2.shape)
# print(stack3.shape)

# print(stack1[0,:,:])

# ss = 0
# lp_tot_stor = np.random.randn(4,24,2)
# print(lp_tot_stor.shape)
# print(lp_tot_stor[ss, :, :].shape)
# powers1 = lp_tot_stor[ss, :, :].reshape(1, np.size(lp_tot_stor[ss, :, :], axis = 0), np.size(lp_tot_stor[ss, :, :], axis = 1))
# powers2 = lp_tot_stor[np.newaxis, ss, :, :]

# print(powers1.shape)
# print(powers1)

# print(powers2.shape)
# print(powers2)

# print(powers1 == powers2)


# import plot_generator as plot

# # Total load profiles 
# time_aggr = np.arange(0,24,1)
# lp_tot1_stor = np.column_stack((np.linspace(0, 100, 24), np.linspace(0, 200, 24)))
# lp_tot2_stor = np.column_stack((np.linspace(0, 300, 24), np.linspace(0, 400, 24)))
# lp_tot3_stor = np.column_stack((np.linspace(0, 500, 24), np.linspace(0, 600, 24)))
# lp_tot4_stor = np.column_stack((np.linspace(0, 700, 24), np.linspace(0, 800, 24)))

# lp_tot_stor = np.stack((lp_tot1_stor, lp_tot2_stor, lp_tot3_stor, lp_tot4_stor), axis = 0)

# print(lp_tot_stor.shape)

# for season in seasons:

#     ss = seasons[season][0]
#     plot_specs = {
#     0: ['bar', 'Total'],
#     }

#     powers1 = lp_tot_stor[np.newaxis, ss, :, :]

#     fig = plot.seasonal_load_profiles(time_aggr, powers1, plot_specs, season)
#     fig.show()


# Average load profile and quantiles
# plot_specs = {
#     0: ['plot', 'Average'],
#     1: ['bar', 'Min'],
#     2: ['bar', 'Med'],
#     3: ['bar', 'Max']
#     }

# season = 'winter'

# powers2 = np.stack((lp_tot1_stor, lp_tot4_stor, lp_tot3_stor, lp_tot2_stor), axis = 0)
# fig = plot.seasonal_load_profiles(time_aggr, powers2, plot_specs, season)
# fig.show()





# energies = np.random.randint(100, size = (4, 17, 100))

# energies_tot = np.sum(energies, axis = (0,2))
# energies_sum = np.sum(energies, axis =2)

# print(energies_sum.shape)
# print(energies_sum)


# # energies_sum = energies_sum.reshape(17,4)
# energies_sum = np.transpose(energies_sum)
# print(energies_sum.shape)
# print(energies_sum)

# energiii = np.transpose(np.sum(energies, axis = 2))
# print(energiii.shape)
# print(energiii)

# print(energiii == energies_sum)



    
fpath = basepath / 'Input'  
filename = 'eltdome_report.csv'
delimit = ';'
    
app_list = [] #list containing, for each appliance,its attributes 
app_ID = {} #dictionary relating each appliance to an identification number, nickname and type
    
# Reading the CSV file
with open(fpath / filename, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=delimit)
    line_count = 0
    for row in csv_reader:
        # if line_count == 0:
        #     header = row
            
        #     # The second row contains the units of measure and is automatically skipped
        #     line_count += 2
        #     continue
        
        # else:
        #     app_list.append(row[7:])
        #     app_ID[row[1].lower()] = (int(row[0]), row[2], row[3], row[4].split(','), row[5].split(','), row[6])
        
        # line_count += 1
        if line_count == 1: 
            next(csv_reader)

        print(row)
        line_count += 1

input('Stop?')