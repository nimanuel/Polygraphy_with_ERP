# -*- coding: utf-8 -*-
"""
This module contains Tangent MDM with geodesic filtering from Riemannian Geometry
Allows to classify EEG signals into 2+ classes, based on Riemannian distances
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


import pyriemann.classification as riemann
from src.utils import covariance_matrix, normalize
import numpy as np
from sklearn.metrics import accuracy_score
from collections import OrderedDict
import pandas as pd
from skfeature.function.information_theoretical_based import MRMR

class riemann_fbfgmdm(object):

    def __init__(self):
        self.y_pred = None
        self.y_true = None
        self.model = None
        self.accuracy_score = None
        self.index_selected_features = None
        self.repository_passband_models = OrderedDict()
        self.selected_passbands = {}
        self.size_train = None
        self.size_test = None
        self.classifier_parameter = {}


    def fit(self, repository_passband_split_signals, set_=None, classifier_parameter=None):
        """
        Work with 2 classes only
        :param repository_passband_split_signals:
        :param set_:
        :return:
        """

        if 'nb_features_to_keep' in classifier_parameter.keys():
            nb_features = classifier_parameter['nb_features_to_keep']
        else:
            raise Exception('You do not have set the nb_features_to_keep parameter')

        if len(repository_passband_split_signals) != 1: # Should have more than one passband in this repository
            self.distances_centroid_1, self.distances_centroid_2 = None, None

            # For each passband, get distances to two classes
            for passband, eeg_signals in repository_passband_split_signals.items():
                X, y = eeg_signals[set_].X, eeg_signals[set_].y
                distances_centroid_1, distances_centroid_2, model = self.get_distances_to_both_centroids(X, y, None)
                self.repository_passband_models[passband] = model

            self.index_selected_features = self.index_features_to_keep(distances_centroid_1, distances_centroid_2, y, nb_features=nb_features)
            self.size_train = len(y)
            self.selected_passbands = np.floor(self.index_selected_features)
        else:
            raise Exception('Riemannian filter bank FgMDM can only be applied on multiple passbands, please enter multiple passbands')



    def predict(self, repository_passband_split_signals, set_=None):
        """
        Predict trials labels based on EEG signals
        :param X: EEG signals [nb_samples, nb_channels, nb_trials]
        :return: label vector [nb_trials]
        """
        if len(repository_passband_split_signals) != 1:  # Should have more tha one passband in this repository
            self.distances_centroid_1, self.distances_centroid_2 = None, None

            # For each passband, get distances to two classes
            for passband, eeg_signals in repository_passband_split_signals.items():
                X, y = eeg_signals[set_].X, eeg_signals[set_].y
                distances_centroid_1, distances_centroid_2, model = self.get_distances_to_both_centroids(X, y, passband=passband)

            self.y_pred = self.select_features_from_index(distances_centroid_1, distances_centroid_2)

            if len(np.unique(self.y_true)) != 2:
                print('we only deal with 2 classes !')
            else:
                sorted_list_labels = np.sort(np.unique(self.y_true))
            self.size_test = len(y)
            self.y_true = [0 if x == sorted_list_labels[0] else 1 for x in self.y_true]

    def score_accuracy(self):
        """
        Scores performances of the algorithms
        :return: a float number, corresponding to the classification accuracy score
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

    def get_distances_to_both_centroids(self, X, y, passband=None):

        # Get the covariance matrix from eeg signals from the training set
        covariance_matrix_ = covariance_matrix.get_covariance_matrix_from_eeg_signals(X)

        # sort both covariance matrices and labels by labels values
        covariance_matrix_ = covariance_matrix_[np.argsort(y),:,:]
        y = y[np.argsort(y)]

        if passband == None: # it means we are working on the training set
            # Create model
            model = riemann.FgMDM()
            model.fit(covariance_matrix_, y)
        else: # it means we are working on the testing set
            model = self.repository_passband_models[passband]
            self.y_true = y

        # Get the geodesic distances
        distances = model.transform(covariance_matrix_)  # obtained through pyriemann shape = [nb_trials, nb_class]

        # Get distances data from training set to each centroid
        self.distances_centroid_1 = np.array(
            [distances[:, 0]]).T if self.distances_centroid_1 is None else np.concatenate(
            (self.distances_centroid_1, np.array([distances[:, 0]]).T), axis=1)

        self.distances_centroid_2 = np.array(
            [distances[:, 1]]).T if self.distances_centroid_2 is None else np.concatenate(
            (self.distances_centroid_2, np.array([distances[:, 1]]).T), axis=1)

        return self.distances_centroid_1, self.distances_centroid_2, model



    def index_features_to_keep(self, distances_centroid_1, distances_centroid_2, y, nb_features=None):
        """
        Select features with maximum information concerning distances to centroids of classes
        :param distances_centroid_1:
        :param distances_centroid_2:
        :return:
        """
        squared_distances_centroid_1 = np.square(distances_centroid_1)
        squared_distances_centroid_2 = np.square(distances_centroid_2)

        # Calcul differences of distances to each centroid
        diff_dist_centroids = squared_distances_centroid_1 - squared_distances_centroid_2

        # Normalizing and discretizing data sets
        dist_train_first_centroid_to_norma, mean_features, std_features = normalize.normalize_data(
            diff_dist_centroids, y)

        # PYMRMR model
        '''
        columns_name = [str(i) for i in range(np.shape(squared_distances_centroid_1)[1] + 1)]

        frame_ = pd.DataFrame(
        np.concatenate((np.array([y]).T, dist_train_first_centroid_to_norma[:, :-1]), axis=1),
            columns=columns_name)

        index_ = pymrmr.mRMR(frame_, 'MID', nb_features)
        index = pd.Series(index_).astype(int) - 1
        '''

        # skfeature model
        index = MRMR.mrmr(dist_train_first_centroid_to_norma[:, :-1], np.array(y).T,
                                n_selected_features=nb_features)

        return index

    def select_features_from_index(self, distances_centroid_1, distances_centroid_2):
        """
        Select features with maximum information concerning distances to centroids of classes
        :param distances_centroid_1:
        :param distances_centroid_2:
        :return:
        """
        squared_distances_centroid_1 = np.square(distances_centroid_1)[:, self.index_selected_features]
        squared_distances_centroid_2 = np.square(distances_centroid_2)[:, self.index_selected_features]

        features = np.concatenate((np.array([np.sum(squared_distances_centroid_1, axis=1)]).T,
                                   np.array([np.sum(squared_distances_centroid_2, axis=1)]).T),
                                  axis=1)

        mask_min_test = np.argmin(features, axis=1)

        return mask_min_test

