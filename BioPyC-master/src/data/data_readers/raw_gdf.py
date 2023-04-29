# -*- coding: utf-8 -*-

"""
The class mat is made for reading .gdf files, containing eeg signals
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import mne
import numpy as np
from src.utils import eeg_signals_constructor, physio_signals_constructor
from src.utils import functionalities_curiosity_project
from collections import OrderedDict

''' ######### OPTIONAL : STOP BOTH MNE PRINTING AND PYTHON WARNINGS ############ '''
import warnings
warnings.filterwarnings("ignore")
mne.set_log_level("CRITICAL")

class raw_gdf(object):

    def __init__(self):
        self.eeg_signals = None # X 3D matrix of shape [nb_samples, nb_channels, nb_trials], y vector of shape [1, nb_trials]

    def load_data_dev(self,
                      dataset=None,
                      list_files=None,
                      specify_labeling=None,
                      list_runs=[],
                      list_sessions=[],
                      passband=[],
                      dictionary_stimulations={},
                      tmin={},
                      tmax={},
                      list_all_channels=[],
                      list_channels_EEG=[],
                      channel_eda='',
                      channel_breathing='',
                      channel_heart_rate='',
                      list_eog=[],
                      list_channels_to_drop=[]):
        '''
        Method that allows to load the data from gdf files.
        First calls the method define_files_to_load to obtain the list of files to load.
        Second upload the data into MNE raw objects.
        Finally calls the method preprocess_data to preprocess the raw objects using MNE
        :param list_files:
        :param list_runs:
        :param list_sessions:
        :param passband:
        :param tmin:
        :param tmax:
        :param list_all_channels:
        :param list_eog:
        :param list_channels_to_drop:
        :return: repository_passband_signals
        '''

        list_raw_files = []

        list_files_to_load = self.define_files_to_load(list_files=list_files,
                                  list_runs=list_runs,
                                  list_sessions=list_sessions)

        # Check if files specifying the labels :
        list_label_files = []
        for file in list_files:
            if file not in list_files_to_load and 'labels' in file:
                list_label_files.append(file)

        # Load the data with mne, and add them to a list of raw object, where raw objects are mne structures (1 object for each dataset)
        for file in list_files_to_load:
            # Reading files, labeling "kind" of EOG electrodes as 202 ("kind" of EEG electrods = 2, "kind" of STIM = 3)
            raw = mne.io.read_raw_edf(input_fname=file, eog=list_eog, preload=True)
            list_raw_files.append(raw)

        # Preprocess the data with MNE, and obtain a repository of passband signals
        repository_passband_signals_EEG, repository_physiological_signals = self.preprocess_data_dev(list_raw_files=list_raw_files,
                                                                                                     list_label_files=list_label_files,
                                                                                                     dataset=dataset,
                                                                                                     specify_labeling=specify_labeling,
                                                                                                     passband=passband,
                                                                                                     dictionary_stimulations=dictionary_stimulations,
                                                                                                     tmin=tmin,
                                                                                                     tmax=tmax,
                                                                                                     list_channels=list_all_channels,
                                                                                                     list_channels_EEG=list_channels_EEG,
                                                                                                     channel_eda=channel_eda,
                                                                                                     channel_breathing=channel_breathing,
                                                                                                     channel_heart_rate=channel_heart_rate,
                                                                                                     list_channels_to_drop=list_channels_to_drop)

        return repository_passband_signals_EEG, repository_physiological_signals


    def define_files_to_load(self,
                             list_files=None,
                             list_runs=[],
                             list_sessions=[]):
        '''
        Each subjets' folder will have 1 or more files in it. Ususally, those files correspond to distinct runs & sessions.
        To make things easier, the user will have to previously name his files with pattern easily recognitiable (ex: 'R1'for run 1, 'S3' for session 3, etc)
        :param path_to_subject_folder: path to the folder of a single subject
        :return: list_files_to_keep
        '''

        # Create a new list of files that answer to conditions
        list_files_to_keep = []

        for run_ in list_runs:
            run = 'R' + str(run_)
            for session_ in list_sessions:
                session = 'S' + str(session_)
                for f in list_files:
                    try:
                        # Check if existing R and S in the filename
                        if f.find('R') > 0 and int(f[f.find('R') + 1]) and f.find('S') > 0 and int(f[f.find('S') + 1]):

                            if run in f and session in f:
                                list_files_to_keep.append(f)
                    except:
                        raise Exception('You need to explecitely indicate the run and the session in the filename by inputing the "R" letter and the "S" letter in front numbers ! The filename should contain only 1 "R" and 1 "S". Ex: subject1_S1_R1.gdf')

        if len(list_files_to_keep) == len(list_runs) * len(list_sessions):
            print('All the files you chose to keep for the study have been found, i.e. session(s) {} & run(s) {}'.format(list_runs, list_sessions))
        else:
            print('the number of files should be equal to the number of run multiplied by the number of sessions [nb_run*nb_sessions]')

        return list_files_to_keep

    def preprocess_data_dev(self,
                            list_raw_files=[],
                            list_label_files=[],
                            dataset=None,
                            specify_labeling=False,
                            passband=[],
                            dictionary_stimulations={},
                            tmin={},
                            tmax={},
                            list_channels=[],
                            list_channels_EEG=[],
                            channel_eda='',
                            channel_breathing='',
                            channel_heart_rate='',
                            list_channels_to_drop=[]):
        '''
        Perform EEG epoching, filter the data per passband
        :return: repository_passband_signals -> dict per passband of object signals, signals[passband].x -> data, signals[passband].y -> labels
        '''
        repository_passband_signals = OrderedDict()
        idx_pb = []
        epochs = []
        epochs_eda = []
        epochs_breathing = []
        epochs_heart_rate = []

        for (idx, raw) in enumerate(list_raw_files):
            nb_trials_physio=0

            if list_channels != []: # to modify channels names or positions, for example references
                raw.info['ch_names'] = list_channels

            # Rename all channels in [chs -> ch_name] following changes that have been made in ch_names
            for i in range(len(raw.info['ch_names'])):
                raw.info['chs'][i]['ch_name'] = raw.info['ch_names'][i]

            # Get rid of some channels, if specified
            if list_channels_to_drop!=[]:
                raw.drop_channels(list_channels_to_drop)

            # Get index EEG and physio channels
            if list_channels_EEG != []:
                index_np = np.argwhere([val in list_channels_EEG for val in raw.info['ch_names']])
                index_EEG = np.array([index_np[i][0] for i in range(len(index_np))])
            if channel_eda != '':
                index_eda = np.array([raw.info['ch_names'].index(channel_eda)])
            if channel_breathing != '':
                index_breathing = np.array([raw.info['ch_names'].index(channel_breathing)])
            if channel_heart_rate != '':
                index_heart_rate = np.array([raw.info['ch_names'].index(channel_heart_rate)])

            # Epoching the data
            # picked_channels = mne.pick_types(raw_pb.info, meg=False, eeg=True, eog=False, exclude='bads')
            events_ = mne.io.find_edf_events(raw)

            if specify_labeling == True:

                # Import the labeling tool specific to the dataset
                char_import = 'from src.utils.specific_studies_labeling import ' + dataset
                exec (char_import)

                char_call_object = dataset + '.' + dataset + '()'
                dataset_object = eval(char_call_object)

                if list_label_files != []:
                    events_specific, event_id = dataset_object.specify_labeling(list_label_files=list_label_files,
                                                                                index=idx,
                                                                                events_=events_)
                else:
                    events_specific, event_id = dataset_object.deal_with_event_stimulation(events_)
            else:
                events_specific = np.concatenate((np.array([events_[1]]).T,
                                                  np.array([events_[3]]).T,
                                                  np.array([events_[2]]).T),
                                                 axis=1)  # probem with mne
                event_id = dictionary_stimulations



            # Deal with EDA
            if channel_eda != '':

                # Working with find_edf_events
                rune_eda = mne.Epochs(raw=raw,
                                  events=events_specific,
                                  event_id=event_id,
                                  tmin=tmin['eda'],
                                  tmax=tmax['eda'],
                                  baseline=None,
                                  picks=index_eda)
                # picks=mne.pick_types(raw.info, eeg=True, stim=False))
                epochs_eda.append(rune_eda)
                nb_trials_physio = np.shape(rune_eda.get_data().T)[2]

            # Deal with breathing
            if channel_breathing != '':

                # Working with find_edf_events
                rune_breathing = mne.Epochs(raw=raw,
                                      events=events_specific,
                                      event_id=event_id,
                                      tmin=tmin['breathing'],
                                      tmax=tmax['breathing'],
                                      baseline=None,
                                      picks=index_breathing)
                # picks=mne.pick_types(raw.info, eeg=True, stim=False))
                epochs_breathing.append(rune_breathing)

                nb_trials_physio = np.shape(rune_breathing.get_data().T)[2]



            # Deal with heart rate
            if channel_heart_rate != '':
                # Working with find_edf_events
                rune_heart_rate = mne.Epochs(raw=raw,
                                            events=events_specific,
                                            event_id=event_id,
                                            tmin=tmin['heart_rate'],
                                            tmax=tmax['heart_rate'],
                                            baseline=None,
                                            picks=index_heart_rate)
                # picks=mne.pick_types(raw.info, eeg=True, stim=False))
                epochs_heart_rate.append(rune_heart_rate)

                nb_trials_physio = np.shape(rune_heart_rate.get_data().T)[2]



            # Deal with EEG signals
            if list_channels_EEG != []:

                # Band pass the EEG signals
                for (idx_passband, passband_) in enumerate(passband):
                    # pass band filer the data in the desired bandpass
                    raw_pb = raw.copy().filter(passband_[0], passband_[1])

                    # events_curious, event_id = functionalities_curiosity_project.deal_with_event_stimulation(events_)

                    # Working with find_edf_events
                    rune = mne.Epochs(raw=raw_pb,
                                      events=events_specific,
                                      event_id=event_id,
                                      tmin=tmin['EEG'],
                                      tmax=tmax['EEG'],
                                      baseline=None,
                                      picks=index_EEG)
                    # picks=mne.pick_types(raw.info, eeg=True, stim=False))



                    # the number of trials can be different, based on the tmin and tmax
                    if nb_trials_physio != 0:
                        if np.shape(rune.get_data().T)[2] > nb_trials_physio:
                            if np.shape(rune.get_data().T)[2] - nb_trials_physio == 1:
                                rune.drop([np.shape(rune.get_data().T)[2]-1])

                    epochs.append(rune)
                    idx_pb.append(idx_passband)

        # Concat all epochs for all raw files
        for (idx_passband, passband_) in enumerate(passband):
            epoch_passband = []
            for (id, epoch) in enumerate(epochs):
                if idx_pb[id] == idx_passband:
                    epoch_passband.append(epoch)

            concat_epochs = mne.concatenate_epochs(epoch_passband)

            X = concat_epochs.get_data().T
            y = concat_epochs.events[:, -1]

            # Build a signals structure based on data arrays
            eeg_signals_pb = eeg_signals_constructor.eeg_signals_constructor()
            eeg_signals_pb.build_signals(X, y)

            repository_passband_signals[str(passband_)] = eeg_signals_pb


        # Create a repository of physiological signals, even if no physio signals
        repository_physiological_signals = {}

        # Concat all epochs from all runs, and for all physiological signals
        if channel_eda != '':
            concat_epochs_eda = mne.concatenate_epochs(epochs_eda)
            X = concat_epochs_eda.get_data().T # nb_samples* channel(1!) * nb_trials
            y = concat_epochs_eda.events[:, -1]


            # Build a signals structure based on data arrays
            eda_signals = physio_signals_constructor.physio_signals_constructor()
            eda_signals.build_signals(X, y, raw.info['sfreq'])

            repository_physiological_signals['eda'] = eda_signals

        if channel_breathing != '':
            concat_epochs_breathing = mne.concatenate_epochs(epochs_breathing)
            X = concat_epochs_breathing.get_data().T  # nb_samples* channel(1!) * nb_trials
            y = concat_epochs_breathing.events[:, -1]

            # Build a signals structure based on data arrays
            breathing_signals = physio_signals_constructor.physio_signals_constructor()
            breathing_signals.build_signals(X, y, raw.info['sfreq'])

            repository_physiological_signals['breathing'] = breathing_signals

        if channel_heart_rate != '':
            concat_epochs_heart_rate = mne.concatenate_epochs(epochs_heart_rate)
            X = concat_epochs_heart_rate.get_data().T  # nb_samples* channel(1!) * nb_trials
            y = concat_epochs_heart_rate.events[:, -1]

            # Build a signals structure based on data arrays
            heart_rate_signals = physio_signals_constructor.physio_signals_constructor()
            heart_rate_signals.build_signals(X, y, raw.info['sfreq'])

            repository_physiological_signals['heart_rate'] = heart_rate_signals


        return repository_passband_signals, repository_physiological_signals



