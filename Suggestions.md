# Suggestions

## Suggestions for potential improvements (or changes, anyway) of the routine can be written down here

### 1. Evaluation of the average nominal power for a given appliance

Right now, the following calculation is performed: the yearly energy consumption of the appliance, according to its energetic class (kWh/year) is considered. It is divided by 365 and multiplied by 1e3 in order to get the average daily consumption (Wh/day). This value is divided by the average time for which the appliance is used everyday, according to previous studies (ISTAT, MICENE and others).

The problem is that this calculation considers an everyday-use of the appliance, ignoring the fact that it might be used for a certain number of days a week. The yearly (even weekly, as a first approximation) energy consumption from the appliance is, for obvious reasons, correct, whereas the average power during each usage-cycle might be wrong. For example, considering A-labelled appliances, the average power for a vacuum cleaner results to be equal to ~350 W (against the 800 - 1500 W that are found in other sources), for an electric oven the average power results to be equal to ~350 W (against the 2000 W that are found in other sources), and so on.

When the energy consumption is concerned, this may not be a problem, but in our case , where we'll deal with instantaneous (quartelry or hourly) demand, this might be an issue that brings to an underestimation of the electricity demand from a household.

### 2. Use of the user's behavior coefficients kk

Right now, a user's behavior coefficient is deployed, that ranges between 0 and 1.7, that increases/decreases the power for each appliance according to the user's behavior in each season, in each location (e.g. kk is equal to 0 for AC during winter,spring and autumn since it is only used during summer, kk is equal to 1.7 for the electric boiler during winter, while it is equal to 0.7 during summer).

It appears rather strange, anyway, that the power demanded by an appliance changes according to user's behavior, while it would sound much better if the time in which the appliance is used changes according to this coefficient, that might increase/decrease the time (keeping the power constant) in order to icnrese/decrease the energy consumption.

Furthermore, right now this coefficient are, making a rough estimate, averagely equal to 1.2. This means that, globally, the yearly energy consumption for each appliance is increased with respect to the values given by the energy labels. Since the kk coefficient's goal is to take into account the variation of the user's behvior according to the season, shouldn't the following equation hold: (kk_winter + kk_summer + kk_spring + kk_autumn)/4 = 1 ? So that the yearly energy consumption remains constant?

### More