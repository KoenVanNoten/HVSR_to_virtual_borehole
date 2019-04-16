import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import csv
import os
import matplotlib.path as mpath
import matplotlib.collections as mcoll
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
#from scipy.stats import powerlaw
from matplotlib.ticker import MultipleLocator

### HVSR 2007 Brussels Celine
# all_data = r'C:\BGD\HVSR\HV Brussels Petermans\HVRS Petermans Bxl_redo_CG\HVSR 2017 field notes.csv'
# all_folder = r'C:\BGD\HVSR\HV Brussels 2017 campaign\HVSR results\all data'
# savefolder = r'C:\BGD\HVSR\HV Brussels 2017 campaign\HVSR Spectra'

# ### HVSR 2017 Brussels
all_data = r'C:\BGD\HVSR\HV Brussels 2017 campaign\HVSR results\all data\HVSR 2017 all 20180407.csv'
all_folder = r'C:\BGD\HVSR\HV Brussels 2017 campaign\HVSR results\all data'
savefolder = r'C:\BGD\HVSR\HV Brussels 2017 campaign\HVSR Spectra'

plot_one = 1
ID = 'A258'


#Powerlaw Bxl Justine Molron
#a_pw = 94.228
#b_pw = -1.758

#New Powerlaws Bxl Koen Van Noten
#All
a_pw = 89.0 #new EGU all
b_pw = -1.680

# a_pw = 87.85 #new EGU indiv Bxl
# b_pw = -1.73

# a_pw = 94.606 #old excel
# b_pw = -1.634

#Separated
a_SHH_Bxl = 94.606      #Shh-Ld-Mal-Bxl
b_SHH_Bxl = -1.634

#a_Al = 88.604   #Alluvial above Moen and Brussels
#b_Al = -1.667

#a_StM = 
#b_Stm =    #St-Maur

##### Christian Anderlecht
#all_data = r'C:\BGD\HVSR\HV KBIN\HVSR Anderlecht 20170919.csv'
#all_folder = r'C:\BGD\HVSR\HV KBIN'
#savefolder = r'C:\BGD\HVSR\HV KBIN'
##Powerlaw Kortrijk Formation
#a_pw = 83.147
#b_pw = -1.278

##### HVSR Powerlaw paper
#all_data = r'C:\OMA\VanNotenetal2017 BW Site effects\F0 data selection_without bxl.csv'
#savefolder = r'C:\OMA\VanNotenetal2017 BW Site effects\HVSR results'

#HVSR Prodigy paper
#all_folder = r'C:\OMA\Lecocqetal Prodigy\\HVSR prodigy & mac'
#all_file = 'Prodigy files.csv'
#savefolder = r'C:\OMA\Lecocqetal Prodigy\HVSR prodigy & mac'

#all_data = all_folder + '\%s'%all_file
#print all_data


#data selection
def make_segments(x, y):
    '''
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    '''
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    return segments

def colorline(x, y, z, cmap=plt.get_cmap('copper'), linewidth=10, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """
    z = np.asarray(z)
    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, linewidth=linewidth, alpha=alpha)

    ax = plt.gca()
    ax.add_collection(lc)

    return lc

def plot_data(in_filespec,ID):
    data = np.genfromtxt(in_filespec, delimiter='\t', usecols=(0,1,2,3))
    f_orig = f = data[:,0]
    A_min = data[:,2]
    A_orig = A = data[:,1]
    A_max = data[:,3]
    NaNs = np.isnan(data)
    data[NaNs] = 0

    #Interpolate data to have a smoothed HVSR curve
    func = interp1d(f_orig, A_orig, 'cubic')
    f_new = np.linspace(f_orig[0], f_orig[-1],15000)

    A_new = func(f_new)
#    A = np.interp(f, f_orig, A_orig)
    func = interp1d(f_orig, A_min, 'cubic')
    A_min = func(f_new)
    func = interp1d(f_orig, A_max, 'cubic')
    A_max = func(f_new)
#    print "A_max: ", A_max
    A_orig = A = A_new
    f_orig = f = f_new
    A_plot = A*0

    #plotter
    gs = gridspec.GridSpec(1, 2, width_ratios=[12, 1])
    plt.suptitle(ID)
    ax0 = plt.subplot(gs[0])
#    plt.plot(A,f, linewidth=0.8)
    plt.plot(A_new,f_new, linewidth=0.7)
    maxx = np.argmax(A_new)
#    maxx = 265   #overwrite atuomatic Amplitude
    print("maxx: ", maxx, A_new[maxx], f_new[maxx])
#    plt.axhline(f_new[maxx], c='g', ls='--')
    plt.fill_betweenx(f, A_min, A_max, color = 'lightgrey', zorder = -100)
    ax0.set_yscale('log')
    colorline(A_plot, f, A, cmap='viridis', linewidth=5)
    colorbar = colorline(A_plot, f, A, cmap='viridis', linewidth=10)
    plt.colorbar(colorbar, cmap = 'viridis', label = "Amplitude")

    #plot f0
    A_max = np.max(A)
#    A_max = np.where(np.max(A)[0.8,1.2])
    with open(in_filespec) as file:
            for line in file:
                    columns = line.split()
                    if line.startswith('# f0 from average'):
                                 split = line.strip().split('\t')
                                 f0_average = float(split[1])
                                 print ("f0_avg: {}".format(f0_average))
                    if line.startswith('# Peak amplitude'):
                                 split = line.split('\t')
                                 A0 = float(split[1])
                    if line.startswith('# f0 from windows'):
                                 split = line.strip().split('\t')
                                 f0min = float(split[2])
                                 print (f0min)
                                 f0 = float(split[1])
                                 print ("f0_win: %s"%f0)
                                 error = float(f0 - f0min)
                                 print (error)
 

#    f_new[maxx] = 0.956061     #overwrite automatic frequency picking
#     plot the horizontal line for the average
#    plt.axhline(y=f0_average, xmin=0, xmax=20,color = 'red', linewidth=0.5, hold=None, zorder = -100)
    #plot the horizontal line for the interpolation
    plt.axhline(y=f_new[maxx], xmin=0, xmax=20,color = 'red', linewidth=0.5, hold=None, zorder = -100)
    f0_min = float(f0_average - error)
    f0_max = float(f0_average + error)
    plt.axhline(y=f0_min, xmin=0, xmax=20,color = 'grey', linewidth=0.5, ls = '--', hold=None, zorder = -100)
    plt.axhline(y=f0_max, xmin=0, xmax=20,color = 'grey', linewidth=0.5, ls = '--', hold=None, zorder = -100)   
#    # title for f0
#    plt.title("$f_0$_graph: %.2f"%f0_average + "; $f_0$: %.3f"%f0 + r"$\pm$%.3f"%error + "(err)" +
    # r"$\pm$%.3f"%(f_new[maxx]-f0_average)+ "($f_0$ip); " + "$A_0$: %.2f"%A0, size = 10)
    # Title for f0 interpolated
    # plt.title("$f_0$_graph: %.3f"%f0_average + "; $f_0$ interpolated: %.3f"%f_new[maxx] + r"$\pm$%.3f"%error + "(err)" +
    #           r"$\pm$%.3f"%(f0 - f_new[maxx])+ "($f_0$); " + "$A_0$: %.2f"%A0, size = 10)
    plt.title("$f_0$ int.: %.3f" % f_new[maxx] + r"$\pm$%.3f" %error + "(err)" + "; $A_0$: %.2f" % A0, size=10)
    print ("$f_0$_ip = ", f_new[maxx])
    plt.ylabel("Frequency (Hz)", fontsize=10)
    plt.xlabel("Amplitude", fontsize=10)
    plt.xlim(-1,20)
    plt.ylim(0.5,50)
  
  #Making a depth plot
    ax1 = plt.subplot(gs[1])
    h = a_pw*np.power(f,b_pw)
    depth_min = a_pw*np.power(f0_min,b_pw)
    depth_max = a_pw*np.power(f0_max,b_pw)
#    depth = a_pw*np.power(f0_average,b_pw)
    depth = a_pw*np.power(f_new[maxx],b_pw)
    depth_f0max = a_pw*np.power(f_new[maxx],b_pw)
    altitude = Z - depth
    altitude_min = Z - depth_min 
    altitude_max = Z - depth_max
    altitude_f0max = Z - depth_f0max 
    all_depths = Z - h
#    print "Z: ", Z 
#    print "altitude: ", altitude, "(range: ", altitude_min, ", ", altitude_max, ")"
    
    colorline(A_plot, all_depths, A_new, cmap='viridis', linewidth=50)
    plt.ylim(Z+10, Z-depth-20)   
    plt.gca().invert_yaxis()
    plt.ylabel("Altitude bedrock (m TAW)", fontsize=10)
    ax1.axes.get_xaxis().set_ticks([])
    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()
    savefile = savefolder + '\%s'%ID + ".png"
    plt.title("Bedrock at %.0f"%(depth) + " m", size = 10)
        ##alternative depth from f0 interpolated
#    plt.title("BM at %s"%int(depth) + "or %s"%int(depth_f0max) + " m", size = 10)
    plt.axhline(y=altitude, xmin=0, xmax=20,color = 'red', linewidth=0.8, hold=None, zorder = 100)
    plt.axhline(y=altitude_min, xmin=0, xmax=20,color = 'black', linewidth=0.8, hold=None, zorder = 100)
    plt.axhline(y=altitude_max, xmin=0, xmax=20,color = 'black', linewidth=0.8, hold=None, zorder = 100)
        # plot horizontal line from f0 picked from the interpolated maximum
#    plt.axhline(y=altitude_f0max, xmin=0, xmax=20,color = 'purple', linewidth=0.8, hold=None, zorder = 100)
    plt.axhline(y=Z, xmin=0, xmax=20,color = 'black', linewidth=0.7, hold=None, zorder = 100)
    plt.annotate('%s'%int(Z) + " m", xy=(0.,Z), fontsize = 8)
    plt.savefig(savefile, format= 'png', dpi = 600)


if plot_one:            # Find filename from ID nr & convert 1 HVSR
    keys = [] 	#ID's 
    name = []
    HV_name = []
    Z_indiv = []
    with open(all_data) as file:
            next(file)
            for line in file:
                    columns = line.split(',')
                    name.append((columns[2]))	#name the ID column
                    HV_name.append(columns[15])	#name the filename column
                    Z_indiv.append(float(columns[8]))   # altitude from AGIV DEM model
    index = name.index(ID)      # index the ID line that has to be searched
    filename = HV_name[index]
    Z = Z_indiv[index]       # find name based on the nr
    in_filespec = all_folder + '\%s'%filename + '.hv'
    print (in_filespec)
    plot_data(in_filespec, ID)
else:                   #plot all HVSR data
    with open(all_data) as file:
                next(file)
                for line in file:
#                    print line
                    columns = line.split(',')
                    HV_name = columns[15]
                    ID = columns[2]
                    Z = float(columns[8])
#                    print np.dtype(columns[7])
                    print (HV_name)
#                    print Z
                    plot_data(all_folder + '\%s'%HV_name + '.hv', ID)

plt.show()