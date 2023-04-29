# -*- coding: utf-8 -*-
"""
This module contains the Linear Discriminant Analysis Algorithm, allowing to classify EEG signals after filtering
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,f1_score
import numpy as np

class svm(object):

    def __init__(self):
        self.y_pred = None
        self.y_true = None
        self.model = None
        self.accuracy_score = None
        self.size_train = None
        self.size_test = None
        self.classifier_parameter = {}

    def fit(self, X=None, y=None):
        """
        :param X: EEG signals [nb_samples, nb_channels, nb_trials]
        :param y: label vector [nb_trials]
        :return:
        """
        print('')
        print('##############################')
        print('Data in (train set) : ', np.shape(X))
        print('Label in (train set) : ', len(y))
        print('')
        self.model = SVC(gamma='auto', kernel='linear')
        self.model.fit(X, y)
        self.size_train = len(y)

    def predict(self, X=None, y=None):
        """
        Predict trials labels based on EEG signals
        :param X: EEG signals [nb_samples, nb_channels, nb_trials]
        :return: label vector [nb_trials]
        """
        print('Data in (test set) : ', np.shape(X))
        print('Label in (test set) : ', len(y))
        print('##############################')
        print('')
        self.y_true = y
        self.size_test = len(y)
        self.y_pred = self.model.predict(X)
