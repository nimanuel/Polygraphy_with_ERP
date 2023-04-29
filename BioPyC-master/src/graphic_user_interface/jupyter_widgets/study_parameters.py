# -*- coding: utf-8 -*-

"""
The class mat is made for initializing study parameters
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


class study_parameters(object):

    def __init__(self):
        """
        Set the different parameters for runnning a sutdy in a shortcut way (See bottom of the gui.py file)
        Each method represents a dataset, and each attributes the parameters for the study the chosen dataset
        """
        # Application directory
        self.application_directory = ''

        # Study type
        self.calibration_type = '' # 'subject_specific' or 'subject_independent'

        # Study sub types
        self.cross_val_type = '' # 'k-fold' or 'leave-one-out'
        self.type_split = 'chronological' # 'shuffle' or 'chronological' default is chronological
        self.training_split_ratio = 0.0 # split ratio for the training set (Ex: 0.8 for keeping 80% of the data for the training set)
        self.kfold = 0


        # Dataset
        # === global parameters ===
        self.dataset_format = ''  # the format of the dataset, i.e. .mat, .gdf etc
        self.signals_type = '' # EGG physio or EEG+physio
        self.data_type = ''  # 'raw' or 'preprocessed'
        self.dataset = '' # (Ex: 'bci_competition_4_dataset_2a')
        # self.passband = [] # set of passbands data should be filtered into
        self.passband_repository = {} # set of passbands data should be filtered into

        # === preprocessed data === (no list of runs/session, should have been concatenated during the preprocessing)
        self.passband_delimiters = [] # string characters that delimit limit figures of the bandpass

        # === raw data === (meaning those are parameters for the preprocessing)
        self.specify_labeling = None  # Meaning you have to implement a script to labelize your data
        self.list_subjects_to_keep = [] # list containing strings of the subjects (Ex: ['subject_1', 'subject_2'])
        self.list_sessions = [] # list containing integers of the sessions (Ex: [1,2])
        self.list_runs = [] # list containing integers of the runs (Ex: [1,2,3,4])
        self.dictionary_stimulations = {} # (Ex: {'right':1, 'left':2})
        self.tmin = {}  # start time window signal, can before/after the stimulation (Ex: 2.5 for 2,5 sec after stimulation)
        self.tmax = {} # stop time window signal, can before/after the stimulation (Ex: -1.0 for 1 sec before the stimulation)
        self.list_all_channels = [] # list of channels ['channel_1', 'channels_2', etc]
        self.list_eog = [] # list EOGs ['eog_1', 'eog_2', etc]
        self.list_channels_to_drop = [] # list of channels ['unnamed_1', 'unnamed_2', etc]

        # Algorithm
        # ==== type ====
        self.list_filters = ''
        self.list_classifiers = ''
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