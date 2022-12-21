# coding=utf-8
###  	Koen Van Noten
###  	Royal Observatory of Belgium
###  	PLOTTING ROTATIONAL H/V RESULTS FROM the .hv module of GEOPSY

### Van Noten, K., Lecocq, T. Gelis, C., Meyvis, B., Molron, J., Debacer, T.N., Devleeschouwer, X. 2022.
### Brussels’ bedrock paleorelief from borehole-controlled powerlaws linking polarised H/V resonance frequencies and sediment thickness.
### Journal of Seismology. https://doi.org/10.1007/s10950-021-10039-8

### This script loads one or all Geopsy HV grid files by reading the ID column from the database.from the Geopsy HV rotate module and exports it into the database
### All rotational data then is exported to the database file named database_file & _polarisation_export.csv
### Following data is exported:
### HEADERS: A_max, max_freq, max_Azi, A_min, min_freq, min_Azi
### A_max: maximum amplitude at resonance frequency deduced from the HVSR polarisation analysis (see Fig. 4 of paper)
### max_freq: Resonance frequency at A_max
### max_Azi: Azimuth at which resonance frequency is maximum (deduced from polarisation analysis)
### A_min: minimum amplitude at resonance frequency deduced from the HVSR polarisation analysis (see Fig. 4 of paper)
### min_fre q:  Azimuth at which resonance frequency is minimal (deduced from polarisation analysis)
### min_Azi: Azimuth at which resonance frequency is minimum (deduced from polarisation analysis)

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

### load the database containing the ID names (The "Filename" column will be used for loading the data
database_file = 'HVSR database file_f0_from_hv.csv'
in_folder = 'Data' #Folder containing the Geopsy HV rotate module grid exported files

### choose to export all grid data from the database list or only one specific ID given in below
### if plot_all is True, rotational data will be exported to a "HVSR rotation.csv" file
export_all = 1	#False = manual search
IDs = ['A201', 'A202']  #list of data in manual search

# If freq_range = False, find the maximum rot values around the resonance frequency
# If freq_range = True, search for the maximum rot values in a certain frequency range.
freq_range = 0
f_range = [1.15, 1.4]

################################################
# Main program
################################################

rot_data = []

def export_rotationaldata(in_filespec,ID):
    df = pd.read_csv(in_filespec, delimiter=' ', skiprows=0, engine = 'python')
    freq = df["x"]
    Azi = df["y"]
    A = df["val"]

    ## Get the rotation step. Default = 10° in Geopsy. Can be changed since Geopsy version 3.3.3
    groups = df.groupby(Azi)
    rotation_classes = len(groups) ## gives the amount of rotation step classes. = 19 for 10° steps
    rotation_step = int(180/(rotation_classes-1)) ## gives the rotation_step

    ### find the polarization by searching for maximum amplitude for each azimuth
    Amax = []
    freqmax = []
    Azimax = []

    for i in np.arange(0,180+rotation_step,rotation_step):
        index = np.array(np.where((Azi == i)))[0]

        ## search for maximum and minimum A0 in a given frequency range
        if freq_range:
            index_range = []
            for ind in index:
                if freq[ind] >= f_range[0]:
                    if freq[ind] <= f_range[1]:
                        index_range.append(ind)
            index = index_range

        ## find maximum amplitude of each angle (0--> 180) so we later can find the max and min value in this list
        ## append the max Amplitude in the i angle
        Amax.append(np.max(A[index]))
        ## append the frequency corresponding to that amplitude
        freqmax.append(freq[index[0] + np.argmax(A[index])])
        ## append the angle to a list
        Azimax.append(i)
        ## find the maximum in the max amplitude list
        A_max = np.max(Amax)

    #find the minima and maxima (white and red dots in the plot)
    max_freq = freqmax[np.argmax(Amax)]
    max_Azi = Azimax[np.argmax(Amax)]
    A_min = np.min(Amax)
    min_freq = freqmax[np.argmin(Amax)]
    min_Azi = Azimax[np.argmin(Amax)].transpose()

    #store the data
    rot_data.append([A_max, max_freq, max_Azi,A_min, min_freq, min_Azi])
    print(ID, round(A_max,2), round(max_freq,2),round(max_Azi,2),round(A_min,2),round(min_freq,2), min_Azi)

##### plot all rotational data & apply the definition
print('ID', 'A_max', 'max_freq', 'max_Azi','A_min', 'min_freq', 'min_Azi')

if export_all:
    df2 = pd.read_csv(database_file, delimiter=',', skiprows=0, engine = 'python')
    IDs = df2["Filename"]

    for i in IDs:
        HV_file = os.path.join(in_folder, '%s' % i)
        # in earlier Geopsy versions the rotation data was saved without extension
        try:
            export_rotationaldata(HV_file, i)
        # in newer Geopsy versions the rotation data is saved as .grid extension
        except BaseException as e:
            HV_file = os.path.join(in_folder, '%s.hv.grid' % i)
            export_rotationaldata(HV_file, i)
            pass

    # Export the polarisation data and add it to the HVSR database
    out_filespec = os.path.splitext(database_file)[0] + "_polarisation_export.csv"
    outputfile = pd.read_csv(database_file)
    df_polarisation = pd.DataFrame(rot_data, columns = ['A_max', 'max_freq', 'max_Azi','A_min', 'min_freq', 'min_Azi'])
    outputfile = outputfile.join(df_polarisation)
    outputfile.to_csv(out_filespec, index = False)

else:
    IDs = IDs
    df2 = pd.read_csv(database_file, delimiter=',', skiprows=0, engine='python', index_col = "Filename")

    for i in IDs:
        HV_file = os.path.join(in_folder, '%s' % i)

        # in earlier Geopsy versions the rotation data was saved without extension
        try:
            export_rotationaldata(HV_file, i)
        # in newer Geopsy versions the rotation data is saved as .hv.grid extension
        except BaseException as e:
            HV_file = os.path.join(in_folder, '%s.hv.grid' % i)
            export_rotationaldata(HV_file, i)
            pass

    # Export the polarisation data and add it to the HVSR database
    out_filespec = os.path.splitext(database_file)[0] + "_polarisation_export.csv"
    outputfile = pd.read_csv(database_file)
    df_polarisation = pd.DataFrame(rot_data, columns=['A_max', 'max_freq', 'max_Azi', 'A_min', 'min_freq', 'min_Azi'])
    outputfile = outputfile.join(df_polarisation)
    outputfile.to_csv(out_filespec, index=False)

print(" ")
print("Export Done")