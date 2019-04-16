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



'''
run = 1
size_on = 0


Color = 'jet'
#Color = 'viridis'
northings = []
eastings = []
f0_all = []
size = []
depth = []
z = []

if run:
    with open(in_filespec) as file:

	HV_data = csv.reader(file)
	HV_results = open(out_filespec, "wb")
	writer = csv.writer(HV_results)
		
	header = True
	total_n = 0
	for HV in HV_data:
		#Defining the headers in the picked file:
		if header:
			name_column = HV.index('name')
			easting_column = HV.index('Easting')
			northing_column = HV.index('Northing')
			Filename_column = HV.index('Filename')
			f0min_column = HV.index('f0min')
			f0_column = HV.index('f0')
			f0_average_column = HV.index('f0_average')
			error_column = HV.index('error')
			f0max_column = HV.index('f0max')
			A0_column = HV.index('A0')
			nw_column = HV.index('nw')
			z_column = HV.index('DEM')
			writer.writerow(HV)#writing the header of the file
			header = False
		else:

                        total_n += 1 # total_n = total_n + 1
                        Filename = HV[Filename_column]
#                        print Filename
                        eastings.append(HV[easting_column])
                        northings.append(HV[northing_column])
                        z.append(float(HV[z_column]))
                       ###load hv files 
                        HV_indiv = in_folder + '\%s'%Filename + ".hv"
                        
                        for line in open(HV_indiv):
                            if line.startswith('# f0 from windows'):
                                 split = line.strip().split('\t')
                                 f0min = float(split[2])
                                 HV.insert(f0min_column, f0min)
                                 f0 = float(split[1])
                                 HV.insert(f0_column, f0)
                                 f0max = float(split[3])
                                 HV.insert(f0max_column, f0max)
                                 error = float(f0 - f0min)
                                 HV.insert(error_column, error)
                                 if size_on: 
                                    s = f0*(1/error)*15
                                 else:
                                    s = 50
                                 print "        f0min = ", f0min
                                 print "        f0=", f0
                                 print "        f0max =", f0max, type(f0max)
                                 print "        error =", error
                                 print "        thickness =", h
                                 size.append(s)
                                 f0_all.append(f0)
#                                 paleo_tops.append(paleo_top)
#                                 paleo_top = DEM - h
                            if line.startswith('# f0 from average'):
                                 split = line.strip().split('\t')
                                 f0_average = float(split[1])
                                 HV.insert(f0_average_column, f0_average)
                                 print "        f0_average = ", f0_average
                                 h = 94.228*np.power(f0_average,-1.758)
                                 depth.append(h)
                            if line.startswith('# Peak amplitude'):
                                 split = line.split('\t')
                                 A0 = float(split[1])
                                 print "        A0 = ", A0
                                 HV.insert(A0_column, A0)
                            if line.startswith('# Number of windows='):
                                 split = line.split('# Number of windows=')
                                 nw = int(split[1])
                                 HV.insert(nw_column, nw)
                                 print Filename, ", nw = %s"%nw
                        writer.writerow(HV)

    print "n= ", total_n
else: 
    picked_data = np.genfromtxt(out_filespec, skip_header = 1, delimiter=',', usecols=(2, 3, 7, 8, 14,15), names = ['Easting', 'Northing', 'DEM', 'Filename','f0', 'error'])
    eastings = picked_data['Easting']
    northings = picked_data['Northing'] 
    z = picked_data['DEM']
    error = picked_data['error']
    f0_all = picked_data['f0']
    if size_on:
        size = f0_all*(1/error)*15
    else:
        size = 30
depth = 94.228*np.power(f0_all,-1.758)
paleotopo = np.array(z)-np.array(depth)
print size
#print f0_all
#print eastings, northings
#print depth
#print z
#print np.array(z)-np.array(depth)


# Main plot
gs = gridspec.GridSpec(3, 2, hspace = 0.3, top = .94)
###Only dense network
#xmax = 152000
#xmin = 146000
#ymax= 163500
#ymin = 159000
##with dworp boreholes
xmax = 152000
xmin = 142000
ymax= 163500
ymin = 157000

def plot_data(z,  title, ax):
    plt.scatter(eastings, northings, c = z, cmap = Color, s = size)
    scatter = plt.scatter(eastings, northings, c = z, cmap = Color)
    cb = plt.colorbar(scatter, cmap = Color)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
#    plt.axis('equal')
    plt.title(title)
    ax.xaxis.set_major_locator(MultipleLocator(base=2000.))
    ax.yaxis.set_major_locator(MultipleLocator(base=1000.))
    
ax0 = plt.subplot(gs[0])
plot_data(f0_all, "Resonance map", ax0)

ax2 = plt.subplot(gs[2])
plot_data(depth, "Thickness map", ax2)

ax4 = plt.subplot(gs[4])
plot_data(paleotopo, "Altitude paleotop BM", ax4)

def interpol(z, ylabel, title, ax):
        npts = 1000
        xi = np.linspace(xmin, xmax, npts)
        yi = np.linspace(ymin, ymax, npts)
        zi = griddata((eastings, northings), z, (xi[None,:], yi[:,None]), method='linear')
    # contour the gridded data, plotting dots at the randomly spaced data points.
        CS = plt.contour(xi,yi,zi,15,linewidths=0.1,colors='k')
        CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
        cb = plt.colorbar()
        cb.ax.set_ylabel(ylabel, fontsize=12)
        plt.scatter(eastings,northings,marker='o',c='black',s=0.5)
        plt.title(title + ' map')
        ax.xaxis.set_major_locator(MultipleLocator(base=2000.))
        ax.yaxis.set_major_locator(MultipleLocator(base=1000.))

#        plt.axis('equal')

ax1 = plt.subplot(gs[1])
interpol(f0_all, "Frequency", "Resonance",ax1)

ax3 = plt.subplot(gs[3])
interpol(depth, "Thickness", "Sediment thickness", ax3)

ax5 = plt.subplot(gs[5])
interpol(paleotopo, "Altitude (m TAW)", "Paleotop BM", ax5)

#ax6 = plt.subplot(gs[7])
#size = 1
#plot_data(error,  "Error", ax6)

plt.show()

gs = gridspec.GridSpec(1, 1, hspace = 0.3, top = .94)
ax6 = plt.subplot(gs[0])
interpol(paleotopo, "Depth", "Paleotop BM", ax6)
plt.show()
'''