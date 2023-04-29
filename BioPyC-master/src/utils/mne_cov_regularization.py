# -*- coding: utf-8 -*-

"""
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License


import numpy as np

def _regularized_covariance(data, reg=None):
    """Compute a regularized covariance from data using sklearn.

    Parameters
    ----------
    data : ndarray, shape (n_channels, n_times)
        Data for covariance estimation.
    reg : float | str | None (default None)
        If not None, allow regularization for covariance estimation
        if float, shrinkage covariance is used (0 <= shrinkage <= 1).
        if str, optimal shrinkage using Ledoit-Wolf Shrinkage ('ledoit_wolf')
        or Oracle Approximating Shrinkage ('oas').

    Returns
    -------
    cov : ndarray, shape (n_channels, n_channels)
        The covariance matrix.
    """
    # compute regularized covariance using sklearn
    if reg == 'ledoit_wolf':
        from sklearn.covariance import LedoitWolf
        skl_cov = LedoitWolf(store_precision=False, assume_centered=True)
    elif reg == 'oas':
        from sklearn.covariance import OAS
        skl_cov = OAS(store_precision=False,
                              assume_centered=True)
    
    cov = skl_cov.fit(data.T).covariance_

    return cov





