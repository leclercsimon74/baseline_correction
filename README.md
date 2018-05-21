# baseline_correction
Baseline correction for spectra-like data

This code present example of use for a simple baseline correction.
It is more adapated for data with a large number of points (over 500) and presenting peak.

This code is for python 2.7, and require numpy, skimage, scipy as well as matplotlib library to work.
Is present the baseline correction function, a display function and spectrum data.

The baseline function is very simple, and perform a moving average that exclude 'signal', a level correction and finish with a smoothing.
To exlude signal, a Otsu threshold is applied (http://scikit-image.org/docs/dev/api/skimage.filters.html#skimage.filters.threshold_otsu) on the data for the moving average, excluding the values identify as positive. This permits to obtain a spectrum without the 'signal', that is adjusted to have the minmum of the baseline equal to 0. The baseline is further smooth by a savgol-golay filter to remove any spikes (https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.signal.savgol_filter.html). Finally, the data are substracted with the baseline.

Parameters of the function is the data (1d array), block_size (optionnal, at 101), the polyorder (optionnal, at 3) and the show_graph (optionnal, True). The block size permits to control the window used for the moving average and the smoothing. I advise to use a block size superior to the size of the 'signal' peak, and inferior to the baseline variations. The polyorder affect the smoothing power, with a low poly resulting in a vey blocky smooth. Finally, the show_graph permit to display the raw data, raw and smooth baseline as well as the corrected data on the same graph.
The function returns only the corrected data, same lenght as the input data.

More information on https://leclercsimon74.wixsite.com/mysite
