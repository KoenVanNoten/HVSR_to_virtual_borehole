import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import csv
import os
import pandas as pd
from scipy.interpolate import griddata
#from scipy.stats import powerlaw
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import interp1d

in_filespec = r'HVSR 2018 field notes.csv'
# in_folder = r'C:\BGD\HVSR\HV 2018 Anderlecht\20180718 site survey'

out_filespec = os.path.splitext(in_filespec)[0] + "_f0_from_hv.csv"

koensfile = pd.read_csv(in_filespec)

for _ in ["f0_min", "f0_win", "f0_average", "f0_ip", "f0_ip_diff", "error", "f0_max", "A0", "nw"]:
    koensfile[_] = 0.

output = []
for id, row in koensfile.iterrows():
    print (row["Filename"] + ".hv")
    df = pd.read_csv(row["Filename"] + ".hv", nrows=5, skiprows=1, header=None)
    Filenr = row["Filename"] + ".hv"
    rows = ["num", "f0_avg", "num_f0", "f0s", "peak_amp"]
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

    # Interpolate data to have a smoothed HVSR curve
    #        df = pd.read_csv(Filenr, nrows=100,skiprows=9, header=None)
    #        rows = ["Frequency","Average"]
    #        print df
    HV_data = np.genfromtxt(Filenr, delimiter='\t', usecols=(0, 1))
    f_orig = HV_data[:, 0]
    A_orig = HV_data[:, 1]
    func = interp1d(f_orig, A_orig, 'cubic')
    f_new = np.linspace(f_orig[0], f_orig[-1], 15000)
    A_new = func(f_new)
    maxx = np.argmax(A_new)
    f0_ip_diff = f_new[maxx] - data["f0_win"]
    print "f0_ip - f0_win = ", f0_ip_diff
    print data["f0_win"]
    koensfile.loc[id, "f0_min"] = data["f_min"]
    koensfile.loc[id, "f0_win"] = data["f0_win"]
    koensfile.loc[id, "f0_average"] = data["f0_avg"]
    koensfile.loc[id, "f0_ip"] = f_new[maxx]
    koensfile.loc[id, "f0_ip_diff"] = f0_ip_diff
    koensfile.loc[id, "error"] = data["error"]
    koensfile.loc[id, "f0_max"] = data["f_max"]
    koensfile.loc[id, "A0"] = data["peak_amp"]
    koensfile.loc[id, "nw"] = data["num"]

# print(koensfile.head())
# print data["f_min"]

koensfile.to_csv(out_filespec)