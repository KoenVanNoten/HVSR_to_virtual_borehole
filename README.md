# HVSR_to_virtual_borehole

1. Conduct H/V spectral ratio analyses from gathered ambient noise measurements in Geopsy and save the output of Geopsy as .hv file.

2. Do that xxx times for the entire database and update your database file (see HVSR database.csv) with the necessary information (ID, Filename, altitude of measurements, ...)

# Get f0s from geopsy hv files.py
3. Load all HVSR data (min f0, f0, max f0, error, max Amplitude, n of windows) automatically from all .hv files listed in the database file. The default setting of Geopsy to export the H/V spectrum is set to 100 samples (100 freq. and Amplitude values), no matter the range in the output frequency sampling. If this default sampling setting is used, a wide output range, e.g. 0.5 Hz to 50 Hz, will pick f0 less accurately than if a narrow range around the peak amplitude is selected. To increase the f0 picking accuracy, one can increase the sample setting to the maximum (e.g. 9999 samples in Geospy) in Geopsy. Or one can resample the Geopsy output curve by a performing a linear interpolation up to 15000 samples (interpolation used in this script). This results in a slightly different interpolated amplitude maximum and f0 than the one exported by Geopsy. The interpolated values will be exported to the databse file.

# f0_to_virtual_borehole.py: 
4. Script to replot one or all .hv files into a f0 versus amplitude plot and to convert the H/V spectrum to a VIRTUAL BOREHOLE using either a  mean Vs value or with regression - powerlaw - function between f0 and depth. See Van Noten et al. 2019 for explanation of the methodology. The figure in below shows the output of the script:

<img src="https://github.com/KoenVanNoten/HVSR_to_virtual_borehole/blob/master/A201.png" width="550" height="400" />

