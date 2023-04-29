# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:08:54 2020

@author: David Trocellier - david.trocellier33@orange.fr
"""


import mne
import numpy as np
import scipy.stats as stats

class Biosignal:

    def __init__(self, data, sfreq):
        """ Put in memory the biosignal data and call the corresponding preprocessing function"""
        self.data = np.array(data)
        #self.time = np.array(time)
        self.sfreq = sfreq
        self.features = {}
        #self.preprocessing()

    def crossing_detection(self, value):
        """ take a signal and a value return each time the signal cross the value """
        bool_pic = np.where(self.data >= value, True, False)

        crossings = np.where(np.diff(bool_pic))[0]

        return (crossings)

    def max_detection(self, crossings, value=0):
        """ Take the index where the raw cross a value and return the max between the two crossings """

        # fait qu'il y ai le bon nombre de pics.
        if self.data[0] > value:
            if self.data[1] < self.data[0]:  # si c'est décroissant
                crossings = crossings[1:]
            else:  # si croisant
                crossings = np.insert(crossings, 0, 0)

        if self.data[-1] > value:
            if self.data[-2] < self.data[-1]:  # si croissant
                crossings = crossings[:-1]
            else:  # si décroissant
                crossings = np.append(crossings, len(self.data))

        assert (len(crossings) % 2 == 0)

        bins = np.zeros((len(crossings) // 2, 4))
        for i in range(len(crossings) // 2):
            begin = crossings[i * 2]
            end = crossings[(i * 2) + 1]

            val_max = np.max(self.data[begin:end])
            arg_max = np.argmax(self.data[begin:end]) + begin

            bins[i] = [begin, end, val_max, arg_max]

        return bins

    def min_detection(self, crossings=None, value=0):
        """ Take the index where the raw cross a value and return the min between the two crossings """

        # fait qu'il y ai le bon nombre de pics.
        if self.data[0] < value:
            if self.data[1] < self.data[0]:  # si c'est décroissant
                crossings = np.insert(crossings, 0, 0)
            else:  # si croisant
                crossings = crossings[1:]

        if self.data[-1] < value:
            if self.data[-2] < self.data[-1]:  # si croissant
                crossings = np.append(crossings, len(self.data))
            else:  # si décroissant
                crossings = crossings[:-1]

        assert (len(crossings) % 2 == 0)

        bins = np.zeros((len(crossings) // 2, 4))
        for i in range(len(crossings) // 2):
            begin = crossings[i * 2]
            end = crossings[(i * 2) + 1]

            val_min = np.min(self.data[begin:end])
            arg_min = np.argmin(self.data[begin:end]) + begin

            bins[i] = [begin, end, val_min, arg_min]

        return bins

    def freq_to_features(self, power, freq):
        """Take the power spectral density and the corresponding frequencies and save them into the features dictionnary """

        for i in range(len(freq)):
            self.features["psd_" + str(freq[i])[:6]] = power[i]

    def bandpassfilter(self, lowpass=None, highpass=None):
        """ Use mne fonction to bandpass the data"""

        return (mne.filter.filter_data(self.data, self.sfreq, lowpass, highpass))

    def descriptive_statistics(self, name, array=None, stat_etendu=False):
        """ import a 1D numpy array and save the descriptive statistics (median ,
        standar deciation , count , minimim, maximum, 1st and 3rd quartile) in the features dictionnari """

        if type(array) == type(None):
            array = self.data

        stat = {}

        stat[name + "_std"] = array.std()
        stat[name + "_count"] = len(array)
        stat[name + "_min"] = array.min()
        stat[name + "_max"] = array.max()
        stat[name + "_1quartile"], stat[name + "_median"], stat[name + "_3quartile"] = np.percentile(array,
                                                                                                     [0.25, 0.5, 0.75])
        stat[name + "_mean"] = array.mean()
        if stat_etendu:
            stat[name + "_skewness"] = stats.skew(array, axis=None, bias=True, nan_policy='raise')
            stat[name + "_kurtosis"] = stats.kurtosis(array, axis=None, fisher=True, bias=True, nan_policy='raise')
        return stat
