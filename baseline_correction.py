# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:22:20 2018

@author: Simon
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"

def Beautiful_Axis(plt, thickness, fontsize, nbins=5):
    ax = plt.gca()
    ax.tick_params(direction='out', width=thickness)
    plt.setp(ax.spines.values(), linewidth=thickness)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.locator_params(nbins=nbins, axis='x')
    plt.locator_params(nbins=nbins, axis='y')
    plt.yticks(fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.tight_layout()

def baseline_correction(data, block_size=101, polyorder=3, show_graph=True):
    """
    Permit to remove the baseline from data.
    It first realized an Otsu filtering on the data on the block_size,
    then realize the mean of the selected point. The minimum of this baseline
    is then substract to avoid negative value.
    Finally, the data is smooth using a savgol filter of block_size and 
    polyorder parameters. \n
    Require skimage.filters and scipy.signal.\n
    Parameters
    ----------
    data : array like, 1d
        data where the correction is apported
    block_size : int, odd number
        block size for the scanning, need to be an odd number (not internally check).
        Default value is 101
    polyorder : int
        value for the smoothin using the savgol_filter, Default is 3
    show_graph : bool
        permit to display the different step of smoothing and final result in a matplotlib plot.
        Default is True
    Return
    --------
    corrected_data : 1D array
        data with the baseline substracted 

    """
    import skimage.filters
    import scipy.signal
    baseline = np.zeros((len(data)))
    for x in range(int(len(data))):
        min_half = int(block_size/2)
        max_half = int(block_size/2)
        if x-min_half < 0:
            min_half = 0
        if x+max_half > len(data):
            max_half = len(data)
        selected_data = data[x-min_half:x+max_half]
        thre = skimage.filters.threshold_otsu(np.asarray((selected_data))) #detect peak in the block
        test = selected_data[selected_data<thre] #remove the peak value
        baseline[x] = np.mean(test)
        
    baseline = baseline - np.min(baseline)
    smooth_baseline = scipy.signal.savgol_filter(baseline, block_size, polyorder) #smooth the result
    corrected_data = data - smooth_baseline
    
    if show_graph:
        plt.plot(np.arange(len(data)), data, 'b', label='raw data')
        plt.plot(np.arange(len(data)), baseline, 'c', label='baseline1')
        plt.plot(np.arange(len(data)), smooth_baseline, 'g', label='baseline2')
        plt.plot(np.arange(len(data)), corrected_data, 'r', label='corrected')
        plt.legend()
        plt.show()
    
    return corrected_data

#data loading
cell_sp = np.loadtxt('cell_spectrum.csv')
bkgd_sp = np.loadtxt('background_spectrum.csv')
x_axis =  np.loadtxt('x_axis.csv')

#raw plot
plt.plot(x_axis, cell_sp, label='cell spectrum')
plt.plot(x_axis, bkgd_sp, label='background spectrum')
plt.title('raw data')
Beautiful_Axis(plt, 1, 7)
plt.legend(frameon=False)
plt.show()

#baseline processing
cell_sp_co = baseline_correction(cell_sp, block_size=25)
bkgd_sp_co = baseline_correction(bkgd_sp, block_size=25)

#corrected data plot
plt.plot(x_axis, cell_sp_co, label='cell spectrum')
plt.plot(x_axis, bkgd_sp_co, label='background spectrum')
plt.title('corrected data')
Beautiful_Axis(plt, 1, 7)
plt.legend(frameon=False)
plt.show()

#final result
plt.plot(x_axis, cell_sp_co-bkgd_sp_co)
plt.title('substracted cell data')
Beautiful_Axis(plt, 1, 7)
plt.show()
