# -*- coding: utf-8 -*-
"""
This file contains the CSP class
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from mne.decoding import CSP
import numpy as np
from src.utils import mne_cov_regularization
import scipy.linalg as la
from collections import OrderedDict
import pandas as pd

class csp(object):

    def __init__(self):
        self.n_components = 6

        self.features_train = None
        self.features_test = None

        self.label_train = None
        self.label_test = None
        self.repository_passband_model = OrderedDict()



    def fit(self, repository_passband_split_signals={}, filter_parameter={}):
        """
        fit the data to create a model out of them : the data needs to be bandpassed into a unique frequency band
        Ex: [8,12] pour alpha
        :param repository_passband_split_signals: 1-key dictionary with passband as key, 2-keys dictionaries as values.
        Those 2 keys are 'training_set' and 'testing_set'
        :return: 1-key dictionary with passband as key, model as values.
        """
        self.n_components = filter_parameter['csp_lda_nb_filter_pairs']*2

        if len(repository_passband_split_signals) == 1:
            for key, eeg_signals in repository_passband_split_signals.items():

                # Using CSP method from MNE
                if len(np.unique(eeg_signals['training_set'].y)) == 2:
                    model = CSP(n_components=self.n_components, reg=0.16, norm_trace=True)
                    model.fit(eeg_signals['training_set'].X.T, eeg_signals['training_set'].y)
                else:
                    raise Exception('You can apply CSP only on 2 classes paradigms !   ' + str(len(np.unique(eeg_signals['training_set'].y))) + 'classes have been found')

                # Using homemade CSP - Lotte's version
                #self.learn(eeg_signals['training_set'])
                #self.filter_train = self.extract_features(eeg_signals['training_set'])[:, :-1]
                #self.filter_test = self.extract_features(eeg_signals['testing_set'])[:, :-1]

                self.label_train = eeg_signals['training_set'].y
                self.label_test = eeg_signals['testing_set'].y

                self.repository_passband_model[key] = model

        else:
            raise Exception(' This is a matter of passband, we only want signals from one band pass for the CSP ! ')

    def transform(self, repository_passband_split_signals):

        if len(repository_passband_split_signals) == 1:
            for key, model in self.repository_passband_model.items():
                # using sci kit
                self.features_train = model.transform(repository_passband_split_signals[key]['training_set'].X.T)
                self.features_test = model.transform(repository_passband_split_signals[key]['testing_set'].X.T)

        print('')
        print('feature train inside')
        print(np.shape(self.features_train))
        print('')
        self.features_train = pd.DataFrame(self.features_train)
        self.features_test = pd.DataFrame(self.features_test)
        self.selected_passbands = [0]
        print(self.features_train)
        print(np.shape(self.features_train))
        print('')

    '''
    def learn(self, EEG_signals):
        nb_channels = np.shape(EEG_signals.X)[1]
        nb_trials = np.shape(EEG_signals.X)[2]
        class_labels = np.unique(EEG_signals.y)
        nb_classes = np.shape(class_labels)[0]

        if nb_classes != 2:
            print('ERROR! CSP can only be used for two classes ')
            return

        cov_matrices = []

        # computing the normalized covariance matrices for each trial
        trial_cov = np.zeros(nb_channels * nb_channels * nb_trials).reshape(nb_channels, nb_channels, nb_trials)
        for t in range(nb_trials):
            E = EEG_signals.X[:, :, t].T
            EE = np.dot(E, E.T)
            trial_cov[:, :, t] = EE / EE.trace(offset=0)

        # computing the covariance matrix for each class
        for c in range(nb_classes):
            cov_matrices.append(np.mean(trial_cov[:, :, EEG_signals.y == class_labels[c]], axis=2))

        # regularize the matrices to avoid negative values from miscalculus

        cov_matrices[0] = mne_cov_regularization._regularized_covariance(cov_matrices[0], reg='ledoit_wolf')
        cov_matrices[1] = mne_cov_regularization._regularized_covariance(cov_matrices[1], reg='ledoit_wolf')

        D, V = la.eigh(cov_matrices[0], cov_matrices[1])

        # sorting eigen values and get the index
        index_sorted_eigv = np.argsort(D)[::-1]
        V = V[:, index_sorted_eigv]

        self.CSP_matrix = V.T

    def extract_features(self, EEG_signals):

        nb_trials = np.shape(EEG_signals.X)[2]
        features = np.zeros((nb_trials, 2 * self.n_components + 1))

        filter_ = np.concatenate((self.CSP_matrix[:self.n_components], self.CSP_matrix[-self.n_components:]), axis=0)

        # Extracting the CSP features from each trial
        for t in range(nb_trials):
            # Projecting the data onto the CSP filters
            projected_trials = np.dot(filter_, EEG_signals.X[:, :, t].T)

            # Generating the features as the log variance of the projected signals
            variances = np.var(projected_trials, axis=1)  # var dim [44 * 1]

            for f in range(len(variances)):
                features[t, f] = np.log(variances[f])
            features[t, -1] = EEG_signals.y[t]
        return features
    '''

        