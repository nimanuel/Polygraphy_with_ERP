# -*- coding: utf-8 -*-

"""
The class mat is made for reading .mat files, containing eeg signals
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from scipy.io import loadmat
import numpy as np
from src.utils import eeg_signals_constructor

class preprocessed_mat(object):

    def __init__(self, matlab_header=''):
        self.eeg_signals = None # X 3D matrix of shape [nb_samples, nb_channels, nb_trials], y vector of shape [1, nb_trials]
        self.matlab_header = matlab_header # you can either specifcy your matlab header of the structure, either seek for it

    def load_data(self, path_to_file):
        """
        Using scipy.io to read the matlab structure contained in files, then convert this matlab structure to a python object defining the eeg_signals
        :return: Nothing
        """
        data = loadmat(path_to_file) # we got here a dictionary with 5 classes, including "Header" and "EEGsignals"

        # you can either specifcy your matlab header of the structure (above), either seek for it
        if self.matlab_header == '':
            for name, dict_ in data.items():
                if(name[0:3]=='EEG'):
                    self.matlab_header = name
        matlab_structure = data[self.matlab_header]  # we are only interested by EEGsignals in this matlab matrix

        # Convert matlab structure matrices into numpy arrays data/labels
        X, y = self.convert_matrix(matlab_structure)

        # Build a signals structure based on data arrays
        self.eeg_signals = eeg_signals_constructor.eeg_signals_constructor()
        self.eeg_signals.build_signals(X, y)

        return self.eeg_signals


    def convert_matrix(self, matlab_structure):
        X = self.get_eeg_signals(matlab_structure[0][0])
        y = self.get_label(matlab_structure[0][0])
        return X, y


    def get_eeg_signals(self, matrix):
        """
        Extract the 3D matrix of the eeg signals : X
        :param matrix:
        :return: 3D matrix of eeg signals : shape [nb_samples, nb_channels, nb_trials]
        """
        sub_x = matrix[0]
        return sub_x

    def get_label(self, matrix):
        """
        Extract the vector of labels from the matrix : y
        :param matrix: matrix of shape [nb_samples, nb_channels, nb_trials]
        :return: vector of shape : [1,nb_trials]
        """
        sub_y = matrix[1]
        for y in range(np.shape(sub_y)[0]):
            y_vect = sub_y[y]
        return y_vect

