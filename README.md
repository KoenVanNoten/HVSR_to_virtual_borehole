# HVSR_to_virtual_borehole

## 1. Create .hv files in Geopsy
Conduct H/V spectral ratio analyses from gathered ambient noise measurements in Geopsy and save the output of Geopsy as .hv file.

Do that xxx times for the entire database and update your database file (see HVSR database.csv) with the necessary information (ID, Filename, altitude of measurements, ...)

## 2. Get f0s from geopsy hv files.py
Load all HVSR data (min f0, f0, max f0, error, max Amplitude, n of windows) automatically from all .hv files listed in the database file. The default setting of Geopsy to export the H/V spectrum is set to 100 samples (100 freq. and Amplitude values), no matter the range in the output frequency sampling. If this default sampling setting is used, a wide output range, e.g. 0.5 Hz to 50 Hz, will pick f0 less accurately than if a narrow range around the peak amplitude is selected. To increase the f0 picking accuracy, one can increase the sample setting to the maximum (e.g. 9999 samples in Geospy) in Geopsy. Or one can resample the Geopsy output curve by a performing a linear interpolation up to 15000 samples (interpolation used in this script). This results in a slightly different interpolated amplitude maximum and f0 than the one exported by Geopsy. The interpolated values (f0_ip & A0)and its difference with F0 from Geopsy (f0_ip_diff) will be exported to the database file.

## 3. f0_to_virtual_borehole.py: 
Script to replot one or all .hv files into a f0 versus amplitude plot and to convert the H/V spectrum to a VIRTUAL BOREHOLE using either a  mean Vs value or with regression - powerlaw - function between f0 and depth. See Van Noten et al. 2019 for explanation of the methodology. The figure in below shows the output of the script:

<img src="https://github.com/KoenVanNoten/HVSR_to_virtual_borehole/blob/master/A201.png" width="550" height="400" />

## 4.HVSR polarisation.py:
The H/V rotational module in Geopsy computes the azimuth in which the resonance frequency has a maximum amplitude. To facilate reading this polarisation, this python script plots the variance of the amplitude with azimuth in a polar plot. The IDs to plot will be loaded from the HVSR database file. Polarisation data (Amax, Amin and their corresponding azimuths and frequencues) will be exported to a seperate file which then can be visualised in a GIS.
Output:
<img src="https://github.com/KoenVanNoten/HVSR_to_virtual_borehole/blob/master/A201_polarisation.png" width="500" height="350" />
