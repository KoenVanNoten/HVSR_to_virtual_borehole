### Koen Van Noten - Royal Observatory of Belgium
### HVSR to Virtual Borehole
### Version 0.0: August 2017 - python 2
### Version 1.0: April 2019 - python 3

### Van Noten, K., Lecocq, T. Gelis, C., Meyvis, B., Molron, J., Debacer, T.N., Devleeschouwer, X. submitted.
### Brussels’ bedrock paleorelief from borehole-controlled powerlaws linking polarised H/V resonance frequencies and sediment thickness.
### Journal of Seismology

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.collections as mcoll
from scipy.interpolate import interp1d

# ### Load the HVSR data and the database csv overviewfile from the folder
all_data = 'HVSR database file.csv'

# Plot only one Virtual Borehole with the ID given (ID & .hv file need to be in the database file)
# If plot_one = 0; all .hv files will be plotted as a Virtual Borehole
plot_one = 1
ID = 'A202'

# Choose if you want to use the Geopsy values or want to interpolate between 0 and 15000 frequency values
# See annotations in "Get f0s from geopsy hv files.py" for more information
interpolate = 1

## f0 needs to be converted to depth by: e.g. using a Powerlaw relation between resonance frequency and depth
## according to the formula: h = a * power(f0, b)
## a & b values of the Regional powerlaw relation (R') of Van Noten et al. 2019.
a_pw = 88.631     # a value
b_pw = -1.683    # b value

#################################
# Main Program
#################################

#data selection
def make_segments(x, y):
    """"
    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array
    """
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

def plot_data(in_filespec,ID, Z):
    ### load data
    df = pd.read_csv(in_filespec, delimiter='\t', skiprows=9, names=['Frequency', 'Average', 'Min', 'Max'])
    f = df["Frequency"]
    A_min = df['Min']
    A0 = df['Average']
    A_max = df['Max']
    NaNs = np.isnan(df)
    df[NaNs] = 0

    ### Instead of using the output of Geopsy, one can interpolate the entire HVSR curve for 15000 points to improve f0
    if interpolate:
        # interpolate for A0
        func = interp1d(f, A0, 'cubic')
        f_ip = np.linspace(f[0], f[len(f) - 1], 15000)
        A0_ip = func(f_ip)

        # interpolate for A_min
        func = interp1d(f, A_min, 'cubic')
        A_min_ip = func(f_ip)

        # interpolate for A_max
        func = interp1d(f, A_max, 'cubic')
        A_max_ip = func(f_ip)

        # overwrite original f, A0
        A0 = A0_ip
        f = f_ip
        A_min = A_min_ip
        A_max = A_max_ip

    A_plot = A0 * 0

    ### Plot the Amplitude - frequency diagram and the virtual borehole
    gs = gridspec.GridSpec(1, 2, width_ratios=[12, 1])
    plt.suptitle(ID)
    ax0 = plt.subplot(gs[0])
    plt.plot(A0,f, linewidth=0.7)
    maxx = np.argmax(A0)
    print("index max:", maxx, "A0:", round(A0[maxx],2), "fmax: ",round(f[maxx],2))
    plt.fill_betweenx(f, A_min, A_max, color = 'lightgrey', zorder = -100)
    ax0.set_yscale('log')
    colorline(A_plot, f, A0, cmap='viridis', linewidth=5)
    colorbar = colorline(A_plot, f, A0, cmap='viridis', linewidth=10)
    plt.colorbar(colorbar, cmap = 'viridis', label = "Amplitude")


    #### function to find and plot f0 values from the geopsy files
    #A_max = np.max(A0) # find largest amplitude in the geopsy or interpolated values
    #A_max = np.where(np.max(A)[0.8,1.2])   # sometimes amplitude is higher at other values dan f0, avoid this by defining a range in which we need to search

    with open(in_filespec) as file:
            for line in file:
                    if line.startswith('# f0 from average'):
                                 split = line.strip().split('\t')
                                 f0_average = float(split[1])
                                 print ("f0_average: %s"%round(f0_average,3)) #average f0 picked by geopsy
                    if line.startswith('# Peak amplitude'):
                                 split = line.split('\t')
                                 A0_geopsy = float(split[1]) #A0 picked by geopsy
                    if line.startswith('# f0 from windows'):
                                 split = line.strip().split('\t')
                                 f0min = float(split[2])
                                 print ("f0 min: %s"%round(f0min,2))
                                 f0 = float(split[1])
                                 print ("f0_win: %s"%round(f0,3))
                                 error = float(f0 - f0min)
                                 print ("error: %s"%round(error,3))
 
    if interpolate:
        ### plot a horizontal line for the average if you want to plot the interpolated f0 value
        plt.axhline(y=f[maxx], xmin=0, xmax=20, color='red', linewidth=0.5, zorder=-100)
        print("f0_ip = ", round(f[maxx], 3))
        f0_min = float(f[maxx] - error)
        f0_max = float(f[maxx] + error)
        depth = a_pw * np.power(f[maxx], b_pw)
    else:
        ### plot a horizontal line for the average if you want to plot the geopsy f0 value
        plt.axhline(y=f0_average, xmin=0, xmax=20,color = 'red', linewidth=0.5, zorder = -100)
        f0_min = float(f0_average - error)
        f0_max = float(f0_average + error)
        # convert frequency to depth using the powerlaw relation
        depth = a_pw * np.power(f0_average, b_pw)

    ### plot horizontal lines for f0_min and f0_max using the error provided by geopsy
    plt.axhline(y=f0_min, xmin=0, xmax=20, color='grey', linewidth=0.5, ls='--', zorder=-100)
    plt.axhline(y=f0_max, xmin=0, xmax=20,color = 'grey', linewidth=0.5, ls = '--', zorder = -100)
    plt.title("$f_0$ int.: %.3f" % f[maxx] + r"$\pm$%.3f" %error + "(err)" + "; $A_0$: %.2f" % A0_geopsy, size=10)
    plt.ylabel("Frequency (Hz)", fontsize=10)
    plt.xlabel("Amplitude", fontsize=10)
    plt.xlim(-1,10)
    plt.ylim(1,50)
  
    #### Making the virtual borehole in function of depth
    ax1 = plt.subplot(gs[1])
    # convert frequency to depth using the powerlaw relation for all frequencies
    h = a_pw*np.power(f,b_pw)

    #defining the errorbars in the virtual borehole
    depth_min = a_pw*np.power(f0_min,b_pw)
    depth_max = a_pw*np.power(f0_max,b_pw)

    # calculating absolute depth; Z = altitude of borehole
    bedrock = Z - depth
    bedrock_min = Z - depth_min
    bedrock_max = Z - depth_max
    all_depths = Z - h
    print ("Z: ", round(Z,2))
    print ("bedrock at", round(bedrock,1), " m (range: ", round(bedrock_min,1), "m, ", round(bedrock_max,1), "m)")

    colorline(A_plot, all_depths, A0, cmap='viridis', linewidth=50)

    plt.ylim(Z+10, Z-depth-20)
    plt.gca().invert_yaxis()
    plt.ylabel("Altitude bedrock (m TAW)", fontsize=10)
    ax1.axes.get_xaxis().set_ticks([])
    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()
    plt.axhline(y=bedrock, xmin=0, xmax=20,color = 'red', linewidth=0.8, zorder = 100)
    plt.axhline(y=bedrock_min, xmin=0, xmax=20,color = 'black', linewidth=0.8, zorder = 100)
    plt.axhline(y=bedrock_max, xmin=0, xmax=20,color = 'black', linewidth=0.8, zorder = 100)
    plt.axhline(y=Z, xmin=0, xmax=20,color = 'black', linewidth=0.7, zorder = 100)
    plt.annotate('%s'%int(Z) + " m", xy=(0.,Z), fontsize = 8)
    plt.title("Bedrock at %.0f" % (bedrock) + " m", size=10)

    #save it
    savefile = '%s' % ID + ".png"
    plt.savefig(savefile, format= 'png', dpi = 600)
    print('')

# Find filename from ID nr & convert 1 HVSR
df_database = pd.read_csv(all_data, header = 0)
name = df_database['Name']
Z = df_database['Z (DEM)']
HV_name = df_database['Filename']

if plot_one:
    filename = HV_name[(name == ID).argmax()] # find filename to plot based on the ID
    Z = Z[(name == ID).argmax()]
    in_filespec = filename+'.hv'
    print (in_filespec)
    plot_data(in_filespec, ID, Z)
    plt.show()

# plot all HVSR data
else:
    for i,j,k in zip(name,Z,HV_name):
        print(k)
        plot_data(k + '.hv', i, j)