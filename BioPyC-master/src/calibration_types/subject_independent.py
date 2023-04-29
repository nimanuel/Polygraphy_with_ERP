# -*- coding: utf-8 -*-

"""
The class subject_specific runs the subject specific study
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License

from src.utils import split_signals
from collections import OrderedDict
import pandas as pd
import numpy as np
from src.results import results_constructor


class subject_independent(object):

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
        self.specify_labeling = None  # Meaning you have to implement a script to labelize your data
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


    def run_study_classic(self):

        results = results_constructor.results_constructor()

        # Going along all subjects as testing set
        for subject_test in self.dataset_structure.list_subjects_to_keep:

            list_repository_passband_signals_train = []
            repository_passband_split_signals, repository_passband_signals_train, repository_passband_signals_test = {}, {}, {}

            # Going all subjects as training + testing set, then split all subjects as train vs 1 subject as test.
            for subject, files_list in self.dataset_structure.repository_subjects_files.items():

                # Read signals from subjects files
                paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]

                if subject == subject_test:
                    repository_passband_signals_test = self.extract_signals_from_path_dev(
                        paths_list)  # Structure, signals.X -> signals, signals.y -> labels
                else:
                    repository_passband_signals_train = self.extract_signals_from_path_dev(
                        paths_list)  # Structure, signals.X -> signals, signals.y -> labels
                    list_repository_passband_signals_train.append(repository_passband_signals_train)

            # Split signals of each passband into a train and a test set,
            repository_passband_split_signals = self.split_signals_dev(list_repository_passband_signals_train=list_repository_passband_signals_train,
                                                                       repository_passband_signals_test=repository_passband_signals_test)

            # Apply filter (if filter)

            if self.filter != '':
                filters_ = self.apply_filter(repository_passband_split_signals)

            # Apply classifier
            if self.classifier != '':

                # ==== With Filter ====
                if self.filter != '':
                    classifier_ = self.apply_classifier_on_filters(filters_)

                # ==== Without Filter ====
                else:
                    classifier_ = self.apply_classifier_on_repository_passband_signals(
                        repository_passband_split_signals)

            # Results
            # ==== Hold selected passbands subject ==== (if multiple passbands, i.e. if filter bank)
            if 'fb' in self.filter or 'fb' in self.classifier:
                if 'fb' in self.filter:
                    results.hold_selected_passband_subject(selected_passbands=filters_.selected_passbands)
                else:
                    results.hold_selected_passband_subject(selected_passbands=classifier_.selected_passbands)

            # ==== Hold classifiers predictions subject ====
            results.hold_classification_prediction_vector_subject(subject=subject_test,
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

        # ==== Analysis to make ====
        #if self.list_plots != [] and self.list_statistical_tests != []:
        #    results.display_and_store_statistics(list_plots=self.list_plots,
        #                                         list_statistical_tests=self.list_statistical_tests,
        #                                         results_path_folder_store=self.results_filename)

        # ==== Saving path for results dataframe ====
        if self.results_filename != '':
            results.store_results(results_path_folder_store=self.results_filename,
                                  calibration_type=self.calibration_type,
                                  filter=self.filter,
                                  classifier=self.classifier)


    '''    
    def run_study_dev(self):

        selected_passband=[]


        # Going along all subjects as testing set
        for subject_test in self.dataset_structure.list_subjects_to_keep:

            list_repository_passband_signals_train = []
            repository_passband_split_signals, repository_passband_signals_train, repository_passband_signals_test = {}, {}, {}

            # Going all subjects as training + testing set, then split all subjects as train vs 1 subject as test.
            for subject, files_list in self.dataset_structure.repository_subjects_files.items():

                # Read signals from subjects files
                paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]

                if subject == subject_test:
                    repository_passband_signals_test = self.extract_signals_from_path_dev(
                        paths_list)  # Structure, signals.X -> signals, signals.y -> labels
                else:
                    repository_passband_signals_train = self.extract_signals_from_path_dev(
                        paths_list)  # Structure, signals.X -> signals, signals.y -> labels
                    list_repository_passband_signals_train.append(repository_passband_signals_train)

            # Split signals of each passband into a train and a test set,
            # ends up with a 2-keys repository ('training_set' and 'testing_set') of eeg_signals values into a passbands repository
            repository_passband_split_signals = self.split_signals_dev(list_repository_passband_signals_train=list_repository_passband_signals_train,
                                                                       repository_passband_signals_test=repository_passband_signals_test)

            # Apply filter
            if self.filter != '':
                filters_ = self.apply_filter(repository_passband_split_signals)
                if self.filter == 'fbcsp':
                    selected_passband.extend(np.array(filters_.passband_selected))

            # Apply classifier
            if self.classifier != '':

                if self.filter != '':
                    classifier = self.apply_classifier_on_filters(filters_)
                    self.hold_results(classifier)  # create 3 vectors : accuracy score, y_pred and y_true

                else:
                    classifier = self.apply_classifier_on_repository_passband_signals(
                        repository_passband_split_signals)
                    self.hold_results(classifier)  # create 3 vectors : accuracy score, y_pred and y_true

        frame_results = self.store_results()
        frame_results.to_csv(self.results_filename, index=False, header=True)

        import statistics
        print(self.vector_score)
        print(statistics.mean(self.vector_score))
        selected_passband.sort()
        print(Counter(selected_passband))
    '''

    def extract_signals_from_path_dev(self, paths_list):
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
            repository_passband_signals = reader.load_data_dev(dataset=self.dataset,
                                                               list_files=paths_list,
                                                               specify_labeling=self.specify_labeling,
                                                               list_runs=self.list_runs,
                                                               list_sessions=self.list_sessions,
                                                               passband=self.passband,
                                                               dictionary_stimulations=self.dictionary_stimulations,
                                                               tmin=self.tmin,
                                                               tmax=self.tmax,
                                                               list_all_channels=self.list_all_channels,
                                                               list_eog=self.list_eog,
                                                               list_channels_to_drop=self.list_channels_to_drop)

        return repository_passband_signals


    def split_signals_dev(self, list_repository_passband_signals_train=[], repository_passband_signals_test={}):

        repository_passband_split_signals = {}

        # Check if the number of subject for the training set is equal to the number of subject to keep minus the subject test
        assert (len(list_repository_passband_signals_train) == len(self.dataset_structure.list_subjects_to_keep) - 1,
                'Number of subjects for the train set should be the number of subjects that ahve been kept for the study, minus 1')


        if repository_passband_signals_test != {}:

            # Create an object for splitting data of the subject test into the ratio of trials for teh testing set
            splitter = split_signals.split_signals()

            # Call the method to get indexes of split data of the test set
            index_train, index_test = splitter.split_index_based_on_ratio(
                repository_passband_signals_test[str(self.passband[0])],
                self.training_split_ratio, self.type_split)

            for passband, signals_test in repository_passband_signals_test.items():
                passband_set = {}

                # Deal with training set
                first_elmt = True
                for repository_passband_signals_train in list_repository_passband_signals_train:
                    if first_elmt == True:
                        split_signals_train = repository_passband_signals_train[passband]
                        first_elmt = False
                    else:
                        split_signals_train.X = np.concatenate([split_signals_train.X,
                                                                repository_passband_signals_train[passband].X],
                                                               axis=2)
                        split_signals_train.y = np.concatenate([split_signals_train.y,
                                                                repository_passband_signals_train[passband].y])

                passband_set['training_set'] = split_signals_train

                # Deal with testing set
                passband_set['testing_set'] = splitter.split_signals_based_on_index(signals_test, index_train, index_test)['testing_set']

                # Add both training and testing sets to the passband repository
                repository_passband_split_signals[passband] = passband_set

        return repository_passband_split_signals


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

    def apply_classifier_on_filters(self, filters_):
        """
        Apply a classifier on filters
        :param filters_: filters object, with filters_train and filters_test as attributes.
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
        classifier.fit(X=filters_.filter_train, y=filters_.label_train)
        classifier.predict(filters_.filter_test, y=filters_.label_test)
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
        classifier.score_accuracy()
        return classifier

    def hold_results(self, classifier):
        '''
        Store classifier predictions, real values of the test set and results into vectors for each subject
        :param classifier: object of the used classifier, containing y_true, y_pred and accuracy score
        :return:
        '''
        self.array_y_pred.append(classifier.y_pred)
        self.array_y_true.append(classifier.y_true)
        self.vector_score.append(classifier.accuracy_score)
        self.vector_size_train.append(classifier.size_train)
        self.vector_size_test.append(classifier.size_test)

    def store_results(self):
        '''
        Create a pandas dataframe to store the results : rows are subjects' IDs; columns are accuracy_score, y_pred, y_true
        :return: a pandas dataframe [nb_subjects * (3 + 2*max_trials_test)]
        '''
        # Sort the list of subjects
        self.dataset_structure.list_subjects_to_keep = self.dataset_structure.sort_subjects_list(self.dataset_structure.list_subjects_to_keep)

        # Create a vector of data for each subject
        max_trials_test = max(self.vector_size_test)
        for i in range(len(self.dataset_structure.list_subjects_to_keep)):
            nb_trials_test = self.vector_size_test[i]
            diff_subj_max_trials_test = max_trials_test - nb_trials_test

            # Create a vector for each subject, containing main information + y_pred + y_true concatenate in a line
            # (completed with nans since all subejcts do not have the same number of trials in the test set)
            vector_subject = np.array([[self.dataset_structure.list_subjects_to_keep[i]] + [self.vector_score[i]] +
                                      [self.vector_size_train[i]] + [self.vector_size_test[i]] + list(self.array_y_pred[i]) +
                                      list(self.array_y_true[i]) + [np.nan for i in range(diff_subj_max_trials_test*2)]])
            if i == 0 :
                list_vector_subject = vector_subject
            else:
                list_vector_subject = np.concatenate([vector_subject, list_vector_subject], axis=0)

        frame_results = pd.DataFrame(list_vector_subject)
        frame_results = frame_results[::-1]
        frame_results = frame_results.rename(columns={0:'subjects IDs',
                                                            1: 'accuracy_score',
                                                            2: 'train set size',
                                                            3: 'test set size'})

        return frame_results
