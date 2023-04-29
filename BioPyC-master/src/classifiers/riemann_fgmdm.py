# -*- coding: utf-8 -*-
"""
This module contains Tangent MDM with geodesic filtering from Riemannian Geometry
Allows to classify EEG signals into 2+ classes, based on Riemannian distances
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


import pyriemann.classification as riemann
from src.utils import covariance_matrix
import numpy as np
from sklearn.metrics import accuracy_score

class riemann_fgmdm(object):

    def __init__(self):
        self.y_pred = None
        self.y_true = None
        self.model = None
        self.accuracy_score = None
        self.size_train = None
        self.size_test = None

        self.classifier_parameter = {}

    def fit(self, repository_passband_split_signals, set_=None, classifier_parameter=None):

        if len(repository_passband_split_signals) == 1: # Should have only one passband in this repository
            for eeg_signals in repository_passband_split_signals.values():
                X, y = eeg_signals[set_].X, eeg_signals[set_].y
                self.size_train =len(y)
        else:
            raise Exception('Riemannian FgMDM can only be applied on one passband, please enter a single passband')

        # Get the covariance matrix from eeg signals from the training set
        covariance_matrix_train = covariance_matrix.get_covariance_matrix_from_eeg_signals(X)

        # Get the transposed vector to match with Barachan riemannian algo
        labels = np.array(y).astype(int)

        self.model = riemann.FgMDM()
        self.model.fit(covariance_matrix_train, labels)

    def predict(self, repository_passband_split_signals, set_=None):
        """
        Predict trials labels based on EEG signals
        :param X: EEG signals [nb_samples, nb_channels, nb_trials]
        :return: label vector [nb_trials]
        """
        if len(repository_passband_split_signals) == 1: # Should have only one passband in this repository
            for eeg_signals in repository_passband_split_signals.values():
                X, y = eeg_signals[set_].X, eeg_signals[set_].y
        else:
            raise Exception('Riemannian FgMDM can only be applied on one passband, please enter a single passband')

        # Get the covariance matrix from eeg signals from the testing set
        covariance_matrix_test = covariance_matrix.get_covariance_matrix_from_eeg_signals(X)

        self.y_true = y
        self.size_test = len(y)
        self.y_pred = self.model.predict(covariance_matrix_test)

    def score_accuracy(self):
        """
        Scores performances of the algorithms
        :param y:
        :return:
        """
        self.accuracy_score = accuracy_score(self.y_true, self.y_pred, normalize=True)

    def score_fisher(self, y):
        """
        Scores performances of the algorithms
        :param y:
        :return:
        """
        self.y_true = y
        return self.y_true, self.y_pred



