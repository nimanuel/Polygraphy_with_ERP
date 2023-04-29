# -*- coding: utf-8 -*-

"""
The class eeg_signals_constructor builds a structure for the eeg signals. This structure is based on matlab structure
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License


class physio_signals_constructor(object):

    def __init__(self):

        self.X = None # Repository with keys ['EDA', 'heart_rate', 'breathing']
        self.y = None
        self.sfreq = None

    def build_signals(self, X, y, sfreq):
        self.X = X
        self.y = y
        self.sfreq = sfreq