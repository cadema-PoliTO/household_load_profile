# Aggregated_Household_Load_Profiler

## Generation of load profiles from electric appliances for an aggregate of household

### Requirements

Codes included in this repository are written in Python 3, that is the only real requirement. They have been tested with Python 3.8 but also earlier version of Python 3 should work.
Python packages needed for running the methods are: numpy, scipy.interpolate, matplotlib.pyplot, math, random. All the other self-created methods used are present in this repository.

### General description

This is an open-source routine that creates the load profiles from the main electric appliances for a domestic user (household), for an aggregate of households. Different load profiles are evaluated according to the season, the day of the week (distinguishing between weekdays and weekend days) and the energetic class of the appliances.
The load profiles are evaluated for a whole day ($1440 \textrm{ min}$) with a time-resolution of $1 \textrm{ min}$. Anyway, the result can be aggregated and shown with a different timestep (ranging from $5$ to $60 \textrm{ min}$). The total and average energy consumptions from the ensamble of electric appliances are also evaluated, considering a reference year that starts on a Monday 01/01.

#### Input data

This routine relies on sets of data that were the result of a measurement campaign performed by eERG (end-use Efficiency Research Group) conducted in the early 2000s and called MICENE (MIsure dei Consumi di ENergia Elettrica). During this campain 110 households in different parts of Italy were monitored for a period of at least three weeks in order to evaluate the energy consumption from the main electric appliances. The energy consumption was measured every ten minutes and therefore resulted in a load profile with a $10 \textrm{ min}$ resolution. The results were averaged among the different days of measurement and among the different households.
The appliances considered in the study were: vacuum cleaner, dishwasher, washing machine and tumble drier, audio-video devices (tv, hifi stereo,...) and other electronic devices (laptop, personal computers) and lighting.

In this routine, other appliances are also considered, suchs as air-conditioner, electric and microwave ovens. The load profile for air-conditioners is drawn starting from energy consumption assessments performed by Enea, while the yearly energy consumption is adjusted to the data given by EURECO. The data for electric and microwave ovens is taken from REMODECE.

For each appliance a certain number of attributes needs to be specified, such as the distribution factor in different geographical locations (meaning that a given appliance may not be present in all households), the time period in which it is averagely switched on during a day and so on. This data is taken from the report from the International Conference Eedal 2006. Also, for each appliance a different average yearly energy consumption is considered according to the energy class and a "user's behavior" coefficient is considered according to the season. This data is taken from energy consumption assessments performed by Enea.

#### Routine process

The routine works on different levels, in a bottom-up fashion. This means that different methods are used that perform the evaluation of the load profile, first for a single appliance, then for an household (with a given availability of appliances, according to their distribution factors) and finally for the aggregate of housholds. This allows to obatin results on different scale and therefore to check them individually.

##### i. Generation of the load profile for each appliance

As mentioned above, at this level the load profile for one day ($1440 \textrm{ min}$) is evaluated for a single appliance, with a time-resolution of $1 \textrm{ min}$. This is done by following a different routine, according to the type of appliance that is considered.

* Appliances of "continuous" type  (air-conditioner and lighting).

   They are used throughout the whole day, therefore the power demand from the appliance is already known for each timestep and can be directly injected into the load profile. Anyway, it must be firstly adjusted to the one-minute resolution and the value of the power is adjusted to the season and to the actual footage of the household (since the values are normalized for a $100 \textrm{ m}^2$ household).
* Appliances of not "continuous" type  (all the others).

   They are used for a limited time period during the day (hereinafter referred to as "duration"). It is needed to randomly select a moment in which the appliance is switched (remaining on for its whole duration period). This is done considering the data from MICENE as a frequency density for the event of the appliance being switched on throughout the day. A cumulative frequency is evaluated from the frequency density. Finally the instant when the appliance is switched on is evaluated generating a certain proability as a random number and checking at which time in the day the cumulative frequency reaches this value. Starting from this moment, the power demand from the appliance needs to be injected into the load profile. The power demand is evaluated according to the type of appliance.
  * "duty-cycle" type appliances (dishwasher, washing machine and tumble drier).
     The duty-cycle, i.e. the power demand throughout the whole duration of the appliance, is known, therefore it can be directly injected into the load profile. Anyway, the values of the power must be firstly adjusted to the season and the energetic class.
  * "no duty-cycle" type appliances (all the others).
     This appliances are considered to demand a constant power thoughout their duration. Therefore a uniform duty-cycle is built according to their duration and the value of the nominal power (that is adjusted to the season and the energetic class). Firstly, the duration is modified in order to consider the behavior of different users. This is done by exctrating a new duration from a normal distribution (centred in the original duration, with a given standard deviation), that must fit in a specified range.

##### ii. Generation of the load profile for a household

The load profile for the whole house, i.e. the sum of the instantaneous power demand from all the appliances available in the household, is evaluated calling the method that computes the load profile for a single appliance, as many times as the appliances available in the house. Since the power demands from the single appliances are summed, the total power demand may exceed the contractual power (maximum power) for the household. If this happens, the method is re-called for a single appliance for a certain number of tries. If this still fails, the power is saturated to the maximum power. The energy consumed in one day by each appliance is also evaluated by integratin the instantaneous power over the whole day.

##### iii. Aggregation of the load profiles from the single households

The method that computes the load profile for a single household is computed for a certain number of households and aggregated with a new timestep to be specified. Firstly, an "appliances availability" matrix has to be built, in which for each household, the availability of the different appliances is specified ($1$ is available, $0$ otherwise). This is done by computing the total number of households that own each appliances, according to the distribution factors and the total number of households, and randomly assigning thr appliances to the households. The aggregated load profiles are computed for each season, both for a weekday than a weekend day, and stored in different files (together with percentile load profiles) in order to plot them.
Concerning the energy consumptions, they are stored in a matrix in order to be able to distinguish between different appliances and different housholds. For each season, the total energy consumptions are evaluated according to the total number of week days and weekend days. Summing the energy consumptions in the different seasons, the yearly energy consumption is computed for each appliance, for each household.

### Content of the repository

#### \Input folder

This repository contains all the files that need to be loaded in the workspace of the various method as _.csv_ files. Their name is properly formatted so that each methods knows which file to look at when certain data is needed. Particularly, the file needed for the methods are:

* *'eltdome_report.csv'*: it contains the attributes for all the appliances. It also contains, for each appliance, its "nickname", that is crucial for the correct loading of the other files.

* *'classenerg_report.csv'*: it contains the yearly energy consumption for each appliance, according to the different energy classes.

* *'coeff_matrix.csv'*: it contains the "user's behavior" coefficient for each appliance, according to the different seasons.

* Load profile files. They contain a time vector (in hours, from 00:00 to 23:59), generally with a resolution of $10 \textrm{ min}$ in the first column and the load profile vector in Watt in the second column. Their name is formatted as follows: `'loadprof' + '_' + app_nickname + '_' + seasons + '_' + day + '.csv'`. Where seasons indicates if the load profile is different according to the season (*'w'* stands for winter, *'s'* for summer, *'ap'* for autumn/spring) or the same for each season (*'sawp'*) and day indicates if the load profile is different according to the day in the week (*'wd'* stands for weekday and *'we'* for weekend day) or the same throughout the whole week (*'wde'*).

* Frequency density files. They contain a time vector (in hours, from 00:00 to 23:59), generally with a resolution of $10 \textrm{ min}$ in the first column and the frequency density vector for the appliance's utilization (in Watt) in the second column. Their name is formatted as follows: `'freqdens' + '_' + app_nickname + '_' + seasons + '_' + day + '.csv'`. The same considerations made for load profile files hold.

* Duty cycle files. They contain a time vector (in minutes, from $0 \textrm{ min}$ to the value of the duration) with a resolution of $1 \textrm{ min}$ in the first columns and the power demand in Watt from the appliance for each timestep in the second column. Their name is formatted as follows: `'dutycycle' + '_' + app_nickname + '.csv'`

#### \Parameters folder

This folder contains three .csv files where the parameters that are to be specified by the user for the simulation are stored.

* *'sim_param.csv'*: it contains the user-defined values for some parameters that control the simulation.
* *'aggr_param.csv'*: it contains the user-defined values for some parameters that control the aggregation of the results.
* *'plot_param.csv'*: it contains the user-defined values for some parameters that control the post-process of the results (figures).

#### Python files

* `aggregate_load_profiler_main.py`: this is the main file, where some simulation parameters can be changed. The load aggregated load profiles in the different seasons, and the energy consumptions over one year are computed and figures are generated. This is the only file that needs to be used directly by the user. The results are saved in \Output, as follows:
  * *'aggr_lp_season_day.csv'*: they contain the aggregated load profile and the quantile for each seasons, for each type of day.
  * *'energy_season_.csv'*: they contain the energy consumed from each appliance, for each household, for each season.

* `plot_generator.py`: this file contains all the instruction for the creation of the figures showing the results. It is called by the main file but it can also be used directly by the user if the files containing the results are already saved in \Output.

* `parameters_input.py`: this file contains the methods that are used in the main file for updating the paramters value to the user's keyboard input. This file is not directly used by the user. The parameters are saved in \Parameters.

* `house_load_profiler.py`: this file contains the method that computes the load profile for a household. This file can be used directly bu the user if the load profile for a single household is to be computed.

* `load_profiler.py`: this file contains the method that computes the load profile for a single appliance. This file can be used directly bu the user if the load profile for a single appliance is to be computed.

* `cumulative_frequency.py`: this file contains a method to compute the cumulative frequency, starting from the frequency density. This file is not directely used by the user.

* `profile_interpolation.py`: this file contains the method that interpolates a given time-profile in order to change the time resolution. This file is not directely used by the user.

* `datareader.py`: this file contains different methods that properly read the various input files. This file is not directely used by the user.

#### \ Output folder

This folder contains all the .csv files where the results from the various simulations are stored. The filename is formatted in order to give all the information needed about the location, season, day type of the simulation ,as well as the number of households considered and the energetic class of the appliances.
The folder also contains the subfolder \Figures, where the graphs are saved.
