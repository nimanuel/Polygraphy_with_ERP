# -*- coding: utf-8 -*-

"""
The class bci_competition_4_dataset_2a is made for specifying labels of the different classes for the bci_competition_4_dataset_2a dataset
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 28/03/2020
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import pandas as pd
import numpy as np

class bci_competition_4_dataset_2a(object):

    def __init__(self):
        pass

    def specify_labeling(self, list_label_files=[],
                         index=0,
                         events_=None):

        for file in list_label_files:

            # Check if run 1, corresponding to training, meaning idx 0 and 'T' in filename
            if index == 0 and 'T' in file:
                frame_labels = pd.read_csv(file)
            elif index == 1 and 'E' in file:
                frame_labels = pd.read_csv(file)

        list_labels = list(frame_labels['y'])
        mask = np.in1d(events_[2], 768)

        events_3_col = np.concatenate((np.array([events_[1]]).T,
                                          np.array([events_[3]]).T,
                                          np.array([events_[2]]).T),
                                         axis=1)  # probem with mne

        events_cross = events_3_col[mask, :]

        events_cross[:, 2] = list_labels
        mask = np.in1d(events_cross[:, 2], [1, 2])

        event_specific = events_cross[mask, :]

        event_id = {"right": 2, "left": 1}

        return event_specific, event_id