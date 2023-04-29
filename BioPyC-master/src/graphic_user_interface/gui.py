# -*- coding: utf-8 -*-
"""
This file contains both calls for the GUI and calls for the model
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


from src.data import dataset_constructor
from src.results.analysis_constructor import analysis_constructor

class gui(object):

    def __init__(self, application_directory):
        # Signals type : type of signals you want to use in your study
        self.signals_type = [] # ['EEG', 'heart_rate', 'EDA', 'breathing']

        # data types : the can either be preprocessed data (data_type = 'preprocessed') or raw data (data_type = raw)
        self.data_type = ''

        self.dataset_structure = None # Will be and object, representation of the dataset structure, easily manipulable

        # Location of the application folder on user's computer
        self.application_directory = application_directory

        # Datasets
        self.list_available_datasets = None # List of all available datasets
        self.dataset = '' # Chosen dataset

        # List of subjects for the study
        self.list_available_subjects = []
        self.list_subjects_to_keep = []

        # List of sessions
        self.list_sessions= []

        # List of runs
        self.list_runs = []

        # List of channels
        self.list_all_channels = []
        self.dictionary_signal_type_channel = {} # Example {'EEG' : ['FP1', AFz', etc], 'eda': ['channel 67']}
        self.list_channels_EEG = []  # List of channels ['FP1', AFz', etc]
        self.channel_breathing = ''  # name of the channel used for breathing, ex 'channel 65'
        self.channel_eda = ''  # name of the channel used for eda, ex 'channel 67'
        self.channel_heart_rate = ''  # name of the channel used for heart rate, ex 'channel 68'

        # list of EOG
        self.list_eog = []

        # List of channels to drop
        self.list_channels_to_drop = []

        self.dictionary_stimulations = []
        self.tmin = {}  # Ex: self.tmin = {'breathing': -10.0, 'eda': -10.0, 'heart_rate': -10.0, 'EEG': -4.0}
        self.tmax = {}  # Ex : self.tmax = {'breathing': 6.0, 'eda': 6.0, 'heart_rate': 6.0, 'EEG': 0.0}

        # Filters
        self.list_available_filters = None # List of all available filters
        self.list_filters = '' # Chosen filter

        # Classifiers
        self.list_available_classifiers = None  # List of all available classifiers
        self.list_classifiers = ''  # Chosen classifier

        # Passbands
        self.passband = [] # List, or unique value, of passband to use

        # Passbands delimiters
        self.passband_delimiters = [] # List of passband delimiters

        # Calibration / Evaluation
        self.calibration_type = [] # Can be ['subject-specific', 'subject-independent']  or ['subject-specific'] or ['subject-independent']
        self.evaluation_type = '' # can be 'classic' or 'cross_validation'
        # if classic subject specific or subject independent evaluation
        self.training_ratio = 0.0 # Float
        self.type_split = '' # 'chronological' or 'shuffle'
        # if cross validation
        self.cross_val_type = ''  # 'k-fold' or 'leave_one-out'
        self.kfold = 0  # number of k kold for the cross validation
        self.type_split = ''  # 'chronological' or 'shuffle'

        # Results filename
        self.results_filename = '' # String absolute path to the results folder

        # Study type
        self.study_type = ''  # Chosen study type

        # score type
        self.score_type = ''


    def run_study_voila(self, studies_parameters=None):
        '''
        Run the study with parameters and implementation that are specific to "voila".
        :param studies_parameters: object with all parameters that are necessary for running the study,
        i.e., signals type, calibration type, preprocessing parameters, etc
        :return: nothing, just calling the run_study_voila_single_calibration and run_analysis to make statistics and plottings on results
        '''


        # Build an object to specify parameters for your study
        parameters_object = studies_parameters

        # set list of calibration types
        calibration_types = parameters_object.calibration_type

        # Set the application directory
        parameters_object.application_directory = self.application_directory

        parameters_object.results_filename = self.application_directory + 'data_store/results/' + parameters_object.dataset + '/'

        # Run studies under one calibration (either subject specific or subject independent)
        if len(calibration_types)==1:
            self.run_study_voila_single_calibration(parameters_object, calibration=calibration_types[0])

        # Run studies under each calibration (subject specific and independent)
        elif len(calibration_types)!=0:
            for calibration in calibration_types:
                self.run_study_voila_single_calibration(parameters_object=parameters_object, calibration=calibration)

        self.run_analysis(parameters_object=parameters_object, score_type=self.score_type, calibration_types=calibration_types)


    def run_study_voila_single_calibration(self, parameters_object=None, calibration=''):

        #parameters_object.calibration_type = calibration

        # Import module
        char_import = 'from src.calibration_types import ' + calibration
        exec(char_import)

        # Create a dataset structure
        self.dataset_structure = dataset_constructor.dataset_constructor(
            application_directory=self.application_directory,
            dataset_name=parameters_object.dataset,
            data_type=parameters_object.data_type)

        # Check if restrictions about the number of participants to keep for the study
        if parameters_object.list_subjects_to_keep != []:
            self.list_subjects_to_keep = ['subject_' + str(num) for num in
                                          parameters_object.list_subjects_to_keep]  # Precise in parameters which participants to keep, in a list

            self.dataset_structure.list_subjects_to_keep = self.list_subjects_to_keep

        # Seek for subjects' files
        self.dataset_structure.seek_for_subjects_files()

        # Creating a study
        char = calibration + '.' + calibration + '()'
        study = eval(char)  # type object, calling one of the scripts from "study_types" folder

        # ==============================
        # Updating "study"'s attributes
        # ==============================

        # Dataset
        # === global parameters ===
        if parameters_object.dataset_format != '':  # the format of the dataset, i.e. .mat, .gdf etc
            self.dataset_structure.format = parameters_object.dataset_format
        else:  # Seek for the data format
            self.dataset_structure.seek_for_files_format()
        study.dataset_structure = self.dataset_structure
        study.signals_type = parameters_object.signals_type #
        study.data_type = parameters_object.data_type  # 'raw' either 'preprocessed'
        study.dataset = parameters_object.dataset  # (Ex: 'bci_competition_4_dataset_2a')
        # study.passband = parameters_object.passband # set of aassbands data should be filtered into
        study.training_split_ratio = float(parameters_object.training_split_ratio)  # split ratio for the training set (Ex: 0.8 for keeping 80% of the data for the training set)
        study.type_split = parameters_object.type_split  # 'chronological' or 'shuffle'
        study.cross_val_type = parameters_object.cross_val_type # 'k-fold' or 'leave_one-out'
        study.kfold = parameters_object.kfold # number of k kold for the cross validation. Ex : kfold = 5

        # === preprocessed data === (no list of runs/session, should have been concatenated during the preprocessing)
        study.passband_delimiters = parameters_object.passband_delimiters

        # === raw data === (parameters for the preprocessing)
        study.specify_labeling = parameters_object.specify_labeling  # Meaning you have to implement a script to labelize your data
        study.list_sessions = parameters_object.list_sessions  # list containing integers of the sessions (Ex: [1,2])
        study.list_runs = parameters_object.list_runs  # list containing integers of the runs (Ex: [1,2,3,4])
        study.dictionary_stimulations = parameters_object.dictionary_stimulations  # (Ex: {'right':1, 'left':2})

        # Ex: self.tmin = {'breathing': -10.0, 'eda': -10.0, 'heart_rate': -10.0, 'EEG': -4.0}
        # self.tmax = {'breathing': 6.0, 'eda': 6.0, 'heart_rate': 6.0, 'EEG': 0.0}
        study.tmin = parameters_object.tmin  # start time window signal, can before/after the stimulation (Ex: 2.5 for 2,5 sec after stimulation)
        study.tmax = parameters_object.tmax  # stop time window signal, can before/after the stimulation (Ex: -1.0 for 1 sec before the stimulation)

        # split the dictionary of the channel lists associated with the different types of signals
        study.list_all_channels = parameters_object.list_all_channels  # list of channels ['channel_1', 'channels_2', etc]

        #study.list_channels_EEG = parameters_object.list_channels_EEG  #list of channels used for EEG, ex ['AFP1', 'Fz', etc]
        if 'EEG' in parameters_object.dictionary_signals_channels.keys():
            study.list_channels_EEG = parameters_object.dictionary_signals_channels['EEG']

        #study.channel_eda = parameters_object.channel_eda  # name of the channel used for eda, ex 'channel 68'
        if 'eda' in parameters_object.dictionary_signals_channels.keys():
            study.channel_eda = parameters_object.dictionary_signals_channels['eda'][0]  # name of the channel used for eda, ex 'channel 68'

        #study.channel_breathing = parameters_object.channel_breathing  # name of the channel used for breathing, ex 'channel 68'
        if 'breathing' in parameters_object.dictionary_signals_channels.keys():
            study.channel_breathing = parameters_object.dictionary_signals_channels['breathing'][0]  # name of the channel used for breathing, ex 'channel 68'

        #study.channel_heart_rate = parameters_object.channel_heart_rate  # name of the channel used for heart rate, ex 'channel 68'
        if 'heart rate' in parameters_object.dictionary_signals_channels.keys():
            study.channel_heart_rate = parameters_object.dictionary_signals_channels['heart rate'][0]  # name of the channel used for heart rate, ex 'channel 68'


        study.list_eog = parameters_object.list_eog  # list EOGs ['eog_1', 'eog_2', etc]
        study.list_channels_to_drop = parameters_object.list_channels_to_drop  # list of channels ['unnamed_1', 'unnamed_2', etc]



        # Results settings
        # ==== Evaluation ====
        if parameters_object.evaluation_type == 'cross-validation':
            study.evaluation_type = 'cross_validation'  # 'cross_validation'
        else:
            study.evaluation_type = parameters_object.evaluation_type  # 'classic' or 'cross_validation'

        # ==== Analysis to make ====
        study.list_statistical_tests = parameters_object.list_statistical_tests
        study.list_plots = parameters_object.list_plots
        # ==== Saving path for results dataframe ====
        study.results_filename = parameters_object.results_filename

        ##############################################################################################
        # Temporary issues
        if calibration == "subject_independent":
            raise Exception(
                'Some issues have been reported and the subject independent calibration is currently not usable. Please use subject_specific calibration only.')

        if ('heart_rate' in study.signals_type or 'breathing' in study.signals_type or 'eda' in study.signals_type) and 'EEG' not in study.signals_type:
            raise Exception(
                'So far the physiological signals can only be used and combined with EEG features (extracted using the CSP or FBCSP filters).')

        ##############################################################################################

        # Run the studies
        for classifier in parameters_object.list_classifiers:

            if classifier == 'lda' or classifier == 'svm':

                # For EEG features
                if parameters_object.list_filters != [] and 'EEG' in parameters_object.signals_type :




                    for filter in parameters_object.list_filters:

                        if 'fb' in filter:
                            study.passband = parameters_object.passband_repository['filter_bank']
                        else:
                            study.passband = parameters_object.passband_repository['single']

                        self.run_single_study(study=study,
                                              evaluation_type=study.evaluation_type,
                                              filter=filter,
                                              filter_parameter=parameters_object.filter_parameter,
                                              classifier=classifier,
                                              classifier_parameter=parameters_object.classifier_parameter)


                # For physiological features
                elif 'eda' in parameters_object.signals_type or 'breathing' in parameters_object.signals_type or 'heart_rate' in parameters_object.signals_type :

                    if 'EEG' in parameters_object.signals_type : # that means that parameters_object.list_filters == [] and no filters have been chosen to extract EEG features

                        raise Exception(
                            'You cannot combine physiological features with EEG ones if you did not choose a EEG filter (either CSP or FBCSP) before.')
                    else:
                        filter = '' # No EEG filters

                        self.run_single_study(study=study,
                                              evaluation_type=study.evaluation_type,
                                              filter=filter,
                                              filter_parameter=parameters_object.filter_parameter,
                                              classifier=classifier,
                                              classifier_parameter=parameters_object.classifier_parameter)
                else:
                    raise Exception(
                        'If you want to apply linear classifiers such as LDA or SVM on your signals, you therefore have to use spatial filter such as CSP or FBCSP if EEG signals, or extract multiple features from physiological signals such as EDA, breathing or heart rate. ')

            else:
                if 'eda' in parameters_object.signals_type or 'breathing' in parameters_object.signals_type or 'heart_rate' in parameters_object.signals_type :
                    raise Exception(
                        'You can apply Riemannian Geometry-based methods and CNN on EEG data only ! Make sure you select only EEG as signal type before to use this type of algorithm.')

                else:
                    filter = '' # No EEG filters are required for algorithms other than SVM and LDA

                    if 'fb' in classifier:
                        study.passband = parameters_object.passband_repository['filter_bank']
                    else:
                        study.passband = parameters_object.passband_repository['single']

                    self.run_single_study(study=study,
                                          evaluation_type=study.evaluation_type,
                                          filter=filter,
                                          filter_parameter=parameters_object.filter_parameter,
                                          classifier=classifier,
                                          classifier_parameter=parameters_object.classifier_parameter)

        self.score_type = study.score_type


    def run_single_study(self,
                         study='',
                         evaluation_type='',
                         filter='',
                         filter_parameter={},
                         classifier='',
                         classifier_parameter={}):
        '''
        This method is used to run a single study, meaning 1 dataset, 1 type of flilter for EEG signals, 1 type of ML algorithm, 1 type of calibration.
        :param study: name of the data set (Ex: "bci_competition_4_dataset_2a")
        :param evaluation_type: [string] 'cross_validation' vs 'classic'
        :param filter: [string] Ex: 'FBCSP'
        :param filter_parameter:
        :param classifier: [string] 'LDA'
        :param classifier_parameter:
        :return:
        '''

        # Algorithms settings
        # ==== type ====
        study.filter = filter
        study.classifier = classifier
        # ==== hyper-parameters ====
        study.filter_parameter = filter_parameter
        study.classifier_parameter = classifier_parameter


        # Printings
        print('')
        print('########################################################################################################')
        print('Dataset : ', study.dataset)
        print('Type of signals : ', study.signals_type)
        print('Calibration: ', study.calibration_type)
        print('Evaluation: ', evaluation_type)
        print('Algorithm: ', filter + ' ' + classifier)
        print('passband: ', study.passband)
        print('Statistical tests: ', study.list_statistical_tests)
        print('Plots: ', study.list_plots)

        # Run the study
        print(evaluation_type)
        run_study = 'study.run_study_' + evaluation_type + '()'
        exec(run_study)

        print('########################################################################################################')


    def run_analysis(self, parameters_object=None, score_type=None, calibration_types=[]):
        '''
        This method aims at making statistics and plotting on classification accuracy results.
        :param parameters_object:
        :param score_type:
        :param calibration_types:
        :return:
        '''

        print('We use {} as type of score'.format(score_type))

        if len(calibration_types) == 1:
            print('We have 1 types of calibration: {}'.format(calibration_types[0]))
        else:
            print('We have 2 types of calibration: {} and {}'.format(calibration_types[0], calibration_types[1]))

        analyzer = analysis_constructor()
        analyzer.seek_for_results_files(application_directory=parameters_object.application_directory,
                                        dataset_name=parameters_object.dataset,
                                        calibration_types=calibration_types,
                                        list_filters=parameters_object.list_filters,
                                        list_classifiers=parameters_object.list_classifiers,
                                        list_signal_types=parameters_object.signals_type
                                        )

        analyzer.load_results_data_into_pandas_frame(list_classifier=parameters_object.list_classifiers,
                                                     list_filter=parameters_object.list_filters,
                                                     list_signal_types=parameters_object.signals_type)
        path_figures = parameters_object.application_directory + 'data_store/results/' + parameters_object.dataset

        # Plotting
        if len(calibration_types) > 1:
            analyzer.plotting_results(plot_types=parameters_object.list_plots,
                                      dv=score_type,
                                      factor_=['algorithm', 'calibration'],
                                      results_path_folder_store=path_figures)
        else:
            analyzer.plotting_results(plot_types=parameters_object.list_plots,
                                      dv=score_type,
                                      factor_=['algorithm'],
                                      results_path_folder_store=path_figures)

        # Statistical tests
        if len(calibration_types) > 1:
            analyzer.apply_statistical_tests(test_types=parameters_object.list_statistical_tests,
                                             dv=score_type,
                                             factor_=['algorithm', 'calibration'])
        else:
            analyzer.apply_statistical_tests(test_types=parameters_object.list_statistical_tests, dv=score_type, factor_=['algorithm'])






