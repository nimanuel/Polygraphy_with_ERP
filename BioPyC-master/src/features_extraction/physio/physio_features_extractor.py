# -*- coding: utf-8 -*-
"""
This file contains the physio_features_extractor class
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/09/2020
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from src.features_extraction.physio import breathing, heart_rate, eda, general_biosignals
from src.utils import normalize
from skfeature.function.information_theoretical_based import MRMR
import numpy as np
import pandas as pd
import math

class physio_features_extractor(object):

    def __init__(self):

        self.nb_features = None
        self.repository_features = {}

        self.features_train = None
        self.features_test = None

        self.label_train = None
        self.label_test = None
        self.trials_train_mask = [] # not all trials are kept for physiological analysis
        self.trials_test_mask = [] # not all trials are kept for physiological analysis

        self.repository_features_per_signals_type = {}
        self.signals_type = []


    def fit(self, repository_physiological_split_signals, signals_type):

        self.signals_type = signals_type
        print('')
        print('')

        # we only deal with physiological signals in this script
        if 'EEG' in signals_type:

            # Removing 'EEG' from the list
            signals_type = [elmt for elmt in signals_type if elmt != 'EEG']


        for split_set in ['training_set', 'testing_set']:


            repository_features_set = None

            # List of removed trials, mainly because the signals are too short
            list_removed_trials = []
            list_repo_per_sensor = []

            for sensor_type in signals_type:


                repository_features_set = None

                if (sensor_type == 'heart_rate') or (sensor_type == 'breathing') or (sensor_type == 'eda'):

                    # Import the adequate reader, for gdf or mat format
                    char_import = 'from src.features_extraction.physio import ' + sensor_type
                    exec (char_import)

                    matrix_signals = repository_physiological_split_signals[sensor_type][
                        split_set].X  # [nb_samples * nb_ch * nb_trials]


                    for trial_id in range(np.shape(matrix_signals)[2]):

                        try:

                            if sensor_type == 'heart_rate':  # Max number of features = 42 - 40 with 10sec 10 with 4 sec
                                data = matrix_signals[:, :, trial_id].T[
                                    0]  # 0 since we want to get rid of the channel dimension

                                # Create the sensor object
                                char = sensor_type + '.' + sensor_type + '()'
                                hr_raw = heart_rate.heart_rate(data, int(
                                    repository_physiological_split_signals[sensor_type][split_set].sfreq))

                                # hr_raw = heart_rate()
                                hr_raw.preprocessing()
                                hr_raw.hearth_rate_variability()

                                repository_features_set = self.mergeFrame(repository_features_set, hr_raw.features)


                            if sensor_type == 'breathing':  # Max number of features ? 51 with 14 sec 49 with 10
                                data = matrix_signals[:, :, trial_id].T[
                                    0]  # 0 since we want to get rid of the channel dimension

                                # Create the sensor object
                                char = sensor_type + '.' + sensor_type + '()'
                                breathing_raw = breathing.breathing(data, int(
                                    repository_physiological_split_signals[sensor_type][split_set].sfreq))

                                # hr_raw = heart_rate()
                                breathing_raw.preprocessing()
                                breathing_raw.get_features()
                                repository_features_set = self.mergeFrame(repository_features_set, breathing_raw.features)

                            if sensor_type == 'eda':

                                data = matrix_signals[:, :, trial_id].T[
                                    0]  # 0 since we want to get rid of the channel dimension

                                # Create the sensor object
                                char = sensor_type + '.' + sensor_type + '()'
                                eda_raw = eda.eda(data,
                                                  int(repository_physiological_split_signals[sensor_type][split_set].sfreq))

                                # hr_raw = heart_rate()
                                eda_raw.preprocessing()
                                eda_raw.process()

                                #repository_features_set = self.mergeDict(repository_features_set, eda_raw.features)
                                repository_features_set = self.mergeFrame(repository_features_set, eda_raw.features)

                        except:
                            # Remove trials
                            if repository_features_set is not None:
                                frame_new_empty_raw = pd.DataFrame({})
                                for feature in repository_features_set.columns.values:
                                    frame_new_empty_raw[feature] = pd.Series([np.nan])
                                repository_features_set = repository_features_set.append(frame_new_empty_raw).reset_index(drop=True)

                            else:
                                repository_features_set = pd.DataFrame({})
                                repository_features_set['no_feature'] = [np.nan]


                            #if type(list(repository_features_set.values())[0]) == list:
                            #    print('incremental size :', np.shape(pd.DataFrame(repository_features_set)))
                            list_removed_trials.append(trial_id)

                    list_repo_per_sensor.append(repository_features_set)

                    if sensor_type == 'heart_rate':
                        # add features that have been calculated for heart rate
                        self.repository_features_per_signals_type['heart_rate'] = repository_features_set.columns.values
                    elif sensor_type == 'eda':
                        # add features that have been calculated for EDA
                        self.repository_features_per_signals_type['eda'] = repository_features_set.columns.values
                    elif sensor_type == 'breathing':
                        # add features that have been calculated for breathing
                        self.repository_features_per_signals_type['breathing'] = repository_features_set.columns.values

            # Merge repo from each sensor :
            if len(list_repo_per_sensor) > 1:
                if len(list_repo_per_sensor) == 2 :
                    repository_features_set = pd.concat([list_repo_per_sensor[0], list_repo_per_sensor[1]], axis=1)
                elif len(list_repo_per_sensor) == 3 :
                    repository_features_set = pd.concat([list_repo_per_sensor[0], list_repo_per_sensor[1], list_repo_per_sensor[2]], axis=1)


            self.repository_features[split_set] = repository_features_set

            if 'no_feature' in self.repository_features[split_set].columns.values:
                self.repository_features[split_set].drop(labels=['no_feature'], axis=1)

            # Remove trials that have been unsuccessful during train or test
            if split_set == 'training_set' :
                mask_trials_to_keep_train = [trial not in list_removed_trials for trial in list(range(0, len(self.repository_features[split_set])))]

                self.repository_features[split_set] = self.repository_features[split_set].iloc[mask_trials_to_keep_train,:]
                # Update label train and label test
                self.label_train = repository_physiological_split_signals[sensor_type]['training_set'].y[
                    mask_trials_to_keep_train]

                self.trials_train_mask = mask_trials_to_keep_train
            else:
                mask_trials_to_keep_test = [trial not in list_removed_trials for trial in
                                             list(range(0, len(self.repository_features[split_set])))]
                self.repository_features[split_set] = self.repository_features[split_set].iloc[
                                                      mask_trials_to_keep_test, :]
                self.label_test = repository_physiological_split_signals[sensor_type]['testing_set'].y[
                    mask_trials_to_keep_test]
                self.trials_test_mask = mask_trials_to_keep_test



    def transform(self):

        self.nb_features = 10

        self.features_train = self.repository_features['training_set']
        self.features_test = self.repository_features['testing_set']

        ##############################################################################
        # Cleaning
        ##############################################################################

        # Delete the entire feature if more than 20% nans in the column
        threshold_nb_nan = int(0.02 * len(self.features_train))
        features_to_drop = []
        for elmt in self.features_train.columns.values:

            f = [math.isnan(l) for l in list(self.features_train[[elmt]].values.T[0])]
            if f.count(True) > threshold_nb_nan:
                features_to_drop.append(elmt)

        self.features_train = self.features_train.drop(labels = features_to_drop, axis=1)

        # Delete the entire feature if more than 20% nans in the column
        threshold_nb_nan = int(0.02 * len(self.features_test))
        features_to_drop = []
        for elmt in self.features_test.columns.values:

            f = [math.isnan(l) for l in list(self.features_test[[elmt]].values.T[0])]
            if f.count(True) > threshold_nb_nan:
                features_to_drop.append(elmt)
        self.features_test = self.features_test.dropna(axis=1, thresh=threshold_nb_nan)

        features_to_keep = [feature for feature in self.features_train.columns.values if
                            feature in self.features_test.columns.values]


        self.features_train_all_sensors = self.features_train.loc[:, features_to_keep]
        self.features_test_all_sensors = self.features_test.loc[:, features_to_keep]

        # Dealing with labels
        self.features_train['labels'] = pd.Series(self.label_train)
        self.features_train = self.features_train.dropna(axis=0, how = 'any')

        self.label_train = list(self.features_train['labels'])
        self.features_train = self.features_train.drop(labels = ['labels'], axis =1)

        # Get rid of inf values
        #mask_features_to_keep = [x is np.dtype('int64') or x is np.dtype('float64') for x in list(self.features_train.dtypes)]
        #self.features_train = self.features_train.loc[:, mask_features_to_keep]
        self.features_train = self.features_train.replace([np.inf, -np.inf], np.nan)
        self.features_train = self.features_train.dropna(axis=1, how='any')

        self.features_test['labels'] = pd.Series(self.label_test)
        self.features_test = self.features_test.dropna(axis=0, how='any')
        self.label_test = list(self.features_test['labels'])

        self.features_test= self.features_test.drop(labels=['labels'], axis=1)

        # Get rid of inf values
        #mask_features_to_keep = [x is np.dtype('int64') or x is np.dtype('float64') for x in list(self.features_test.dtypes)]
        #self.features_test = self.features_test.loc[:, mask_features_to_keep]
        self.features_test = self.features_test.replace([np.inf, -np.inf], np.nan)
        self.features_test = self.features_test.dropna(axis=1, how='any')

        print('index TRAIN', len(list(self.features_train.index)), list(self.features_train.index))
        print('index TEST', len(list(self.features_test.index)), list(self.features_test.index))

        self.trials_train_mask = list(self.features_train.index)
        self.trials_test_mask = list(self.features_test.index)

        ##############################################################################
        # Features selection per type of signals
        ##############################################################################

        new_frame_all_sensors_train = pd.DataFrame({})
        new_frame_all_sensors_test = pd.DataFrame({})

        save_frame_all_features_train = self.features_train
        save_frame_all_features_test = self.features_test

        self.selected_features = []
        for sensor_type in self.signals_type:

            if (sensor_type == 'heart_rate') or (sensor_type == 'breathing') or (sensor_type == 'eda'):
                list_features_specific_sensor_to_keep = []

                for feature in save_frame_all_features_train.columns.values:

                    if feature in self.repository_features_per_signals_type[sensor_type]:
                        list_features_specific_sensor_to_keep.append(feature)

                self.features_train = save_frame_all_features_train.loc[:, list_features_specific_sensor_to_keep]
                self.features_test= save_frame_all_features_test.loc[:, list_features_specific_sensor_to_keep]

                normalized_filters_train, mean_filters, std_filters = normalize.normalize_data(
                    self.features_train.to_numpy(),
                    self.label_train)

                # skfeature model
                index = MRMR.mrmr(X=normalized_filters_train[:, :-1],
                                  y=normalized_filters_train[:, -1],
                                  n_selected_features=self.nb_features)

                self.features_train = pd.DataFrame(self.features_train).iloc[:, index[0:self.nb_features]]
                self.features_test = pd.DataFrame(self.features_test).iloc[:, index[0:self.nb_features]]

                self.selected_features = self.selected_features + list(self.repository_features['training_set'].columns.values[index[0:self.nb_features]])
                print('')
                print('selected features: ')
                print(self.selected_features)
                print(np.shape(self.selected_features))
                print('')
                new_frame_all_sensors_train = pd.concat([new_frame_all_sensors_train, self.features_train], axis=1)
                new_frame_all_sensors_test = pd.concat([new_frame_all_sensors_test, self.features_test], axis=1)

        # back to normal
        self.features_train = new_frame_all_sensors_train
        self.features_test = new_frame_all_sensors_test

        print('')
        print('for all sensors here is the shape train:  ', np.shape(self.features_train))
        print('for all sensors here is the shape test:  ', np.shape(self.features_test))
        print('here is teh number of features at the end , normaly 10 time the number of sensro : ', len(self.selected_features))
        print('')









    def mergeFrame(self, frame1, frame2):



        if type(frame2) == dict:
            if 'df' in list(frame2.keys()):
                frame2.pop('df')
            if 'RR_Intervals' in list(frame2.keys()):
                frame2.pop('RR_Intervals')



        if frame1 is None:

            new_pd_frame = pd.DataFrame({})
            if frame2 != {}:

                for feature, value in frame2.items():
                    new_pd_frame[feature] = [value]
            final_frame = new_pd_frame
        else:

            frame_ = pd.DataFrame({})
            new_column_repo = {}
            for elmt in frame1.columns.values:
                frame_[elmt] = pd.Series([np.nan])

            for key, value in frame2.items():
                if key in frame_.columns.values:
                    frame_[key][0] = value

                # Create a new column
                else:
                    new_column_repo[key] = value

            final_frame = frame1.append(frame_).reset_index(drop=True)
            # Adding new columns
            for key, value in new_column_repo.items():
                list_value = [np.nan for i in range(len(frame1))]
                list_value.append(value)

                final_frame[key] = pd.Series(list_value)
        return final_frame


