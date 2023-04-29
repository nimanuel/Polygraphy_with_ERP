# -*- coding: utf-8 -*-

"""
The class subject_specific runs the subject specific study
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License


from src.results import results_constructor
from src.utils import split_signals
from src.features_extraction.physio import physio_features_extractor

from collections import OrderedDict
from sklearn import model_selection

import pandas as pd
import numpy as np

class subject_specific(object):

    def __init__(self):

        # Calibration
        self.calibration_type = 'subject_specific'

        # Dataset
        # === all data types ===
        self.signals_type = []  # ['EEG', 'heart_rate', 'EDA', 'breathing']
        self.data_type = ''  # 'raw' or 'preprocessed'
        self.dataset = ''  # (Ex: 'bci_competition_4_dataset_2a')
        self.passband = []  # set of aassbands data should be filtered into
        self.training_split_ratio = 0.0  # split ratio for the training set (Ex: 0.8 for keeping 80% of the data for the training set)
        self.type_split = ''  # 'chronological' or 'shuffle'
        self.dataset_structure = None  # object
        # === preprocessed data === (no list of runs/session, should have been concatenated during the preprocessing)
        self.passband_delimiters = []  # string characters that delimit limit figures of the bandpass
        # === raw data === (meaning those are parameters for the preprocessing)
        self.specify_labeling = None # Meaning you have to implement a script to labelize your data
        self.list_subjects_to_keep = []  # list containing strings of the subjects (Ex: ['subject_1', 'subject_2'])
        self.list_sessions = []  # list containing integers of the sessions (Ex: [1,2])
        self.list_runs = []  # list containing integers of the runs (Ex: [1,2,3,4])
        self.dictionary_stimulations = {}  # (Ex: {'right':1, 'left':2})
        self.tmin = 0.0  # start time window signal, can before/after the stimulation (Ex: 2.5 for 2,5 sec after stimulation)
        self.tmax = 0.0  # stop time window signal, can before/after the stimulation (Ex: -1.0 for 1 sec before the stimulation)
        self.list_all_channels = []  # list of channels ['channel_1', 'channels_2', etc]
        self.list_channels_EEG = []  # List of channels ['FP1', AFz', etc]
        self.channel_breathing = ''  # name of the channel used for breathing, ex 'channel 65'
        self.channel_eda = ''  # name of the channel used for eda, ex 'channel 67'
        self.channel_heart_rate = ''  # name of the channel used for heart rate, ex 'channel 68'
        self.list_eog = []  # list EOGs ['eog_1', 'eog_2', etc]
        self.list_channels_to_drop = []  # list of channels ['unnamed_1', 'unnamed_2', etc]

        # Algorithm
        # ==== type ====
        self.filter = ''
        self.classifier = ''
        # ==== hyper-parameters ====
        self.filter_parameter = {}
        self.classifier_parameter = {}

        # Results
        # ==== Evaluation ====
        self.evaluation_type = ''  # 'classic' or 'cross_validation'
        self.cross_val_type = '' # can be "k-fold" or "leave-one-out" (if cross-validation evaluation type)
        self.kfold = 5 # must be an integer (if cross-validation evaluation type AND k-fold cross-validation type)
        self.type_split = ''  # 'chronological' or 'shuffle' (if classical evaluation type)

        # === build and store ===
        self.vector_score = []
        self.array_y_true = []
        self.array_y_pred = []
        self.vector_size_train = []
        self.vector_size_test = []
        # ==== Analysis to make ====
        self.score_type = ''
        self.list_statistical_tests = []
        self.list_plots = []
        # ==== Saving path for results dataframe ====
        self.results_filename = ''

        ############ Temporary, find a better solution ############
        self.subject = 0 # subject ID (integer)
        self.repository_features = {} # Repository of features that are used for the classification, per subject, per "fold" (dictionary with subject ID as key, a dictionary as value. This dictionary as fold as key))
        self.selected_features_final = {}
        # ##########################################################

    '''
    def run_study_classic_old(self):

        results = results_constructor.results_constructor()

        # First extract the signals from subjects' files
        for subject, files_list in self.dataset_structure.repository_subjects_files.items():


            if subject in self.dataset_structure.list_subjects_to_keep: # Check if the user has chosen to keep him

                # Read signals from subjects files
                paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]
                repository_EEG_passband_signals, repository_physiological_signals = self.extract_signals_from_path(paths_list) # Structure, signals.x -> signals, signals.y -> labels

                # Split signals of each passband into a train and a test set,
                repository_EEG_passband_split_signals = self.split_signals(repository_EEG_passband_signals)

                # Apply filter (if filter)
                if self.filter != '':
                    filters_ = self.apply_filter(repository_EEG_passband_split_signals)

                # Apply classifier
                if self.classifier != '':

                    # ==== With Filter ====
                    if self.filter != '':
                        classifier_ = self.apply_classifier_on_filters(filters_)

                    # ==== Without Filter ====
                    else:
                        classifier_ = self.apply_classifier_on_repository_passband_signals(repository_EEG_passband_split_signals)

                # Results
                # ==== Hold selected passbands subject ==== (if multiple passbands, i.e. if filter bank)
                if 'fb' in self.filter or 'fb' in self.classifier:
                    if 'fb' in self.filter:
                        results.hold_selected_passband_subject(selected_passbands=filters_.selected_passbands)
                    else:
                        results.hold_selected_passband_subject(selected_passbands=classifier_.selected_passbands)

                # ==== Hold classifiers predictions subject ====
                results.hold_classification_prediction_vector_subject(subject=subject,
                                                                      y_pred=classifier_.y_pred,
                                                                      y_true=classifier_.y_true,
                                                                      size_train=classifier_.size_train,
                                                                      size_test=classifier_.size_test)

        # ==== Build repository of selected passands, if multiple passbands ====
        if 'fb' in self.filter or 'fb' in self.classifier:
            results.generate_repository_selected_passbands(list_passbands=self.passband)

        # ==== Build table (pandas frame) of performances ====
        results.generate_performance_scores()
        results.build_frame_results(filter=self.filter, classifier=self.classifier, calibration_type=self.calibration_type)
        self.score_type = results.score_type

        # ==== Saving path for results dataframe ====
        if self.results_filename != '':
            results.store_results(results_path_folder_store=self.results_filename,
                                  calibration_type=self.calibration_type,
                                  filter=self.filter,
                                  classifier=self.classifier)
    '''




    def run_study_classic(self):

        results = results_constructor.results_constructor()

        # Initializing variables for the algorithm
        self.selected_features_final = {}

        # First extract the signals from subjects' files
        for subject, files_list in self.dataset_structure.repository_subjects_files.items():

            if subject in self.dataset_structure.list_subjects_to_keep: # Check if the user has chosen to keep him

                ############ Temporary, find a better solution ############
                self.subject = subject
                print('')
                print('subject : ', self.subject)
                print('')
                self.selected_features_final[self.subject] = []
                ###########################################################

                # Read signals from subjects files
                paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]
                repository_EEG_passband_signals, repository_physiological_signals = self.extract_signals_from_path(paths_list) # Structure, signals.x -> signals, signals.y -> labels

                '''
                # Split signals of each passband into a train and a test set,
                repository_EEG_passband_split_signals = self.split_signals(repository_EEG_passband_signals)

                # Apply filter (if filter)
                if self.filter != '':
                    filters_ = self.apply_filter(repository_EEG_passband_split_signals)
                '''

                # Get indexes of trials to keep as training set, and trials to keep as testing set (this indexes can be defined based either on EEG or on physilogical signals repositories)

                if 'EEG' in self.signals_type:
                    train_index, test_index = self.get_indexes_train_and_test_set(repository_signals=repository_EEG_passband_signals)
                elif repository_physiological_signals != {}:
                    train_index, test_index = self.get_indexes_train_and_test_set(
                        repository_signals=repository_physiological_signals)
                else:
                    raise Exception(
                        'Something went wrong: it is impossible to define indexes if there is no trials (either EEG or physiological) signals-based trials')

                # Apply classifier
                if self.classifier != '':

                    '''
                    # ==== With Filter ====
                    if self.filter != '':
                        classifier_ = self.apply_classifier_on_filters(filters_)

                    # ==== Without Filter ====
                    else:
                        classifier_ = self.apply_classifier_on_repository_passband_signals(repository_EEG_passband_split_signals)
                    '''

                    # ==== With features extraction ====
                    if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                            'eda' in self.signals_type) or self.filter != '':
                        extracted_features, selected_passbands, repository_selected_features_per_signals_type = self.extract_features_from_signals(
                            train_index=train_index,
                            test_index=test_index,
                            repository_physiological_signals=repository_physiological_signals,
                            repository_EEG_passband_signals=repository_EEG_passband_signals)

                        classifier_ = self.apply_classifier_on_features(extracted_features)

                    # ==== Without Feature extraction ====
                    else:
                        if 'EEG' in self.signals_type: # Work with EEG signals only
                            repository_EEG_passband_split_signals = self.split_signals(
                                repository_EEG_passband_signals,
                                train_index, test_index)
                            classifier_ = self.apply_classifier_on_repository_passband_signals(
                                repository_EEG_passband_split_signals)
                        else:
                            raise NameError(
                                'The direct classification without feature extraction works with EEG signals only')



                # Results
                # ==== Hold selected passbands subject ==== (if multiple passbands, i.e. if filter bank)
                if ('fb' in self.filter or 'fb' in self.classifier) and 'EEG' in self.signals_type:
                    if 'fb' in self.filter:
                        results.hold_selected_passband_subject(selected_passbands=selected_passbands)
                    else:
                        results.hold_selected_passband_subject(selected_passbands=classifier_.selected_passbands)

                # ==== Hold classifiers predictions subject ====
                results.hold_classification_prediction_vector_subject(subject=subject,
                                                                      y_pred=classifier_.y_pred,
                                                                      y_true=classifier_.y_true,
                                                                      size_train=classifier_.size_train,
                                                                      size_test=classifier_.size_test)

        # ==== Build repository of selected passbands, if multiple passbands ====
        if 'fb' in self.filter or 'fb' in self.classifier:
            results.generate_repository_selected_passbands(list_passbands=self.passband)

        # ==== Build table (pandas frame) of performances ====
        results.generate_performance_scores()
        results.build_frame_results(filter=self.filter, classifier=self.classifier, calibration_type=self.calibration_type, list_signal_types=self.signals_type)
        self.score_type = results.score_type

        # ==== Saving path for results dataframe ====
        if self.results_filename != '':
            results.store_results(results_path_folder_store=self.results_filename,
                                  calibration_type=self.calibration_type,
                                  filter=self.filter,
                                  signals_type=self.signals_type,
                                  classifier=self.classifier)

        ############ Temporary, find a better solution ############
        # Add this to the results constructor using the "generate_repository_selected_passbands" method 10 lines above
        if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                'eda' in self.signals_type) or self.filter != '':
            self.repository_features = pd.Series(repository_selected_features_per_signals_type)
            self.repository_features.T.to_csv(
                self.results_filename + 'subject_specific/selected_features/repository_features_per_signals.csv',
                index=False)

            print('')
            print('Finallly, the selected features (final !) : ')
            print(self.selected_features_final)
            self.selected_features_final = pd.DataFrame(self.selected_features_final)
            self.selected_features_final.to_csv(
                self.results_filename + 'subject_specific/selected_features/all_selected_features.csv', index=False)
        ################################################################################################


    def run_study_cross_validation(self, cross_val_type='leave_one_out'):

        #self.cross_val_type = 'k-fold'
        #self.kfold = 5


        self.kfold = int(self.kfold)

        results = results_constructor.results_constructor()

        # Initializing variables for the algorithm
        self.selected_features_final = {}

        # First extract the signals from subjects' files
        for subject, files_list in self.dataset_structure.repository_subjects_files.items():

            ############ Temporary, find a better solution ############
            self.subject = subject
            self.selected_features_final[self.subject] = []
            ############################################################

            # Check if subject in list subject to keep
            if subject in self.dataset_structure.list_subjects_to_keep:

                print('')
                print('subject : ', self.subject)
                print('')

                # Initialize subject holding parameters
                list_y_pred_cross_val = []
                list_y_true_cross_val = []
                vector_size_train = 0
                vector_size_test = 0

                # Read signals from subjects files
                paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]
                repository_EEG_passband_signals, repository_physiological_signals = self.extract_signals_from_path(paths_list) # Structure, signals.x -> signals, signals.y -> labels

                # Get indexes of trials to keep as train set test set, based on the cross validation type
                if self.cross_val_type == 'leave-one-out':
                    # Get the number of split
                    loo = model_selection.LeaveOneOut()
                    loo.get_n_splits(repository_EEG_passband_signals[str(self.passband[0])].y)
                    if 'EEG' in self.signals_type:
                        key = list(repository_EEG_passband_signals.keys())[0]
                        object_indexes_countainer = loo.split(repository_EEG_passband_signals[str(key)].X.T)
                    elif repository_physiological_signals != {}:
                        key = list(repository_physiological_signals.keys())[0]
                        object_indexes_countainer = loo.split(repository_physiological_signals[str(key)].X.T)
                    else:
                        raise Exception('Something went wrong: it is impossible to define indexes if there is no trials (either EEG or physiological) signals-based trials')

                elif self.cross_val_type == 'k-fold':
                    # Get the number of split
                    kf = model_selection.StratifiedShuffleSplit(n_splits=self.kfold, test_size=1.0/self.kfold, train_size=1-(1.0/self.kfold))
                    if 'EEG' in self.signals_type:
                        key = list(repository_EEG_passband_signals.keys())[0]
                        object_indexes_countainer = kf.split(repository_EEG_passband_signals[str(key)].X.T,
                                                             y=repository_EEG_passband_signals[str(key)].y)
                    elif repository_physiological_signals != {}:
                        key = list(repository_physiological_signals.keys())[0]
                        object_indexes_countainer = kf.split(repository_physiological_signals[str(key)].X.T,
                                                             y=repository_physiological_signals[str(key)].y)
                    else:
                        raise Exception('Something went wrong: it is impossible to define indexes if there is no trials (either EEG or physiological) signals-based trials')

                else:
                    raise Exception('You need to indicate which type of cross validation you want !')


                for train_index, test_index in object_indexes_countainer:


                    # Apply classifier
                    if self.classifier != '':

                        # ==== With features extraction ====
                        if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                                'eda' in self.signals_type) or self.filter != '':


                            extracted_features, selected_passbands, repository_selected_features_per_signals_type = self.extract_features_from_signals(train_index=train_index,
                                                                                    test_index=test_index,
                                                                                    repository_physiological_signals=repository_physiological_signals,
                                                                                    repository_EEG_passband_signals=repository_EEG_passband_signals)

                            classifier_ = self.apply_classifier_on_features(extracted_features)


                        # ==== Without Feature extraction ====
                        else:
                            # Work with EEG signals only
                            if 'EEG' in self.signals_type:
                                repository_EEG_passband_split_signals = self.split_signals(
                                    repository_EEG_passband_signals,
                                    train_index, test_index)
                                classifier_ = self.apply_classifier_on_repository_passband_signals(repository_EEG_passband_split_signals)
                            else:
                                raise NameError('The direct classification without feature extraction works with EEG signals only')

                    # Results
                    # ==== Hold selected passbands subject ==== (if multiple passbands, i.e. if filter bank)
                    if ('fb' in self.filter or 'fb' in self.classifier) and 'EEG' in self.signals_type:
                        if 'fb' in self.filter:
                            results.hold_selected_passband_subject(selected_passbands=selected_passbands)
                        else:
                            results.hold_selected_passband_subject(selected_passbands=classifier_.selected_passbands)


                    # Hold classifiers predictions cross validation
                    list_y_pred_cross_val.extend(classifier_.y_pred)
                    list_y_true_cross_val.extend(classifier_.y_true)
                    vector_size_train += classifier_.size_train
                    vector_size_test += classifier_.size_test

                # ==== Hold classifiers predictions subject ====
                results.hold_classification_prediction_vector_subject(subject=subject,
                                                                      y_pred=list_y_pred_cross_val,
                                                                      y_true=list_y_true_cross_val,
                                                                      size_train=vector_size_train,
                                                                      size_test=vector_size_test)

        # ==== Build repository of selected passbands, if multiple passbands ====
        if 'fb' in self.filter or 'fb' in self.classifier:
            results.generate_repository_selected_passbands(list_passbands=self.passband)


        # ==== Build table (pandas frame) of performances ====
        results.generate_performance_scores()
        results.build_frame_results(filter=self.filter,
                                    classifier=self.classifier,
                                    calibration_type=self.calibration_type,
                                    list_signal_types=self.signals_type)
        self.score_type = results.score_type

        # ==== Saving path for results dataframe ====
        if self.results_filename != '':
            results.store_results(results_path_folder_store=self.results_filename,
                                  calibration_type=self.calibration_type,
                                  filter=self.filter,
                                  signals_type=self.signals_type,
                                  classifier=self.classifier)


        ############ Temporary, find a better solution ############
        # Add this to the results constructor using the "generate_repository_selected_passbands" method 10 lines above
        if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                'eda' in self.signals_type) or self.filter != '':
            self.repository_features = pd.Series(repository_selected_features_per_signals_type)
            self.repository_features.T.to_csv(self.results_filename + 'subject_specific/selected_features/repository_features_per_signals.csv', index = False)

            self.selected_features_final = pd.DataFrame(self.selected_features_final)
            self.selected_features_final.to_csv(self.results_filename + 'subject_specific/selected_features/all_selected_features.csv', index = False)
        ################################################################################################


    def extract_signals_from_path(self, paths_list):
        """
        This method obtains a list of paths to data files in input. A signal structure is extracted from each file
        :param paths_list: list of paths to data files (types of files are usual signals format .mat, .gdf, .fif etc)
        :return: dict per passband of object signals, signals[passband].x -> data, signals[passband].y -> labels
        """

        if self.data_type == 'preprocessed data':

            # Import the adequate reader, for gdf or mat format
            char_import = 'from src.data.data_readers import ' + 'preprocessed_' + self.dataset_structure.format[1:]
            exec(char_import)

            char = 'preprocessed_' + self.dataset_structure.format[1:] + '.' + 'preprocessed_' + self.dataset_structure.format[1:] + '()'
            reader = eval(char)

            # Preprocessed data doesn't need filtering
            repository_passband_signals = OrderedDict()
            # first create the passband string patterns to seek for in files names
            for passband_ in self.passband:
                str_pattern = self.passband_delimiters[0] + str(passband_[0]) + self.passband_delimiters[1] + \
                str(passband_[1]) + self.passband_delimiters[2]
                # Loop over file
                for path_to_file in paths_list:
                    if str_pattern in path_to_file:
                        # Read the data
                        eeg_signals = reader.load_data(path_to_file)
                        repository_passband_signals[str(passband_)] = eeg_signals

        elif self.data_type == 'raw data':

            # Import the adequate reader, for gdf or mat format
            char_import = 'from src.data.data_readers import ' + 'raw_' + self.dataset_structure.format[1:]
            exec(char_import)

            char = 'raw_' + self.dataset_structure.format[
                                     1:] + '.' + 'raw_' + self.dataset_structure.format[1:] + '()'
            reader = eval(char)

            # Read the data
            repository_EEG_passband_signals, repository_physiological_signals = reader.load_data_dev(dataset=self.dataset,
                                                               list_files=paths_list,
                                                               specify_labeling=self.specify_labeling,
                                                               list_runs=self.list_runs,
                                                               list_sessions=self.list_sessions,
                                                               passband=self.passband,
                                                               dictionary_stimulations=self.dictionary_stimulations,
                                                               tmin=self.tmin,
                                                               tmax=self.tmax,
                                                               list_all_channels=self.list_all_channels,
                                                               list_channels_EEG=self.list_channels_EEG,
                                                               channel_eda=self.channel_eda,
                                                               channel_breathing=self.channel_breathing,
                                                               channel_heart_rate=self.channel_heart_rate,
                                                               list_eog=self.list_eog,
                                                               list_channels_to_drop=self.list_channels_to_drop)

        return repository_EEG_passband_signals, repository_physiological_signals


    def get_indexes_train_and_test_set(self,
                                       repository_signals={},
                                       train_split_ratio=0.0,# must be between 0 and 1
                                       type_split=''
                                       ):
        '''
        This method return the indexes of both the train and test sets based on the split ratio (between 0 and 1) and the type of split ('chronological' or 'shuffle')
        :param repository_signals: dictionary
        :param train_split_ratio: between 0 and 1, float
        :param type_split: 'chronological' or 'shuffle', string
        :return:
        '''
        if self.training_split_ratio != 0.0:
            train_split_ratio = self.training_split_ratio
        if self.type_split != '':
            type_split = self.type_split

        # Create an object
        splitter = split_signals.split_signals()

        # Call the method to get indexes of split data into train and test sets
        key_0 = list(repository_signals.keys())[0]
        index_train, index_test = splitter.split_index_based_on_ratio(repository_signals[str(key_0)],
                                                                      self.training_split_ratio,
                                                                      self.type_split)

        return index_train, index_test

    '''
    def split_signals(self, repository_signals):
        """
        Splits signals from each passband into a training set and a testing set.
        :param repository_passband_signals: dictionary with passbands as keys, eeg signals as values
        :return: dictionary with passbands as keys, dictionaries as values.
        Those dictionary values have two keys 'training set' and 'testing set' and get signals as values
        """
        repository_split_signals = {}

        # Create an object
        splitter = split_signals.split_signals()

        # Call the method to get indexes of split data into train and test sets
        key_0 = repository_signals.keys()[0]
        index_train, index_test = splitter.split_index_based_on_ratio(repository_signals[str(key)],
                                                                      self.training_split_ratio,
                                                                      self.type_split)

        # Call the method to to split data into train and test sets based on indexes
        for key, signals in repository_signals.items(): # key can be passband for EEG, or type of signal for physiological signals (ex: EDA, breathing, heart rate)
            splitter = split_signals.split_signals()
            repository_split_signals[key] = splitter.split_signals_based_on_index(signals, index_train, index_test)

        return repository_split_signals
    '''

    def split_signals(self, repository_signals, train_index, test_index):
        """
        Splits signals from each passdband into a training set and a testing set.
        :param repository_passband_signals: dictionary with passbands as keys, eeg signals as values
        :return: dictionary with passbands as keys, dictionaries as values.
        Those dictionaries values have two keys 'training set' and 'testing set' and get signals as values
        """
        repository_split_signals = OrderedDict()

        for key, signals in repository_signals.items(): # key can be passband for EEG, or type of signal for physiological signals (ex: EDA, breathing, heart rate)
            splitter = split_signals.split_signals()
            repository_split_signals[key] = \
            splitter.split_signals_index(signals, key, train_index, test_index)[key]

        return repository_split_signals



    def extract_features_from_signals(self, train_index=None, test_index=None, repository_EEG_passband_signals={},
                                      repository_physiological_signals={}):
        '''
        This method is called in order to extract features from the signals 
        :param train_index:
        :param test_index:
        :param repository_EEG_passband_signals:
        :param repository_physiological_signals:
        :return:
        '''
        selected_passbands = []
        repository_selected_features_per_signals_type = {}

        # Split signals of each passband into a train and a test set, for each k-fold
        if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or ('eda' in self.signals_type):
            repository_physiological_split_signals = self.split_signals(
                repository_physiological_signals, train_index, test_index)

        if 'EEG' in self.signals_type:
            repository_EEG_passband_split_signals = self.split_signals(repository_EEG_passband_signals,
                                                                                        train_index, test_index)

        # Extract physiological features from ['EDA', 'breathing', 'heart_rate']
        if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                'eda' in self.signals_type):

            physiological_features = self.extract_physiological_features(repository_physiological_split_signals)
            repository_selected_features_per_signals_type = physiological_features.repository_features_per_signals_type

            print('')
            print('PHYSIO ONLY')
            print(np.shape(physiological_features.features_train))
            print(np.shape(physiological_features.features_test))
            print('')


        # Apply filter (if filter) and extract features from EEG signals -> EEG only
        if self.filter != '' and 'EEG' in self.signals_type :

            filters_ = self.apply_filter(repository_EEG_passband_split_signals)

            if ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                'eda' in self.signals_type):

                # Now keep only the trials that are available for physio study as well
                filters_.features_train = filters_.features_train.loc[physiological_features.trials_train_mask,:]
                filters_.label_train = filters_.label_train[physiological_features.trials_train_mask]

                filters_.features_test = filters_.features_test.loc[physiological_features.trials_test_mask, :]
                filters_.label_test = filters_.label_test[physiological_features.trials_test_mask]

            print('')
            print('EEG ONLY')
            #print(filters_.features_train)
            print(np.shape(filters_.features_train))
            print(np.shape(filters_.features_test))
            print('')

        # Concatenating physiological features with EEG features if both types of features are used
        if ('EEG' in self.signals_type and self.filter != '') and (('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                'eda' in self.signals_type)):
            physiological_features.features_train = pd.concat([physiological_features.features_train, filters_.features_train], axis=1)
            physiological_features.features_test = pd.concat(
                [physiological_features.features_test, filters_.features_test], axis=1)

            extracted_features = physiological_features
            selected_passbands = filters_.selected_passbands

            print('')
            print('BOTH EEG and PHYSIO')
            # print(filters_.features_train)
            print(np.shape(extracted_features.features_train))
            print(np.shape(extracted_features.features_test))
            print('')

        else:

            if self.filter != '' and 'EEG' in self.signals_type:
                selected_passbands = filters_.selected_passbands
                extracted_features = filters_

            elif ('heart_rate' in self.signals_type) or ('breathing' in self.signals_type) or (
                'eda' in self.signals_type):
                extracted_features = physiological_features

        # For the submission paper #####################################################################3
        from src.utils import normalize
        normalized_features_train, mean_features, std_features = normalize.normalize_data(
            extracted_features.features_train.to_numpy(),
            extracted_features.label_train)
        #normalized_features_test = normalize.normalize_data(extracted_features.features_test, extracted_features.label_test,
        #                                               mean_features=mean_features, std_features=std_features)

        # skfeature model
        from skfeature.function.information_theoretical_based import MRMR
        index = MRMR.mrmr(X=normalized_features_train[:, :-1], y=normalized_features_train[:, -1], n_selected_features=9)
        extracted_features.features_train = extracted_features.features_train.iloc[:, index[:9]]
        extracted_features.features_test = extracted_features.features_test.iloc[:, index[:9]]

        if np.shape(extracted_features.features_test)[0] <= 1:
            extracted_features.features_train = extracted_features.features_train.iloc[:-4,:]
            extracted_features.features_test = extracted_features.features_train.iloc[-4:,:]
            extracted_features.label_train = extracted_features.label_train[:-4]
            extracted_features.label_test = extracted_features.label_train[-4:]

        self.selected_features_final[self.subject] = self.selected_features_final[self.subject] + list(
            extracted_features.features_train.columns.values)
        print('')
        print('selected features: ')
        print(np.shape(self.selected_features_final))
        print('')

        print('')
        print('aiiight shape: train')
        print(np.shape(extracted_features.features_train))
        print('aiiight shape: test')
        print(np.shape(extracted_features.features_test))
        #######################################################################################################

        return extracted_features, selected_passbands, repository_selected_features_per_signals_type




    def apply_filter(self, repository_passband_split_signals):
        """
        Filter the signals
        :param repository_passband_signals: dictionary, key -> passband, value -> signals
        :return:filters object, with filters_train and filters_test as attributes
        """
        # import the filter module
        char_import = 'from src.filters import ' + self.filter
        exec(char_import)

        # Create the filter object
        char = self.filter + '.' + self.filter + '()'
        filters_ = eval(char)
        filters_.fit(repository_passband_split_signals=repository_passband_split_signals,
                     filter_parameter=self.filter_parameter)
        filters_.transform(repository_passband_split_signals)

        return filters_

    def extract_physiological_features(self, repository_physiological_split_signals):



        features_extractor = physio_features_extractor.physio_features_extractor()
        features_extractor.fit(repository_physiological_split_signals, self.signals_type)

        features_extractor.transform()

        ############ Temporary, find a better solution ############
        if 'subject_' + str(self.subject) in self.repository_features.keys():
            self.repository_features['subject_' + str(self.subject)] = self.repository_features['subject_' + str(self.subject)] + features_extractor.selected_features
        else:
            self.repository_features['subject_' + str(self.subject)] = features_extractor.selected_features
        ############################################################

        return features_extractor





    def apply_classifier_on_features(self, features_):
        """
        Apply a classifier on filters
        :param filters_: filters object, with filters_train and filters_test as attributes.
        :return: classifier, containing the model and results
        """
        # import the filter module
        char_import = 'from src.classifiers import ' + self.classifier
        exec(char_import)

        # Create the filter object
        char = self.classifier + '.' + self.classifier + '()'
        classifier = eval(char)

        # Update classifier parameters
        classifier.parameter_classifier = self.classifier_parameter

        classifier.fit(X=features_.features_train, y=features_.label_train)
        classifier.predict(X=features_.features_test, y=features_.label_test)
        #classifier.score_accuracy(filters_.label_test)
        return classifier


    def apply_classifier_on_repository_passband_signals(self, repository_passband_split_signals):
        """
        Apply a classifier on signals
        :param repository_passband_split_signals : dictionary with passbands as keys, dictionaries as values.
        Those dictionary values have two keys 'training set' and 'testing set' and get signals as values
        :return: classifier, containg the model and results
        """
        # import the filter module
        char_import = 'from src.classifiers import ' + self.classifier
        exec(char_import)

        # Create the filter object
        char = self.classifier + '.' + self.classifier + '()'
        classifier = eval(char)

        # Update classifier parameters
        classifier.parameter_classifier = self.classifier_parameter

        classifier.fit(repository_passband_split_signals, set_='training_set', classifier_parameter=self.classifier_parameter)
        classifier.predict(repository_passband_split_signals, set_='testing_set')
        #classifier.score_accuracy()
        return classifier


if __name__ == '__main__':
    subject_specific()