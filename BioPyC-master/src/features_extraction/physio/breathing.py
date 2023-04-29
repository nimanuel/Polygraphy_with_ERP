# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:08:54 2020

@author: David Trocellier - david.trocellier33@orange.fr
"""


import matplotlib.pyplot as plt
import mne
import numpy as np
import neurokit as nk
import biosppy

from src.features_extraction.physio.general_biosignals import Biosignal



class breathing(Biosignal):
    """Class that preprocess and extract features for respiration data"""

    def preprocessing(self):
        """ Clean the data with biospy then collect all the features from biospy and neurokit"""
        self.data = biosppy.signals.tools.filter_signal(signal=self.data,
                                                        ftype='butter',
                                                        band='bandpass',
                                                        order=2,
                                                        frequency=[0.1, 0.5], sampling_rate=self.sfreq)['signal']

        self.nk = nk.rsp_process(self.data, sampling_rate=self.sfreq)
        self.biosppy = biosppy.signals.resp.resp(self.data, sampling_rate=self.sfreq, show=False)

    def breathing_rate_variability(self, bins):
        """ take in entry the bins and compute the BRV (breathing rate variability inspired by HRV)
        SD is Standar deviation, MSE is Multi Scale Entropy """

        #

        nn_interval = np.diff(bins[:, 3]) * (1/self.sfreq)
        first_diff = np.diff(nn_interval)

        self.features['nn_std'] = nn_interval.std()
        self.features['nn_first_diff_std'] = first_diff.std()
        self.features['nn_mean'] = nn_interval.mean()

        # point carré geometrie

        # plt.scatter( nn_interval[:-1], nn_interval[1:] ,alpha=0.3)

        pc_rr1 = abs(nn_interval[:-1] - nn_interval[1:])

        pc_rr2 = abs(-nn_interval[:-1] + 2 * pc_rr1.mean() - nn_interval[1:])
        # Je pense que cette formule est fausse

        self.features['sd_rr1'] = pc_rr1.std()
        self.features['sd_rr2'] = pc_rr2.std()

    def get_features(self):
        """ Extract all the features and save them into the corresponding attribute"""

        # Mesure each time the data cross the 0 Value
        crossing = self.crossing_detection(0)

        # Find the min and max between this to crossings
        min_bin = self.min_detection(crossing, 0)

        max_bin = self.max_detection(crossing, 0)

        # Update the dictionnary with the statistics
        self.features.update(self.descriptive_statistics('peak_length', array=max_bin[:, 1] - max_bin[:, 0]))
        self.features.update(self.descriptive_statistics('trough_length', min_bin[:, 1] - min_bin[:, 0]))

        self.features.update(self.descriptive_statistics('peak_amplidute', max_bin[:, 3]))
        self.features.update(self.descriptive_statistics('trough_amplitude', min_bin[:, 3]))

        self.features.update(self.descriptive_statistics('resp_rate', self.biosppy['resp_rate']))

        # power=biosppy.signals.tools.power_spectrum(self.data,1/self.dt)

        # Use multitaper to compute PSD
        # Quite long ( between 5 and 10 seconds) to reduce complexiti use bandwidth with a small value
        power, freq = mne.time_frequency.psd_array_multitaper(self.data, sfreq=self.sfreq, fmin=0.1, fmax=0.5,
                                                              adaptive=False, normalization='length')
        #plt.plot(freq, power)
        #plt.show()

        self.breathing_rate_variability(max_bin)
        self.freq_to_features(power, freq)

