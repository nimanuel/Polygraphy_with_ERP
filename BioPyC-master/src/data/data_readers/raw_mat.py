# -*- coding: utf-8 -*-

"""
The class mat is made for reading .gdf files, containing eeg signals
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from scipy.io import loadmat
from mne import create_info
from mne.io import RawArray
from mne.channels import read_montage
import mne
import numpy as np
from src.utils import eeg_signals_constructor
from src.utils import functionalities_curiosity_project
from collections import OrderedDict

''' ######### OPTIONAL : STOP BOTH MNE PRINTING AND PYTHON WARNINGS ############ '''
import warnings
warnings.filterwarnings("ignore")

import sys, os
from contextlib import contextmanager


# To get rid of MNE printings, see method load_data_dev
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


class raw_mat(object):

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
                      tmin=0.0,
                      tmax=0.0,
                      list_all_channels=[],
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
        :return:
        '''

        list_raw_files = []

        #with suppress_stdout():  # Get rid of MNE printings

        list_files_to_load = self.define_files_to_load(list_files=list_files,
                                  list_runs=list_runs,
                                  list_sessions=list_sessions)


        # Load the data with mne, and add them to a list of raw object, where raw objects are mne structures (1 object for each dataset)
        for filename in list_files_to_load:
            data = loadmat(filename, struct_as_record=False, squeeze_me=True)
            run_array = data['data']
            for run in run_array:

                ch_names = [
                    'Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2',
                    'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz',
                    'EOG1', 'EOG2', 'EOG3'
                ]
                ch_types = ['eeg'] * 22 + ['eog'] * 3

                evd = {}
                n_chan = run.X.shape[1]
                montage = read_montage('standard_1005')
                eeg_data = 1e-6 * run.X
                sfreq = run.fs

                if not ch_names:
                    ch_names = ['EEG%d' % ch for ch in range(1, n_chan + 1)]
                    montage = None  # no montage

                if not ch_types:
                    ch_types = ['eeg'] * n_chan

                trigger = np.zeros((len(eeg_data), 1))
                # some runs does not contains trials i.e baseline runs
                if len(run.trial) > 0:
                    trigger[run.trial - 1, 0] = run.y

                eeg_data = np.c_[eeg_data, trigger]
                ch_names = ch_names + ['stim']
                ch_types = ch_types + ['stim']
                evd = {ev: (ii + 1) for ii, ev in enumerate(run.classes)}
                info = create_info(ch_names=ch_names, ch_types=ch_types, sfreq=sfreq, montage=montage)
                rawi = RawArray(data=eeg_data.T, info=info, verbose=False)

                runs.append(rawi)
                event_id.update(evd)

            raw = mne.concatenate_raws(runs)
            print('Look at raw_mat.py')
            breakpoint()
            print('lalalalallallaal')



            '''
            # Reading files, labeling "kind" of EOG electrodes as 202 ("kind" of EEG electrods = 2, "kind" of STIM = 3)
            raw = mne.io.read_raw_edf(input_fname=file, eog=list_eog, preload=True)
            list_raw_files.append(raw)
            '''

        print('list channels to drop')
        print(list_channels_to_drop)
        # Preprocess the data with MNE, and obtain a repository of passband signals
        repository_passband_signals = self.preprocess_data_dev(list_raw_files=list_raw_files,
                                                               dataset=dataset,
                                                               specify_labeling=specify_labeling,
                                                               passband=passband,
                                                               dictionary_stimulations=dictionary_stimulations,
                                                               tmin=tmin,
                                                               tmax=tmax,
                                                               list_channels=list_all_channels,
                                                               list_channels_to_drop=list_channels_to_drop)



        return repository_passband_signals


    def define_files_to_load(self,
                             list_files=None,
                             list_runs=[],
                             list_sessions=[]):
        '''
        Each subjets' folder will have 1 or more files in it. Ususally, those files correspond to distinct runs & sessions.
        To make things easier, the user will have to previously name his files with pattern easily recognitiable (ex: 'R1'for run 1, 'S3' for session 3, etc)
        :param path_to_subject_folder: path to the folder of a single subject
        :return:
        '''

        # Create a new list of files that answer to conditions
        list_files_to_keep = []

        # check if nb_run and nb_sessions make sense in each subject's folder
        list_runs_str = ['R' + str(elmt) for elmt in list_runs]
        list_sessions_str = ['S' + str(elmt) for elmt in list_sessions]

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
        '''
        for f in list_files:

            # Define the run based on filename ('Rx')
            if f.find('R') > 0:
                run = 'R' + f[f.find('R') + 1]
            else:
                raise Exception(
                    'You need to explecitely indicate the run in the filename by inputing the "R" letter in front of the number ! Ex: subject1_S1_R1.gdf')

            # Define the session based on filename ('Sx')
            if f.find('S') > 0:
                session = 'S' + f[f.find('S') + 1]
            else:
                raise Exception(
                    'You need to explecitely indicate the session in the filename by inputing the "S" letter in front of the number ! Ex: subject1_S1_R1.gdf')

            # Check if the file correspond to a file of the wanted Run of the wanted session
            if run in list_runs_str and session in list_sessions_str:
                print('run n:')
                print(run)
                print(session)
                list_files_to_keep.append(f)
        '''

        if len(list_files_to_keep) == len(list_runs) * len(list_sessions):
            print('There is the good number of files, check ')
        else:
            print('the number of files should be equal to the number of run multiplied by the number of sessions [nb_run*nb_sessions]')

        return list_files_to_keep

    def preprocess_data_dev(self,
                            list_raw_files=[],
                            dataset=None,
                            specify_labeling=False,
                            passband=[],
                            dictionary_stimulations={},
                            tmin=0.0,
                            tmax=0.0,
                            list_channels=[],
                            list_channels_to_drop=[]):
        '''
        Perform EEG epoching, filter the data per passband
        :return: dict per passband of object signals, signals[passband].x -> data, signals[passband].y -> labels
        '''
        repository_passband_signals = OrderedDict()
        idx_pb = []
        epochs = []

        for (idx, raw) in enumerate(list_raw_files):

            if list_channels != []: # to modify channels names or positions, for example references
                raw.info['ch_names'] = list_channels

            # Rename all channels in [chs -> ch_name] following changes that have been made in ch_names
            for i in range(len(raw.info['ch_names'])):
                raw.info['chs'][i]['ch_name'] = raw.info['ch_names'][i]

            # Get rid of some channels, if specified
            if list_channels_to_drop!=[]:
                raw.drop_channels(list_channels_to_drop)

            # Band pass the signals
            for (idx_passband, passband_) in enumerate(passband):
                # pass band filer the data in the desired bandpass
                raw_pb = raw.copy().filter(passband_[0], passband_[1])
                # Epoching the data -> Particular for curiosity project
                picked_channels = mne.pick_types(raw_pb.info, meg=False, eeg=True, eog=False, exclude='bads')
                events_ = mne.io.find_edf_events(raw_pb)
                print(raw.info)
                print('')
                print('')
                print('')
                print('')
                print(events_)
                print('')
                print('')
                print('')
                print('')
                print('')
                print('')
                print('')
                print('')

                print(dataset)
                print(specify_labeling)

                specify_labeling = False
                if specify_labeling == True:
                    # Import the labeling tool specific to the dataset
                    char_import = 'from src.utils.specific_studies_labeling import ' + dataset
                    exec(char_import)

                    events_specific, event_id = functionalities_curiosity_project.deal_with_event_stimulation(events_)
                else:
                    events_specific = np.concatenate((np.array([events_[1]]).T,
                                                      np.array([events_[3]]).T,
                                                      np.array([events_[2]]).T),
                                                     axis=1)  # probem with mne
                    event_id = dictionary_stimulations


                #events_curious, event_id = functionalities_curiosity_project.deal_with_event_stimulation(events_)

                # Working with find_edf_events
                rune = mne.Epochs(raw=raw_pb,
                                  events=events_specific,
                                  event_id=event_id,
                                  tmin=tmin,
                                  tmax=tmax,
                                  baseline=None,
                                  picks=mne.pick_types(raw.info, eeg=True, stim=False))

                print(rune.events[:, -1])

                epochs.append(rune)
                idx_pb.append(idx_passband)

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

            print('shape of X: ', np.shape(eeg_signals_pb.X))
            print('shape of y: ', np.shape(eeg_signals_pb.y))
            repository_passband_signals[str(passband_)] = eeg_signals_pb

        return repository_passband_signals

    '''
    def preprocess_data(self):

        for raw in self.raw_files:

            # Change ref position, from Fp1 to Cz
            raw.info['ch_names'] = self.list_channels
            # Rename all channels in [chs -> ch_name] following changes that have been made in ch_names
            for i in range(len(raw.info['ch_names'])):
                raw.info['chs'][i]['ch_name'] = raw.info['ch_names'][i]

            # Get rid of physio and stim channels
            raw.drop_channels(self.list_channels_to_drop)

            # pass band filer the data in the desired bandpass
            raw.filter(self.passband[0], self.passband[1])

            # Epoching the data -> Particular for curiosity project
            picked_channels = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, exclude='bads')
            events_ = mne.io.find_edf_events(raw)
            events_curious, event_id = functionalities_curiosity_project.deal_with_event_stimulation(events_)

            # Working with find_edf_events
            rune = mne.Epochs(raw=raw,
                             events=events_curious,
                             event_id=event_id,
                             tmin=self.tmin,
                             tmax=self.tmax,
                             picks=picked_channels)
            self.epochs.append(rune)

        concat_epochs = mne.concatenate_epochs(self.epochs)

        X = concat_epochs.get_data().T

        y = concat_epochs.events[:, -1]

        # Build a signals structure based on data arrays
        self.eeg_signals = eeg_signals_constructor.eeg_signals_constructor()
        self.eeg_signals.build_signals(X, y)

        print('shape of X: ', np.shape(self.eeg_signals.X))
        print('shape of y: ', np.shape(self.eeg_signals.y))
    '''



