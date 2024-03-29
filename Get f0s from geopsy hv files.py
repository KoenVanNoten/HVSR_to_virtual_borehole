### Koen Van Noten - Royal Observatory of Belgium
### HVSR to Virtual Borehole: loading f0 from .hv Geopsy files
### Version 0.0: August 2017 - python 2
### Version 1.0: April 2020 - python 3

### Van Noten, K., Lecocq, T. Gelis, C., Meyvis, B., Molron, J., Debacer, T.N., Devleeschouwer, X. 2022.
### Brussels’ bedrock paleorelief from borehole-controlled powerlaws linking polarised H/V resonance frequencies and sediment thickness.
### Journal of Seismology - https://doi.org/10.1007/s10950-021-10039-8

### This script loads all following Geopsy .hv information into a database file
### f0_min	f0_win	f0_average	f0_ip	f0_ip_diff	error	f0_max	A0	nw

### #f0 min: f0_win/stddev (from GEOPSY)
### #f0_win: average resonance frequency by taking the f0 of each individual window and averaging all f0 values from these windows (from GEOPSY)
### f0 average: scanning the average curve and identifying the frequency at which the maximum amplitude occurs (from GEOPSY)
### f0_ip: resonance frequency computed after interpolating the HV-Amplitude graph using python (see paper)
### f0_ip_diff: difference between f0_ip and f0_win
### error: standard deviation on f0 (from GEOPSY)
### f0 max: f0_win.stddev (from GEOPSY)
### A0: maximum amplitude (from GEOPSY)
### nw: number of windows (from GEOPSY)

import numpy as np
import os
import pandas as pd
from scipy.interpolate import interp1d

# read the database file in which all the names of the .hv 	measurements are stored
database_file = 'HVSR database file.csv'
in_folder = 'Data' #folder containing all .hv data

out_filespec = os.path.splitext(database_file)[0] + "_f0_from_hv.csv"
outputfile = pd.read_csv(database_file)
outputfile.head()

#### Initializing empty columns that need to be filled from the Geopsy .hv files
for _ in ["f0_min", "f0_win", "f0_average", "f0_ip", "f0_ip_diff", "error", "f0_max", "A0", "nw"]:
	outputfile[_] = 0.

output = []

#### loop through each .hv datafile
for id, row in outputfile.iterrows():
	HV_file = os.path.join(in_folder, row["Filename"] + ".hv")
	print(HV_file)
	df = pd.read_csv(HV_file, nrows=5, skiprows=1, header=None) #opening the .hv file
	rows = ["num", "f0_avg", "num_f0", "f0s", "peak_amp"] #define rows to write in the output file
	data = {}
	for row in rows:
		data[row] = ""
	delims = ["=", "\t", "=", "\t", "\t"]
	for id2, item in df.iterrows():
		XXX = item[0].split(delims[id2])
		data[rows[id2]] = np.asarray(XXX[1:], dtype=float).flatten()
	data["f0_win"], data["f_min"], data["f_max"] = data["f0s"]
	del data["f0s"]
	data["error"] = data["f0_win"] - data["f_min"]
	data["f0_avg"] = data["f0_avg"][0]
	data["peak_amp"] = data["peak_amp"][0]
	data["num"] = data["num"][0]
	data["num_f0"] = data["num_f0"][0]

	# In the default setting, Geopsy only exports 100 frequency-amplitude samples for the computed HVSR curve.
	# One can increase this number by:
	#   - either increasing the sample numbers in geopsy (max = 9999)
	#   - or by interpolating between the samples and improve the accuracy of picking f0 (this script)
	# Increasing the samples in Geopsy to 9999 gives the same results, but one might have forgotten to do this
	# so this interpolation offers a nice twist to solve this.

	# The part in below executes the interpolation up to 15000 samples
	# See paper Van Noten et al. for more information. Same method is applied in the HVSR_to_virtual_borehole module
	HV_data = np.genfromtxt(HV_file, delimiter='\t', usecols=(0, 1))
	f_orig = HV_data[:, 0] #original frequency data
	print("nr of samples:", len(f_orig))
	A_orig = HV_data[:, 1] #original amplitude data
	func = interp1d(f_orig, A_orig, 'cubic') #IN
	f_new = np.linspace(f_orig[0], f_orig[-1], 15000) #interpolation for 15000 samples
	A_new = func(f_new) #defining the function for the new Amplitude
	maxx = np.argmax(A_new)

	# With the interpolated data new columns can be calculated to compare the interpolated values and the ones provided by Geopsy
	f0_ip_diff = f_new[maxx] - data["f0_win"] #difference between f0_interpolated and f0_geopsy

	#write all data to the database file
	outputfile.loc[id, "f0_min"] = data["f_min"] #f0 min
	print("f0_min:", round(data["f_min"],3), "Hz")
	outputfile.loc[id, "f0_win"] = data["f0_win"] #average f0 computed by averaging the peak f0 values of all individual windows
	print("f0_win:", round(data["f0_win"],3), "Hz")
	outputfile.loc[id, "f0_average"] = data["f0_avg"] #f0 corresponding to the maximum amplitude of the average f0 - Amplitude curve
	print("f0_average:", round(data["f0_avg"],3), "Hz")
	outputfile.loc[id, "f0_ip"] = f_new[maxx] #interpolated f0 from 15000 samples
	print("f0_ip:", round(f_new[maxx],3), "Hz")
	outputfile.loc[id, "f0_ip_diff"] = f0_ip_diff #difference between f0_interpolated and f0_win
	print ("f0_ip_diff:", round(f0_ip_diff,3), "Hz")
	outputfile.loc[id, "error"] = data["error"] #error on f0_win in Geopsy
	print("error:", round(data["error"],3), "Hz")
	outputfile.loc[id, "f0_max"] = data["f_max"] #f0 max
	print("f0_max:", round(data["f_max"],3), "Hz")
	outputfile.loc[id, "A0"] = data["peak_amp"] #A0
	print("A0:", round(data["peak_amp"],3))
	outputfile.loc[id, "nw"] = data["num"] #number of windows used to compute f0
	print("nw:", int(data["num"]), "windows")
	print('')

outputfile.to_csv(out_filespec, index = False)