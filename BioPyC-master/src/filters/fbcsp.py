# -*- coding: utf-8 -*-
"""
This file contains the FBCSP class
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from collections import OrderedDict
from mne.decoding import CSP
import numpy as np
import pandas as pd
from src.utils import normalize
from skfeature.function.information_theoretical_based import MRMR



class fbcsp(object):

    def __init__(self):
        self.n_components = 4 # Number of pairs kept for the CSP
        self.nb_features = 4 # number of kept features

        self.filter_train = None
        self.filter_test = None
        self.features_train = None
        self.features_test = None

        self.label_train = None
        self.label_test = None
        self.selected_passbands=None
        self.repository_passband_model = OrderedDict()



    def fit(self, repository_passband_split_signals={}, filter_parameter={}):
        """
        fit the data to create a model out of them : the data needs to be bandpassed into multiple frequency band
        Ex: [[4,8],[8,12]...[36,40]]
        :param repository_passband_split_signals: n-key dictionary with passbands as keys, 2-keys dictionaries as values.
        Those 2 keys are 'training_set' and 'testing_set'
        :return: n-key dictionary with passbands as keys, models as values.
        """
        if 'fbcsp_lda_nb_filter_pairs' in filter_parameter.keys() and 'nb_features_to_keep' in filter_parameter.keys():
            self.components = filter_parameter['fbcsp_lda_nb_filter_pairs']*2
            self.nb_features = filter_parameter['nb_features_to_keep']
        else:
            raise Exception('You do not have set the fbcsp_lda_nb_filter_pairs and nb_features_to_keep parameters')

        if len(repository_passband_split_signals) != 1:
            for key, eeg_signals in repository_passband_split_signals.items():

                # Using CSP method from MNE
                model = CSP(n_components=self.n_components, reg=0.16, norm_trace=True)
                model.fit(eeg_signals['training_set'].X.T, eeg_signals['training_set'].y)

                self.repository_passband_model[key] = model

            self.label_train = eeg_signals['training_set'].y
            self.label_test = eeg_signals['testing_set'].y

        else:
            raise Exception(' This is a matter of shape, we only want signals from one band pass for the CSP ! ')

    def transform(self, repository_passband_split_signals):

        if len(repository_passband_split_signals) != 1:
            for key, model in self.repository_passband_model.items():

                self.filter_train = model.transform(repository_passband_split_signals[key]['training_set'].X.T) \
                    if self.filter_train is None \
                    else np.concatenate((self.filter_train, model.transform(repository_passband_split_signals[key]['training_set'].X.T)), axis=1)

                self.filter_test = model.transform(repository_passband_split_signals[key]['testing_set'].X.T) \
                    if self.filter_test is None \
                    else np.concatenate((self.filter_test, model.transform(repository_passband_split_signals[key]['testing_set'].X.T)), axis=1)

            normalized_filters_train, mean_filters, std_filters = normalize.normalize_data(self.filter_train, self.label_train)
            #normalized_filters_test = normalize.normalize_data(self.filter_test, self.label_test, mean_features=mean_filters, std_features=std_filters)

            # PYMRMR model
            #columns_name = [str(i) for i in range(np.shape(normalized_filters_train)[1])]
            #frame_ = pd.DataFrame(
            #    np.concatenate((np.array([normalized_filters_train[:, -1]]).T, normalized_filters_train[:, :-1]),
            #                   axis=1), columns=columns_name)

            #index_ = pymrmr.mRMR(frame_, 'MID', self.nb_features)
            #index = pd.Series(index_).astype(int) - 1

            # skfeature model
            index = MRMR.mrmr(X=normalized_filters_train[:, :-1],
                                    y=normalized_filters_train[:, -1],
                                    n_selected_features=self.nb_features)

            self.features_train = pd.DataFrame(self.filter_train).iloc[:, index[0:self.nb_features]]
            self.features_test = pd.DataFrame(self.filter_test).iloc[:, index[0:self.nb_features]]
            self.selected_passbands=np.floor(index/self.n_components)





