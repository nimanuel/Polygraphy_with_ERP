# -*- coding: utf-8 -*-

"""
The class specific_studies_parameters allows to store paramters for specific studies
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License



class specific_studies_parameters(object):

    def __init__(self):
        """
        Set the different parameters for runnning a sutdy in a shortcut way (See bottom of the gui.py file)
        Each method represents a dataset, and each attributes the parameters for the study the chosen dataset
        """
        # Application directory
        self.application_directory = ''

        # Study type
        self.calibration_type = '' # 'subject_specific' or 'subject_independent'

        # Dataset
        # === global parameters ===
        self.dataset_format = ''  # the format of the dataset, i.e. .mat, .gdf etc
        self.signals_type = [] # ['EEG', 'heart_rate', 'EDA', 'breathing']
        self.data_type = ''  # 'raw' or 'preprocessed'
        self.dataset = '' # (Ex: 'bci_competition_4_dataset_2a')
        #self.passband = [] # set of aassbands data should be filtered into
        self.passband_repository = {} # set of aassbands data should be filtered into
        self.training_split_ratio = 0.0 # split ratio for the training set (Ex: 0.8 for keeping 80% of the data for the training set)
        self.type_split = '' # 'chronological' or 'shuffle'
        self.cross_val_type = '' #'k-fold' or 'leave_one-out'
        self.kfold = 0 # number of k kold for the cross validation

        # === preprocessed data === (no list of runs/session, should have been concatenated during the preprocessing)
        self.passband_delimiters = [] # string characters that delimit limit figures of the bandpass

        # === raw data === (meaning those are parameters for the preprocessing)
        self.specify_labeling = None  # Meaning you have to implement a script to labelize your data
        self.list_subjects_to_keep = [] # list containing strings of the subjects (Ex: ['subject_1', 'subject_2'])
        self.list_sessions = [] # list containing integers of the sessions (Ex: [1,2])
        self.list_runs = [] # list containing integers of the runs (Ex: [1,2,3,4])
        self.dictionary_stimulations = {} # (Ex: {'right':1, 'left':2})
        self.tmin = {} # repo with name of the sensor : start time window signal, can before/after the stimulation (Ex: 2.5 for 2,5 sec after stimulation)
        self.tmax = {} # repo with name of the sensor : stop time window signal, can before/after the stimulation (Ex: -1.0 for 1 sec before the stimulation)
        self.list_all_channels = [] # list of channels ['channel_1', 'channels_2', etc]
        self.list_channels_EEG = [] # List of channels ['FP1', AFz', etc]
        self.channel_breathing = '' # name of the channel used for breathing, ex 'channel 65'
        self.channel_eda = '' # name of the channel used for eda, ex 'channel 67'
        self.channel_heart_rate = '' # name of the channel used for heart rate, ex 'channel 68'
        self.list_eog = [] # list EOGs ['eog_1', 'eog_2', etc]
        self.list_channels_to_drop = [] # list of channels ['unnamed_1', 'unnamed_2', etc]

        # Algorithm
        # ==== type ====
        self.list_filters = []
        self.list_classifiers = []
        # ==== hyper-parameters ====
        self.filter_parameter = {}
        self.classifier_parameter = {}

        # Results
        # ==== Evaluation ====
        self.evaluation_type = ''  # 'classic' or 'cross_validation'
        # ==== Analysis to make ====
        self.list_statistical_tests = []
        self.list_plots = []
        # ==== Saving path for results dataframe ====
        self.results_filename = ''


    def bci_competition_4_dataset_2a(self):
        """
        This method updates the parameters for the BCI competition 4 dataset 2 study, a raw dataset
        :return: Nothing
        """

        # Details study
        self.calibration_type = ['subject_specific', 'subject_independent']
        self.evaluation_type = 'classic'
        self.data_type = 'raw data'
        self.dataset = 'bci_competition_4_dataset_2a'
        self.dataset_format = '.gdf'

        # Files parameters
        self.list_sessions = [1] # the toolbox will seek for "S1" in the file names
        self.list_runs = [1, 2] # the toolbox will seek for "R1" and "R2" in the file names
        self.list_subjects_to_keep = []

        # Preprocessing MNE
        self.specify_labeling = True
        self.tmin = 2.5 # After the fixation cross, 0r 0.5s after the cue instructing the movement to perform. paper from Lotte 2012
        self.tmax = 4.5
        self.list_eog = ['EOG-left', 'EOG-central', 'EOG-right']
        self.list_channels_to_drop = ['STI 014']

        # Algorithms type
        self.filter = 'csp'
        #self.filter = ''
        self.classifier = 'riemann_fbtsc'
        self.classifier = 'lda'

        self.list_filters = ['csp', 'fbcsp']
        #self.list_classifiers = ['lda', 'riemann_tsc', 'riemann_fgmdm', 'riemann_fbtsc', 'riemann_fbfgmdm']
        self.list_classifiers = ['lda']

        # Define passbands :
        if 'fb' in self.filter or 'fb' in self.classifier:
            self.passband = [[4, 8], [8, 12], [12, 16], [16, 20], [20, 24], [24, 28], [28, 32], [32, 36], [36, 40]]
        else:
            self.passband = [[8, 12]]

        self.passband_repository['filter_bank'] = [[4, 8], [8, 12], [12, 16], [16, 20], [20, 24], [24, 28], [28, 32], [32, 36], [36, 40]]
        self.passband_repository['single'] = [[8, 12]]

        # Define filter parameters

        self.filter_parameter['csp_lda_nb_filter_pairs'] = 3
        self.filter_parameter['fbcsp_lda_nb_filter_pairs'] = 2
        self.filter_parameter['nb_features_to_keep'] = 4


        self.classifier_parameter['nb_features_to_keep'] = 4


        # Splits into train / test sets
        self.training_split_ratio = 0.5
        self.type_split = 'chronological'

        # Results
        # ==== Analysis to make ====
        self.list_statistical_tests = ['rm_anova', 'posthoc_ttest']
        self.list_plots = ['table_results', 'boxplot', 'ttest_heatmap']

        # ==== Saving path for results dataframe ====
        self.results_filename = self.application_directory + 'data_store/results/' + self.dataset + '/'


    def workload(self):
        '''
        This method updates the parameters for the Workload study, a preprocessed dataset
        :return: Nothing
        '''

        # Details study
        self.calibration_type = 'subject_specific'
        self.evaluation_type = ''
        self.data_type = 'preprocessed data'
        self.dataset = 'workload'
        self.dataset_format = '.mat'

        self.list_subjects_to_keep = []

        # Algorithms type
        self.filter = 'csp'
        self.filter = ''
        self.classifier = 'lda'
        self.classifier = 'riemann_fbtsc'

        # Preprocessed datasets parameters
        self.passband_delimiters = ["_", "to", "Hz"]

        # Define passbands :
        if 'fb' in self.filter or 'fb' in self.classifier:
            self.passband = [[4, 8], [8, 12], [12, 16], [16, 20], [20, 24], [24, 28], [28, 32], [32, 36],
                             [36, 40]]
        else:
            self.passband = [[8, 12]]

        # Define filter parameters
        if self.filter == 'csp':
            self.filter_parameter['csp_lda_nb_filter_pairs'] = 3
        elif self.filter == 'fbcsp':
            self.filter_parameter['fbcsp_lda_nb_filter_pairs'] = 2

        if 'fb' in self.classifier:
            self.classifier_parameter['nb_features_to_keep'] = 4


        self.training_split_ratio = 0.5
        self.type_split = 'chronological'

        print('Calibration: ', self.calibration_type)
        print('Algorithm: ', self.filter + ' ' + self.classifier)
        print('passband: ', self.passband)

        # Results
        #self.plot = 'boxplot'
        #self.stats = 'anova'

        if self.filter != '':
            self.results_filename = self.application_directory + 'data_store/results/' + self.dataset + '/' + self.calibration_type + '/' + self.filter + '_' + self.classifier + '.csv'
        else:
            self.results_filename = self.application_directory + 'data_store/results/' + self.dataset + '/' + self.calibration_type + '/' + self.classifier + '.csv'


    def curiosity(self):
        '''
        This method updates the parameters for the Curiosity study, a raw dataset
        :return: Nothing
        '''

        # Calibration / Evaluation
        #self.calibration_type = ['subject_specific'] # Can be ['subject-specific', 'subject-independent']  or ['subject-specific'] or ['subject-independent']
        self.calibration_type = ['subject_independent']
        self.evaluation_type = 'classic' # Can be 'classic' or 'cross-validation'

        # Because this is a classic splitting:
        self.training_split_ratio = 0.5

        # Because this is a cross-validation choice :
        #self.cross_val_type = 'k-fold'
        #self.kfold = 5

        # Parameters for both cross-validation and
        self.type_split = 'chronological' # 'chronological' or 'shuffle'

        # Dataset
        # === global parameters ===
        self.dataset_format = '.gdf' # the format of the dataset, i.e. .mat, .gdf etc
        #self.signals_type = ['breathing', 'eda', 'EEG']
        self.signals_type = ['EEG']
        #self.signals_type = ['eda', 'heart_rate', 'breathing', 'EEG'] #['eda', 'heart_rate']
        #self.signals_type = ['heart_rate']
        self.data_type = 'raw data'  # 'raw' or 'preprocessed'
        self.dataset = 'curiosity'  # (Ex: 'bci_competition_4_dataset_2a')

        #self.training_ratio = 0.0  # split ratio for the training set (Ex: 0.8 for keeping 80% of the data for the training set)
        self.type_split = 'shuffle'  # 'chronological' or 'shuffle'

        # === preprocessed data === (no list of runs/session, should have been concatenated during the preprocessing)
        #self.passband_delimiters = []  # string characters that delimit limit figures of the bandpass

        # === raw data === (meaning those are parameters for the preprocessing)
        self.specify_labeling = True  # Meaning you have to implement a script to labelize your data

        #self.list_subjects_to_keep = [2,3,4,6,7,8,9,10,13,14,15,17,18,19,20,21,22,23,25,27,29,30,31,32,33,35,36]
        #self.list_subjects_to_keep = [2, 3, 4, 6, 7, 8, 9, 10, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 27, 29, 30,
        #                              31, 32, 33, 35, 36]
        self.list_subjects_to_keep = [31,33,36]

        #self.list_subjects_to_keep = [2,21,29]
        self.list_sessions = [1]  # list containing integers of the sessions (Ex: [1,2])
        self.list_runs = [1, 2, 3, 4]  # list containing integers of the runs (Ex: [1,2,3,4])
        self.dictionary_stimulations = {}  # Given by the curiosity "specific_study_labeling"

        self.tmin = {'breathing': -10.0, 'eda': -10.0, 'heart_rate': -10.0, 'EEG': -4.0}  # start time window signal, can before/after the stimulation (Ex: 2.5 for 2,5 sec after stimulation)
        self.tmax = {'breathing': 6.0, 'eda': 6.0, 'heart_rate': 6.0, 'EEG': 0.0}  # stop time window signal, can before/after the stimulation (Ex: -1.0 for 1 sec before the stimulation)

        self.list_all_channels = ['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9', 'CP5', 'CP1', 'Pz',
                                  'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'C4', 'T8', 'FT10',
                                  'FC6', 'FC2', 'F4', 'F8', 'Fp2', 'AF7', 'AF3', 'AFz', 'F1', 'F5', 'FT7', 'FC3', 'FCz',
                                  'C1', 'C5', 'TP7', 'CP3', 'P1', 'P5', 'PO7', 'PO3', 'POz', 'PO4', 'PO8', 'P6', 'P2',
                                  'CPz', 'CP4', 'TP8', 'C6', 'C2', 'FC4', 'FT8', 'F6', 'F2', 'AF4', 'AF8', 'Channel 65',
                                  'Channel 66', 'Channel 67', 'Channel 68', 'Channel 69', 'Channel 70', 'Channel 71',
                                  'Channel 72', 'STI 014']

        self.list_channels_EEG = ['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9', 'CP5', 'CP1', 'Pz',
                                  'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'C4', 'T8',
                                  'FC6', 'FC2', 'F4', 'Fp2', 'AF7', 'AF3', 'AFz', 'F1', 'F5', 'FT7', 'FC3', 'FCz',
                                  'C1', 'C5', 'TP7', 'CP3', 'P1', 'P5', 'PO7', 'PO3', 'POz', 'PO4', 'PO8', 'P6', 'P2',
                                  'CPz', 'CP4', 'TP8', 'C6', 'C2', 'FC4', 'FT8', 'F6', 'F2', 'AF4']

        #self.channel_eda = 'Channel 67'
        #self.channel_heart_rate = 'Channel 68'
        #self.channel_breathing = 'Channel 65'

        self.list_eog = ['FT10', 'F8', 'AF8']
        self.list_channels_to_drop = ['Channel 66', 'Channel 69', 'Channel 70', 'Channel 71', 'Channel 72', 'STI 014']

        # Algorithm
        # ==== type ====
        self.list_filters = ['fbcsp', 'csp']
        self.list_classifiers = ['riemann_tsc', 'riemann_fgmdm', 'lda']

        # ==== hyper-parameters ====
        self.filter_parameter = {}
        self.classifier_parameter = {}

        # Define passbands :
        self.passband_repository['filter_bank'] = [[1, 4], [4, 8], [8, 12], [12, 16], [16, 20], [20, 24], [24, 28], [28, 32],
                                                   [32, 36], [36, 40]]
        self.passband_repository['single'] = [[8, 12]]

        # Define filter parameters
        self.filter_parameter['csp_lda_nb_filter_pairs'] = 3
        self.filter_parameter['fbcsp_lda_nb_filter_pairs'] = 2
        self.filter_parameter['nb_features_to_keep'] = 6

        self.classifier_parameter['nb_features_to_keep'] = 4

        # Results
        # ==== Analysis to make ====
        self.list_statistical_tests = ['rm_anova', 'posthoc_ttest']
        self.list_plots = ['table_results', 'boxplot', 'ttest_heatmap']
        # ==== Saving path for results dataframe ====
        self.results_filename = self.application_directory + 'data_store/results/' + self.dataset + '/'


