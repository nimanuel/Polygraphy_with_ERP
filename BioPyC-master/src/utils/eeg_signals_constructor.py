# -*- coding: utf-8 -*-

"""
The class eeg_signals_constructor builds a structure for the eeg signals. This structure is based on matlab structure
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License


class eeg_signals_constructor(object):

    def __init__(self):

        self.X = None
        self.y = None
        self.sfreq = None

    def build_signals(self, X, y):
        self.X = X
        self.y = y