# -*- coding: utf-8 -*-

"""
The class subject_specific runs the cross-validation study
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License

from src.utils import split_signals
from sklearn import model_selection
import statistics
from collections import OrderedDict
from sklearn.metrics import f1_score
from src.results import results_constructor

class cross_validation(object):

    def __init__(self):
        # Calibration
        self.calibration_type = 'subject_specific'

        # Dataset
        # === all data types ===
        self.data_type = ''  # 'raw' or 'preprocessed'
        self.dataset = ''  # (Ex: 'bci_competition_4_dataset_2a')
        self.passband = []  # set of aassbands data should be filtered into
        self.training_ratio = 0.0  # split ratio for the training set (Ex: 0.8 for keeping 80% of the data for the training set)
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
        self.list_statistical_tests = []
        self.list_plots = []
        # ==== Saving path for results dataframe ====
        self.results_filename = ''





        self.kfold=10

    '''
    def extract_signals_from_path_dev(self, paths_list):
        """
        This method obtains a list of paths to data files in input. A signal structure is extracted from each file
        :param paths_list: list of paths to data files (types of files are usual signals format .mat, .gdf, .fif etc)
        :return: object signals, signals.x -> data, signals.y -> labels
        """
        char_import = 'from src.data.data_readers import ' + self.dataset_structure.format[1:]
        exec(char_import)
        char = self.dataset_structure.format[1:] + '.' + self.dataset_structure.format[1:] + '()'
        reader = eval(char)   
            
        if self.data_type=='preprocessed data':
            repository_passband_signals = OrderedDict()
            # first create the passband string patterns to seek for in files names
            for passband_ in self.passband:
                str_pattern = self.passband_delimiters[0] + str(passband_[0]) + self.passband_delimiters[1] + \
                str(passband_[1]) + self.passband_delimiters[2]
                for path_to_file in paths_list:
                    if str_pattern in path_to_file:
                        # Import the reader module
                        char_import = 'from src.data.data_readers import ' + self.dataset_structure.format[1:]
                        exec(char_import)
                        # Create the reader object
                        char = self.dataset_structure.format[1:] + '.' + self.dataset_structure.format[1:] + '()'
                        reader = eval(char)
                        eeg_signals = reader.load_data(path_to_file)
                        repository_passband_signals[str(passband_)] = eeg_signals
        else:                
            repository_passband_signals = reader.load_data_dev(paths_list,passband=self.passband, tmin=self.tmin, tmax=self.tmax)

        return repository_passband_signals 
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

    def run_study_dev(self, cross_val_type='leave_one_out'):



        #self.vector_score = []
        cross_val_type='K-fold'
        cross_val_type = 'leave_one_out'
        results = results_constructor.results_constructor()


        # First extract the signals from subjects' files
        for subject, files_list in self.dataset_structure.repository_subjects_files.items():

            # Check if subject in list subject to keep
            if subject in self.dataset_structure.list_subjects_to_keep:

                # Initialize subject holding parameters
                list_y_pred_cross_val = []
                list_y_true_cross_val = []
                vector_size_train = 0
                vector_size_test = 0

                #vector_y_true_subject, vector_y_pred_subject = [], []

                # Read signals from subjects files
                paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]
                repository_passband_signals = self.extract_signals_from_path_dev(paths_list) # Structure, signals.x -> signals, signals.y -> labels

                if cross_val_type == 'leave_one_out':


                    #eeg_signals_first = repository_passband_signals[str(self.passband[0])]

                    # Get the number of split
                    loo = model_selection.LeaveOneOut()
                    loo.get_n_splits(repository_passband_signals[str(self.passband[0])].y)
                    object_indexes_countainer = loo.split(repository_passband_signals[str(self.passband[0])].X.T)


                elif cross_val_type == 'K-fold':
                    # Get the number of split
                    # kf = model_selection.StratifiedShuffleSplit(n_splits=self.kfold, )
                    #eeg_signals_first = repository_passband_signals[str(self.passband[0])]


                    kf = model_selection.StratifiedShuffleSplit(n_splits=self.kfold)
                    object_indexes_countainer = kf.split(repository_passband_signals[str(self.passband[0])].X.T, y=repository_passband_signals[str(self.passband[0])].y)

                else:
                    raise Exception('You need to indicate which type of cross validation you want !')


                for train_index, test_index in object_indexes_countainer:

                    # Split signals of each passband into a train and a test set, for each k-fold
                    repository_passband_split_signals = self.split_signals_cross_validation(repository_passband_signals, train_index, test_index)

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
                            classifier_ = self.apply_classifier_on_repository_passband_signals(repository_passband_split_signals)

                    # Results
                    # ==== Hold selected passbands subject ==== (if multiple passbands, i.e. if filter bank)
                    if 'fb' in self.filter or 'fb' in self.classifier:
                        if 'fb' in self.filter:
                            results.hold_selected_passband_subject(subject=subject, selected_passbands=filters_.selected_passbands)
                        else:
                            results.hold_selected_passband_subject(subject=subject, selected_passbands=classifier_.selected_passbands)

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

        # ==== Build repository of selected passands, if multiple passbands ====
        if 'fb' in self.filter or 'fb' in self.classifier:
            results.generate_repository_selected_passbands(list_passbands=self.passband)

        # ==== Build table (pandas frame) of performances ====
        results.generate_performance_scores()
        results.build_frame_results(filter=self.filter, classifier=self.classifier,
                                    calibration_type=self.calibration_type)

        # ==== Analysis to make ====
        if self.list_plots != [] and self.list_statistical_tests != []:
            results.display_statistics(list_plots=self.list_plots,
                                       list_statistical_tests=self.list_statistical_tests)

        # ==== Saving path for results dataframe ====
        if self.results_filename != '':
            results.store_results(results_filename=self.results_filename)



        '''
                        if self.classifier != '':
                        
                            if self.filter != '':
                                filters_ = self.apply_filter(repository_passband_signals_split)
                                y_true, y_pred = self.apply_classifier_on_filters(filters_)
                                vector_y_true_subject.append(y_true[0])
                                vector_y_pred_subject.append(y_pred[0])
                            else:
                                y_true,y_pred=self.apply_classifier_on_repository_passband_signals(repository_passband_signals_split)
                                vector_y_true_subject.append(y_true[0])
                                vector_y_pred_subject.append(y_pred[0])
                            
                else:
                    kf = model_selection.StratifiedShuffleSplit(n_splits=self.kfold,)
                    eeg_signals_first=repository_passband_signals[str(self.passband[0])]
                    kf = model_selection.StratifiedShuffleSplit(n_splits=self.kfold)

                    for train_index, test_index in kf.split(eeg_signals_first.X.T,y=eeg_signals_first.y):
                        repository_passband_signals_split =self.split_signals_cross_validation(repository_passband_signals, train_index, test_index)
                        if self.classifier != '':
                            
                            if self.filter != '':
                                filters_=self.apply_filter(repository_passband_signals_split)
                                y_true, y_pred = self.apply_classifier_on_filters(filters_)
                                vector_y_true_subject.extend(y_true)
                                vector_y_pred_subject.extend(y_pred)
                            else:
                                y_true,y_pred=self.apply_classifier_on_repository_passband_signals(repository_passband_signals_split)
                                vector_y_true_subject.extend(y_true)
                                vector_y_pred_subject.extend(y_pred)
           
                print(subject)
                self.vector_score.append(f1_score(vector_y_true_subject, vector_y_pred_subject))

        print(self.vector_score)
        print(statistics.mean(self.vector_score))
    '''
        
    def run_study(self, cross_val_type='leave_one_out'):
        self.vector_score = []
        # First extract the signals from subjects' files
        #subject = 'subject_1'
        for subject, files_list in self.dataset_structure.repository_subjects_files.items():
            vector_y_true_subject, vector_y_pred_subject = [], []
            # Read signals from subjects files
            paths_list = [self.dataset_structure.dataset_directory + subject + '/' + file for file in files_list]
            repository_passband_signals = self.extract_signals_from_path(paths_list) # Structure, signals.x -> signals, signals.y -> labels
            print("bb")

            if cross_val_type == 'leave_one_out':
                # Split signals of each passband into a train and a test set,
                # ends up with a 2-keys repository of eeg_signals values into a passbands repository
                #for passband
                list_repository_passband_split_signals = self.split_signals(repository_passband_signals)

            # in leave-one-out, the number of repository_passband_split_signals in the list is equal to the number of trials (1 trial as test set in each repository)
            for repository_passband_split_signals in list_repository_passband_split_signals :

                if self.classifier != '':

                    if self.filter != '':
                        # Apply filter
                        filters_ = self.apply_filter(repository_passband_split_signals)

                        # Apply classifier
                        y_true, y_pred = self.apply_classifier_on_filters(filters_)
                        vector_y_true_subject.append(y_true[0])
                        vector_y_pred_subject.append(y_pred[0])

                    else:
                        # Apply classifier
                        y_true, y_pred = self.apply_classifier_on_repository_passband_signals(repository_passband_split_signals)
                        vector_y_true_subject.append(y_true[0])
                        vector_y_pred_subject.append(y_pred[0])
            print(subject)
            self.vector_score.append(f1_score(vector_y_true_subject, vector_y_pred_subject, average = 'weighted'))
            print(self.vector_score)

        print(self.vector_score)
        print(statistics.mean(self.vector_score))

    def extract_signals_from_path(self, paths_list):
        """
        This method obtains a list of paths to data files in input. A signal structure is extracted from each file
        :param paths_list: list of paths to data files (types of files are usual signals format .mat, .gdf, .fif etc)
        :return: object signals, signals.x -> data, signals.y -> labels
        """
        repository_passband_signals = OrderedDict()
        for passband_ in self.passband:
            # first create the passband string patterns to seek for in files names
            str_pattern = self.passband_delimiters[0] + str(passband_[0]) + self.passband_delimiters[1] + \
                          str(passband_[1]) + self.passband_delimiters[2]

            for path_to_file in paths_list:
                #print(path_to_file)
                if str_pattern in path_to_file:
                    # Import the reader module
                    char_import = 'from src.data.data_readers import ' + self.dataset_structure.format[-3:]
                    exec(char_import)
                    # Create the reader object
                    char = self.dataset_structure.format[-3:] + '.' + self.dataset_structure.format[-3:] + '()'
                    reader = eval(char)
                    eeg_signals = reader.load_data(path_to_file)
                    repository_passband_signals[str(passband_)] = eeg_signals
                else:
                    char_import = 'from src.data.data_readers import ' + self.dataset_structure.format[-3:]
                    exec(char_import)
                    # Create the reader object
                    char = self.dataset_structure.format[-3:] + '.' + self.dataset_structure.format[-3:] + '()'
                    reader = eval(char)
                    print(path_to_file)
                    eeg_signals = reader.load_data([path_to_file])
                    repository_passband_signals[str(passband_)] = eeg_signals
                    

        return repository_passband_signals

    def split_signals(self, repository_passband_signals):
        """
        Splits signals from each passdband into a training set and a testing set.
        :param repository_passband_signals: dictionary with passbands as keys, eeg signals as values
        :return: dictionary with passbands as keys, dictionaries as values.
        Those dictionary values have two keys 'training set' and 'testing set' and get signals as values
        """
        repository_passband_split_signals = OrderedDict()
        list_passbands = []
        for passband, eeg_signals in repository_passband_signals.items():
            nb_trials = len(eeg_signals.y)
            kf = model_selection.KFold(n_splits=nb_trials)

            splitter = split_signals.split_signals()
            repository_passband_split_signals[passband] = splitter.split_signals_leave_one_out(eeg_signals, passband, kf)
            list_passbands.append(passband)

        # Create the list of repositories. Lenght of the list is equal to the number of trial if leave-one-out cross val
        list_combination_repository_passband_split_signals = []
        nb_combinations = len(list(repository_passband_split_signals.values())[0])

        # Reverse the dictionary of list of passbanded signals into a list of dictionary of passbanded signals
        for i in range(nb_combinations):
            ephemere_repo = OrderedDict()
            for passband in list_passbands:
                ephemere_repo[passband] = repository_passband_split_signals[passband][i][passband]

            list_combination_repository_passband_split_signals.append(ephemere_repo)

        return list_combination_repository_passband_split_signals

    def split_signals_cross_validation(self, repository_passband_signals,train_index,test_index):
        """
        Splits signals from each passdband into a training set and a testing set.
        :param repository_passband_signals: dictionary with passbands as keys, eeg signals as values
        :return: dictionary with passbands as keys, dictionaries as values.
        Those dictionary values have two keys 'training set' and 'testing set' and get signals as values
        """
        repository_passband_split_signals = OrderedDict()
        for passband, eeg_signals in repository_passband_signals.items():
            splitter = split_signals.split_signals()
            repository_passband_split_signals[passband] = splitter.split_signals_index(eeg_signals, passband, train_index, test_index)[passband]
            
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

        filters_.fit(repository_passband_split_signals)
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

        classifier.fit(filters_.filter_train, filters_.label_train)
        classifier.predict(filters_.filter_test)
        y_true, y_pred = classifier.score_fisher(filters_.label_test)
        return y_true, y_pred

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

        classifier.fit(repository_passband_split_signals, set_='training_set')
        classifier.predict(repository_passband_split_signals, set_='testing_set')
        y_true, y_pred = classifier.score_fisher()
        return y_true, y_pred