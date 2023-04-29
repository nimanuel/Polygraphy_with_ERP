# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:08:54 2020

@author: David Trocellier - david.trocellier33@orange.fr
"""

import matplotlib.pyplot as plt
import numpy as np
import neurokit as nk
import biosppy
import pywt

from src.features_extraction.physio.general_biosignals import Biosignal

class heart_rate(Biosignal):
    """Class that preprocess and extract features for respiration data"""

    def preprocessing(self):
        """ Clean the data with a FIR and remove all frequencies above 40 Hz"""

        self.data, _, _ = biosppy.signals.tools.filter_signal(signal=self.data, ftype='FIR', band='lowpass',
                                                              order=int(0.3 * self.sfreq), frequency=[40],
                                                              sampling_rate=self.sfreq)

    def get_r_peaks(self, tolerance=0.05, do_plot=False):
        """ algoritms develloped by dan, identify the peaks"""

        sampling_rate = self.sfreq

        #Todo modify, signal must have pair index for pywt
        self.data = self.data[1:]
        # Wavelet de reference,ressemble onde qrs
        db1 = pywt.Wavelet('sym4')
        # Decomposition en ondelette

        coeffs = pywt.wavedec(self.data, db1, level=5)
        coeffs[0] = np.zeros(np.shape(coeffs[0]))
        coeffs[3] = np.zeros(np.shape(coeffs[3]))
        coeffs[4] = np.zeros(np.shape(coeffs[4]))
        coeffs[5] = np.zeros(np.shape(coeffs[5]))
        # Reconstruction
        reconstruction = pywt.waverec(coeffs, 'sym4')
        reconstruction = np.abs(reconstruction) * np.abs(reconstruction);

        # Recherche des points inflections
        aux = np.diff(np.sign(np.diff(reconstruction)))
        zeross = np.squeeze(np.argwhere(aux < 0))

        # Mask => On ne cherche que le max des ondes R (signal>0)
        mask = np.squeeze(self.data[zeross] > 0)
        zeross = zeross[mask]

        # On ne veut pas detecter d'autres "petites" ondes T ...
        mask = np.array((reconstruction[zeross] > (np.max(reconstruction) / 10)))
        zeross = zeross[mask]

        # On a besoin de récupérer avec précision le maximum,on
        # fait donc une recherche autour du point déterminé avec une tolérance
        tolerance = int(tolerance * sampling_rate)
        length = len(self.data)
        newR = []
        for r in zeross:
            a = r - tolerance
            if a < 0:
                continue
            b = r + tolerance
            if b > length:
                break
            newR.append(a + np.argmax(self.data[a:b]) + 1)
        if do_plot:
            plt.plot(self.data)
            plt.plot(newR, self.data[newR], 'or')
        # Renvoie les index
        # To do: renvoyer amplitudes aussi?
        newR = np.array(newR)
        newR = np.unique(newR)
        self.peak = newR
        return (newR)

    def hearth_rate_variability(self):

        try:
            self.peak
        except:
            self.get_r_peaks(tolerance=0.5, do_plot=False)



        self.features.update(nk.ecg_hrv(list(self.peak), sampling_rate=self.sfreq))

        # if you want the list and the explanation of nk.ecg_hrv dict try help()

        nn_interval = np.diff(self.peak) * (1/self.sfreq)

        # point carré geometrie

        pc_rr1 = abs(nn_interval[:-1] - nn_interval[1:])

        pc_rr2 = abs(-nn_interval[:-1] + 2 * pc_rr1.mean() - nn_interval[1:])
        # Je pense que cette formule est fausse

        self.features['sd_rr1'] = pc_rr1.std()
        self.features['sd_rr2'] = pc_rr2.std()
