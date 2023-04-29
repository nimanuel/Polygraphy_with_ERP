# -*- coding: utf-8 -*-

"""
The class split_signals splits the signals into train and test data sets
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License

from src.utils import eeg_signals_constructor
from collections import OrderedDict
import numpy as np
from sklearn.model_selection import train_test_split

class split_signals(object):

    def __init__(self):

        self.repository_split_signals = OrderedDict() # Dictionary, always having 'training_set' as first key, testing_set as second key
    
    def split_signals_based_on_ratio(self, eeg_signals, ratio):
        """
        Split the signals into two data set : train and test
        :param eeg_signals: eeg signals structure, with attribute X [nb_samples, nb_channels, nb_trials] and y [nb_trials]
        :param ratio: ratio [float between 0 and 1] of trials to keep in the training set. The testing set size will automatically be equal to 1 minus this ratio
        :return: a sorted dictionary, having 'training_set' as first key, testing_set as second key
        """
        nb_trials = np.shape(eeg_signals.X)[2]

        # Create train and test sets
        train_set = eeg_signals_constructor.eeg_signals_constructor()
        test_set = eeg_signals_constructor.eeg_signals_constructor()
        
        index_train, index_test = train_test_split(np.arange(nb_trials),stratify=eeg_signals.y, test_size=1-ratio)
        # Update train_set
        train_set.X = eeg_signals.X[:, :, index_train]
        train_set.y = eeg_signals.y[index_train]

        # update test_Set
        test_set.X = eeg_signals.X[:, :, index_test]
        test_set.y = eeg_signals.y[index_test]

        if eeg_signals.sfreq:
            train_set.sfreq = eeg_signals.sfreq
            test_set.sfreq = eeg_signals.sfreq

        self.repository_split_signals['training_set'] = train_set
        self.repository_split_signals['testing_set'] = test_set

        return self.repository_split_signals
    
    def split_index_based_on_ratio(self, eeg_signals, ratio, type_):
        """
        Split the signals into two data set : train and test
        :param eeg_signals: eeg signals structure, with attribute X [nb_samples, nb_channels, nb_trials] and y [nb_trials]
        :param ratio: ratio [float between 0 and 1] of trials to keep in the training set. The testing set size will automatically be equal to 1 minus this ratio
        :return: a sorted dictionary, having 'training_set' as first key, testing_set as second key
        """
        nb_trials = np.shape(eeg_signals.X)[2]

        if type_ == 'shuffle':
            index_train, index_test = train_test_split(np.arange(nb_trials),
                                                   stratify=eeg_signals.y,
                                                   test_size=1-ratio)
        elif type_ == 'chronological':
            index_train, index_test = np.arange(nb_trials)[:int(nb_trials*ratio)], np.arange(nb_trials)[int(nb_trials*(1-ratio)):]

        return index_train, index_test
    
    def split_signals_based_on_index(self, eeg_signals, index_train, index_test):
        """
        Split the signals into two data set : train and test
        :param eeg_signals: eeg signals structure, with attribute X [nb_samples, nb_channels, nb_trials] and y [nb_trials]
        :param ratio: ratio [float between 0 and 1] of trials to keep in the training set. The testing set size will automatically be equal to 1 minus this ratio
        :return: a sorted dictionary, having 'training_set' as first key, testing_set as second key
        """
        nb_trials = np.shape(eeg_signals.X)[2]

        # Create train and test sets
        train_set = eeg_signals_constructor.eeg_signals_constructor()
        test_set = eeg_signals_constructor.eeg_signals_constructor()
        
        # Update train_set
        train_set.X = eeg_signals.X[:, :, index_train]
        train_set.y = eeg_signals.y[index_train]
        
        # update test_Set
        test_set.X = eeg_signals.X[:, :, index_test]
        test_set.y = eeg_signals.y[index_test]

        if eeg_signals.sfreq:
            train_set.sfreq = eeg_signals.sfreq
            test_set.sfreq = eeg_signals.sfreq

        self.repository_split_signals['training_set'] = train_set
        self.repository_split_signals['testing_set'] = test_set

        return self.repository_split_signals
    
    
    
    def split_signals_leave_one_out(self, eeg_signals, passband, kf):
        """
        Split the signals into two data set : train and test
        :param eeg_signals: eeg signals structure, with attribute X [nb_samples, nb_channels, nb_trials] and y [nb_trials]
        :param ratio: ratio [float between 0 and 1] of trials to keep in the training set. The testing set size will automatically be equal to 1 minus this ratio
        :return: a sorted dictionary, having 'training_set' as first key, testing_set as second key
        """
        nb_trials = np.shape(eeg_signals.X)[2]

        list_combinations_passband_train_test_split = [] # list of combinations of splitted signals, each of these leaving one trial as test set
        # We dont return a signal but a list of splited signals
        for train, test in kf.split(
                eeg_signals.X.T):  # we have to take the transpose since kf function works only on the first dimension

            ephemere_signals_train, ephemere_signals_test = eeg_signals_constructor.eeg_signals_constructor(), eeg_signals_constructor.eeg_signals_constructor()
            ephemere_signals_train.X, ephemere_signals_test.X = eeg_signals.X[:, :, train], eeg_signals.X[:, :, test]
            ephemere_signals_train.y, ephemere_signals_test.y = eeg_signals.y[train], eeg_signals.y[test]

            self.repository_split_signals = OrderedDict() # Dictionary, always having 'training_set' as first key, testing_set as second key
            self.repository_split_signals['training_set'], self.repository_split_signals[
                'testing_set'] = ephemere_signals_train, ephemere_signals_test

            ephemere_repository = OrderedDict()
            ephemere_repository[passband] = self.repository_split_signals

            list_combinations_passband_train_test_split.append(ephemere_repository)

        return list_combinations_passband_train_test_split

    def split_signals_index(self, eeg_signals, passband, train_index, test_index):
        """
        Split the signals into two data set : train and test
        :param eeg_signals: eeg signals structure, with attribute X [nb_samples, nb_channels, nb_trials] and y [nb_trials]
        :param ratio: ratio [float between 0 and 1] of trials to keep in the training set. The testing set size will automatically be equal to 1 minus this ratio
        :return: a sorted dictionary, having 'training_set' as first key, testing_set as second key
        """



        ephemere_signals_train, ephemere_signals_test = eeg_signals_constructor.eeg_signals_constructor(), eeg_signals_constructor.eeg_signals_constructor()

        ephemere_signals_train.X, ephemere_signals_test.X = eeg_signals.X[:, :, train_index], eeg_signals.X[:, :, test_index]
        ephemere_signals_train.y, ephemere_signals_test.y = eeg_signals.y[train_index], eeg_signals.y[test_index]

        self.repository_split_signals = OrderedDict() # Dictionary, always having 'training_set' as first key, testing_set as second key
        self.repository_split_signals['training_set'], self.repository_split_signals['testing_set'] = ephemere_signals_train, ephemere_signals_test

        if eeg_signals.sfreq:
            self.repository_split_signals['training_set'].sfreq = eeg_signals.sfreq
            self.repository_split_signals['testing_set'].sfreq = eeg_signals.sfreq

        ephemere_repository = OrderedDict()
        ephemere_repository[passband] = self.repository_split_signals


        return ephemere_repository




