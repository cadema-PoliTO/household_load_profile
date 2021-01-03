# Checklist

## Stuff to do next in order to improve the repository

- [x] Update the values of the applinces' distribution factors
- [x] Sort the appliances in a proper way, so that the least-manageable ones are the first ones to be injected into the load profile of the house
- [x] Organize the input/output/paramters files into different folders
- [ ] Update the values of the user's behavior coefficients
- [x] Find out what slows down the routine when used from main (with energetic class D, it takes about 1 min to get the results for 100 households, when the routine that evaluates the load profile for a single household takes around 0.09 s when used alone)
- [x] Fix the code so that it can run on evey OS.
- [ ] Add the possibility to have more units of an appliance larger than the total number of households (i.e. distribution factor larger than 1, for example for TVs)
- [ ] Change the way input files are opened (opened in main and passed to the modules, rather than reading them in each module)
