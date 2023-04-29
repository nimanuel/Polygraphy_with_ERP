# -*- coding: utf-8 -*-
"""
This module contains a function to get covariance matrices from eeg signals
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 17/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from sklearn.covariance import LedoitWolf
import numpy as np

def get_covariance_matrix_from_eeg_signals(X):
    """
    Cpmpute the covarainces matrices from eeg signals
    :param eeg_signals: signals structure, can be signals from either train or test set
    :return:
    """
    nb_channels = np.shape(X)[1]
    nb_trials = np.shape(X)[2]

    # computing the normalized covariance matrices for each trial
    trial_cov = np.zeros(nb_channels * nb_channels * nb_trials).reshape(nb_channels, nb_channels, nb_trials)

    for t in range(nb_trials):
        # regularization of cov matrices
        skl_cov = LedoitWolf(store_precision=False, assume_centered=True)
        trial_cov[:, :, t] = skl_cov.fit(X[:, :, t]).covariance_

    return trial_cov.T