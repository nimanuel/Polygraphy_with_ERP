# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:08:54 2020

@author: David Trocellier - david.trocellier33@orange.fr
"""


import matplotlib.pyplot as plt
import mne

import numpy as np
import neurokit as nk
import math

from src.features_extraction.physio.general_biosignals import Biosignal

class eda(Biosignal):

    def preprocessing(self):
        self.neuro = nk.eda_process(self.data, self.sfreq)

    def process(self):
        """ get all features and save them in the corresponding attributs"""

        self.features.update(self.descriptive_statistics("signal_tonic", self.neuro['df']['EDA_Tonic'], True))
        self.features.update(
            self.descriptive_statistics("signal_EDA", self.neuro['df']['EDA_Filtered'], stat_etendu=True))
        self.features.update(
            self.descriptive_statistics("phasic_peak_amplitude", self.neuro['EDA']['SCR_Peaks_Amplitudes'],
                                        stat_etendu=False))

        self.features["nb_peak_per_min"] = len(self.neuro['EDA']['SCR_Peaks_Indexes']) * 60 / (len(self.data) *(1/self.sfreq))

        # Compute the peak longitude

        phasic_peak_longitude = self.neuro['EDA']['SCR_Recovery_Indexes'] - self.neuro['EDA']['SCR_Onsets']
        indices = np.argwhere(np.isnan(
            phasic_peak_longitude))  # Some peaks dont recover before the next peak in this case longitude is equal to onset_on_this_peak - onset_of_the_next_peak

        try:
            phasic_peak_longitude[indices] = self.neuro['EDA']['SCR_Onsets'][indices + 1] - self.neuro['EDA']['SCR_Onsets'][
                indices]
        except:

            if math.isnan(phasic_peak_longitude[-1]):
                phasic_peak_longitude = phasic_peak_longitude[:-1]

                '''
                if phasic_peak_longitude[0]!=np.nan:
                    phasic_peak_longitude = phasic_peak_longitude[:-1]
                    print('new phasic peak : ', phasic_peak_longitude)
                else:
                    phasic_peak_longitude = phasic_peak_longitude[1:-1]
                    print('new phasic peak : ', phasic_peak_longitude)
                '''
            else:
                raise Exception('There is not phasic peaks in your data ! ')



        self.features.update(self.descriptive_statistics("phasic_peak_longitude", phasic_peak_longitude))

        self.features["not_recovery"] = len(indices)

        self.features.update(self.descriptive_statistics("ordone_pente", self.neuro['df']['EDA_Phasic'][
            self.neuro['EDA']['SCR_Onsets']]))
        self.features.update(self.descriptive_statistics("pic_pic_interval", np.diff(self.neuro['EDA']['SCR_Onsets'])))

        # Frequencies Domain

        power, freq = mne.time_frequency.psd_array_multitaper(self.neuro['df']['EDA_Filtered'], sfreq=512, fmin=0.045,
                                                              fmax=0.25, adaptive=False, normalization='length')
        #plt.plot(freq, power)
        #plt.show()

        self.freq_to_features(power, freq)
