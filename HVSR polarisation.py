# coding=utf-8
###  	Koen Van Noten
###  	Royal Observatory of Belgium
###  	PLOTTING ROTATIONAL H/V RESULTS FROM the .hv module of GEOPSY

### Van Noten, K., Lecocq, T. Gelis, C., Meyvis, B., Molron, J., Debacer, T.N., Devleeschouwer, X. submitted.
### Brussels’ bedrock paleorelief from borehole-controlled powerlaws linking polarised H/V resonance frequencies and sediment thickness.
### Journal of Seismology

import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

# ### load the database containing the ID names
all_data = 'HVSR database file_f0_from_hv.csv'

### choose to plot all files from a list or only one specific ID given in below
### if plot_all is True, rotational data will be exported to a "HVSR rotation.csv" file
plot_all = 1	#False = manual search
IDs = ['A201', 'A202']  #list of data in manual search
save_fig = 1	# save to fig (default = png)

# if auto_freq, frequency will be chosen automatically around f0
# if false, give the range of the frequency
auto_freq = 0
limfreq_min = 0.5
limfreq_max = 1.49

# manual = decide to set the maximum of the Amplitude color scale manually (and give the A_amplitude)
# if several plots need to be made, it might be easier to fix the Amplitude so that one can compare the different plots
manual = 0
A_manual = 10

# Search for the maximum values in a certain frequency range. Don't use this function when plot_all (or all freqs will be plotted in this range)
freq_range = 0
f_range = [1.15, 1.4]

# pacing of the ticks on the frequency distribution
steps = 0.2

################################################
# Main program
################################################

rot_data = []

def plot_rotationaldata(in_filespec,ID, limfreq_min,limfreq_max):
    df = pd.read_csv(in_filespec, delimiter=' ', skiprows=0, engine = 'python')
    freq = df["x"]
    Azi = df["y"]
    A = df["val"]

    ### reshape the amplitude column
    A_reshape = A.values.reshape(19,int(len(freq)/19))

    ## define the region where Amplitudes have to be plotted
    ## freq = xi; yi = Azimuth; A_rehape is amplitude
    xi = np.array([np.geomspace(np.min(freq), np.max(freq), int(len(freq)/19)),]*19)
    yi = np.array([np.arange(0,190,10),]*int(len(freq)/19)).transpose()

    ### flip the polar plot to mirror it on the W side
    yj = np.array([np.arange(180,370,10),]*int(len(freq)/19)).transpose()

    ### find the polarization by searching for maximum amplitude for each azimuth
    Amax = []
    freqmax = []
    Azimax = []

    for i in np.arange(0,190,10):
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

    ####### Let's plot
    plt.figure(figsize=(6.5,5))
    ax = plt.subplot(111, polar=True)

    ### for log plots - use fixed amplitudes for whole the dataset or use a flexible A0max for each plot
    if A0_max == 0:
        plt.pcolormesh(np.deg2rad(yi), np.log(xi), A_reshape, cmap='viridis', vmin=0, vmax=np.round(np.max(A), 0), rasterized=True)
        plt.pcolormesh(np.deg2rad(yj), np.log(xi), A_reshape, cmap='viridis', vmin=0, vmax=np.round(np.max(A), 0),rasterized=True)
    else:
        plt.pcolormesh(np.deg2rad(yi), np.log(xi), A_reshape, cmap='viridis', vmin=0, vmax=np.round(A0_max, 0), rasterized=True)
        plt.pcolormesh(np.deg2rad(yj), np.log(xi), A_reshape, cmap='viridis', vmin=0, vmax=np.round(A0_max, 0), rasterized=True)

    cbar = plt.colorbar(pad = 0.1, format = '%.0f')
    cbar.set_label('H/V Amplitude', rotation=90)

    if A_max < 10:
        format_max = round(A_max,3)
    else:
        format_max = round(A_max,2)
    if A_min < 10:
        format_min = round(A_min, 3)
    else:
        format_min = round(A_min,2)

    ##plot the min and maxima (red and white dots)
    plt.scatter(np.deg2rad(max_Azi), np.log(max_freq), c='red', edgecolor='black',
                label = "Max. Ampl. ("+ str(format_max) + ') at \n' + str(max_Azi) + '° - '
                        + str(max_Azi+180) +'° for $f_0$ ' + format(round(max_freq,2), '.2f') + 'Hz', zorder = 3)
    plt.scatter(np.deg2rad(min_Azi), np.log(min_freq), c='white', edgecolor='black',
                label = "Min. Ampl. ("+ str(format_min) + ') at \n' + str(min_Azi) + '° - ' + str(min_Azi+180) +'° for $f_0$ ' + format(round(min_freq,2), '.2f') + 'Hz', zorder = 3)
    plt.scatter(np.deg2rad(max_Azi+180), np.log(max_freq), c='red', edgecolor='black', zorder = 3)
    plt.scatter(np.deg2rad(min_Azi+180), np.log(min_freq),c='white', edgecolor='black', zorder = 3)

    ### modify the rotational options
    ax.set_theta_direction('clockwise')
    ax.set_theta_zero_location('N')
    ax.set_rlabel_position(0)
    ax.text(np.radians(180),np.log(ax.get_rmax()/3.5),'Frequency',fontsize=8,
            rotation=90,ha='left',va='center', color= 'white')

    #limits of the frequency and modify the ticks of the frequency
    if auto_freq:
        limfreq_min = round(max_freq,1) - 0.4
        limfreq_max = round(max_freq,1) + 0.4

    ax.set_rlim(np.log(limfreq_min),np.log(limfreq_max))
    pos_list = np.log(np.arange(limfreq_min+0.1,limfreq_max,steps/2))
    freq_list = np.round(np.arange(limfreq_min+0.1,limfreq_max,steps),3)
    freqs = []
    for i in freq_list:
        freqs.append(i)
        freqs.append('')

    ax.yaxis.set_major_locator(ticker.FixedLocator(pos_list))
    ax.yaxis.set_minor_locator(ticker.FixedLocator(pos_list+0.1))
    ax.yaxis.set_major_formatter(ticker.FixedFormatter((freqs)))

    rlabels = ax.get_ymajorticklabels()
    for label in rlabels:
        label.set_color('white')

    #specify the ticks of the azimuth
    ax.set_xticks(np.pi/180. * np.linspace(0,  360, 18, endpoint=False))
    ax.yaxis.set_tick_params(labelsize=9)

    plt.legend(loc='best', bbox_to_anchor=(-0.4, -0.35, 0.5, 0.5), frameon=False)
    plt.grid(linestyle='-.', linewidth=0.2, alpha = 1, zorder = 200, color = 'grey')

    plt.title("Resonance frequency polarisation of " + ID, y=1.08)
    plt.tight_layout()
    if save_fig:
        plt.savefig('%s'%ID + '_polarisation.png')

    #find the lon lat positions from the HVSR database file
    df_database = pd.read_csv(all_data, header=0)
    df_database.head()
    name = df_database['Name']
    easting = df_database['Easting'][(name == ID).values.argmax()]
    northing = df_database['Northing'][(name == ID).values.argmax()]

    rot_data.append([ID, A_max, max_freq, max_Azi,A_min, min_freq, min_Azi, easting, northing])

    print(ID, round(A_max,2), round(max_freq,2),round(max_Azi,2),round(A_min,2),
       round(min_freq,2), min_Azi, round(np.float(easting),0), round(np.float(northing),2))

##### plot all rotational data & apply the definition
print('ID', 'A_max', 'max_freq', 'max_Azi','A_min', 'min_freq', 'min_Azi', 'easting', 'northing')

if plot_all:
    df2 = pd.read_csv(all_data, delimiter=',', skiprows=0, engine = 'python')
    IDs = df2["Name"]
    A0s = df2["A0"]
    for i in IDs:
        if manual:
            A0_max = A_manual
        else:
            # set maximum amplitude from A0 provided in the database list
            A0_max = round(A0s[(IDs == i).argmax()] + 1, 0)
        try:
            plot_rotationaldata('%s' % i, i, limfreq_min, limfreq_max)
        except:
            pass

    # save data to csv
    names = ["ID", "A_max", "max_freq", "max_Azi", "A_min", "min_freq", "min_Azi", "Easting", "Northing"]
    with open("HVSR rotation.csv", 'w', newline='') as results:
        wr = csv.writer(results)
        wr.writerow(names)
        for i in rot_data:
            wr.writerow(i)
else:
    IDs = IDs
    df2 = pd.read_csv(all_data, delimiter=',', skiprows=0, engine='python', index_col = "Name")
    A0s = df2["A0"]
    for i in IDs:
        if manual:
            A0_max = A_manual
        else:
            # set maximum amplitude from A0 provided in the database list and add 4
            A0_max = np.array(round(A0s[(i)],0)+1)
        plot_rotationaldata('%s' % i, i, limfreq_min, limfreq_max)
        plt.show()