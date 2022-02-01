# HVSR_to_virtual_borehole
<a href="https://doi.org/10.5281/zenodo.4276310"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4276310.svg" alt="DOI"></a>

This Python module contains several scripts that accompany the following paper:

Van Noten, K., Lecocq, T., Goffin, C., Meyvis, B., Molron, J., Debacker, T. & Devleeschouwer, X. 2022. Brussels’ bedrock paleorelief from borehole-controlled powerlaws linking polarised H/V resonance frequencies and sediment thickness. Journal of Seismology. https://doi.org/10.1007/s10950-021-10039-8

The purpose of the codes are to convert data output files of GEOPSY (http://www.geopsy.org/) into more practical figures ready for scientific publishing. 

Enjoy !
Cheers
Koen

## 1. Create .hv files in Geopsy
Perform the H/V spectral ratio analyses from the gathered ambient noise measurements in Geopsy and save the output as .hv file. Store the .hv files in the Data folder. See A201.hv or A202.hv as example.

## 2. Fill the database
Do the HVSR analysis for the entire database and update your database file (see HVSR database.csv) with the necessary information (ID, Filename, altitude of measurements, ...)
Name = ID of the measurement which will used as the title of the plots.
Filename = name of the .hv files which need to be plotted. 

## 3. Get f0s from geopsy hv files.py
This script reads the HVSR database file and loads one or all HVSR data (min f0, f0, max f0, error, max Amplitude, n of windows) automatically from all .hv files stored in the Data folder. The default setting of Geopsy to export the H/V spectrum is set to 100 samples (100 freq. and Amplitude values), no matter the range in the output frequency sampling. If this default sampling setting is used, a wide output range, e.g. 0.5 Hz to 50 Hz, will pick f0 less accurately than if a narrow range around the peak amplitude is selected. To increase the f0 picking accuracy, one can increase the sample setting to the maximum (e.g. 9999 samples) in Geopsy. Or one can resample the Geopsy output curve by a performing a linear interpolation up to 15000 samples (interpolation used in this script). This results in a slightly different interpolated amplitude maximum and f0 than the one exported by Geopsy. The interpolated values (f0_ip & A0) and its difference with F0 from Geopsy (f0_ip_diff) will be exported into the database file, which will be named as HVSR database file_f0_from_hv.csv.

## 3. HVSR to virtual borehole.py: 
This script replots one or all .hv files into a f0 versus amplitude plot and to converts the H/V spectrum to a VIRTUAL BOREHOLE using a regression - powerlaw - function between f0 and depth. The output figures will be saved in the output folder. See Van Noten et al. (2022) for explanation of the methodology. The figure in below shows the output of the script:

<img src="https://github.com/KoenVanNoten/HVSR_to_virtual_borehole/blob/master/Output/A201.png" width="550" height="360" />

## 4. HVSR polarisation.py:
The H/V rotational module in Geopsy computes the azimuth in which the resonance frequency has his maximum amplitude. In the Geopsy H/V rotate results, right click on the grid file and export values with the same name as you saved the H/V results (either without extension, see A201 or A202 as example, or as .grid file). Store the data in the Data folder. To facilate reading this polarisation, this python script plots the variation of the amplitude with azimuth in a polar plot. The figures will be save in the Output folder. The IDs to plot will be loaded from the HVSR database file. Polarisation data (Amax, Amin and their corresponding azimuths and frequencies) will be exported into the database file as HVSR database file_f0_from_hv_polarisation.csv which then can be visualised in a GIS. Output figure:

<img src="https://github.com/KoenVanNoten/HVSR_to_virtual_borehole/blob/master/Output/A201_polarisation.png" width="450" height="350" />

## 5. Construct the f0 - Sed Thickness Powerlaw Relation.ipynb:
This is an Ipython notebook to construct figures 5, 6, 7, 8 and 10 of the Van Noten et al. (2022) paper. This notebook reads the borehole and survey HVSR supplementary data of the paper (see VanNotenetal_JOSE_S1 - Borehole HVSR analysis.csv and VanNotenetal_JOSE_S2 - Survey HVSR analysis.csv). Also the methodology how to create a statistical powerlaw relation is explained. 

## Installation
To run the steps above, you need:
- Geopsy pack 2019 or above
- Python (3.x recommended)
- Iptyhon notebook
- Numpy
- Scipy
- Pandas
- MatPlotLib
- csv
- os
