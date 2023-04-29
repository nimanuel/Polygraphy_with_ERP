# -*- coding: utf-8 -*-

"""
The class results_constructor allows to organize the ML algorithms predictions, calculate accuracies and finally store the results
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from collections import Counter, OrderedDict
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from src.results import analysis_constructor

class results_constructor(object):
    """
    The class results_constructor allows to organize the ML algorithms predictions, calculate accuracies and finally store the results.
    """

    def __init__(self):

        # General
        self.list_subjects = []
        self.frame_results = pd.DataFrame({})

        # Selected passbands
        self.held_selected_passbands = []
        self.held_subjects = []
        self.frame_selected_passbands = pd.DataFrame({})

        # Classifier feedbacks
        self.array_y_pred = []
        self.array_y_true = []
        self.vector_size_train = []
        self.vector_size_test = []

        # Scoring
        self.score_type = '' # 'accuracy' or 'f1-score'
        self.all_subj_perfomance_scores = []

    def hold_selected_passband_subject(self, selected_passbands=None):
        self.held_selected_passbands.extend(list(selected_passbands.astype(int)))

    def generate_repository_selected_passbands(self, list_passbands=[]):

        repo_all_passbands = OrderedDict()
        repo_counter = Counter(self.held_selected_passbands)
        total_selected = np.sum(list(repo_counter.values()))
        for i in range(len(list_passbands)):

            if i in repo_counter.keys():
                repo_all_passbands[str(list_passbands[i])] = [repo_counter[i], repo_counter[i]/total_selected] # the 2nd is the ratio
            else:
                repo_all_passbands[str(list_passbands[i])] = [0, 0.0] # the 2nd is the ratio

        self.frame_selected_passbands = pd.DataFrame(repo_all_passbands, index=[0, 1]).T.rename(columns={0:"number of uses",
                                                                                                         1:"percentage of uses"})
        self.frame_selected_passbands.insert(0, 'passbands', self.frame_selected_passbands.index)
        self.frame_selected_passbands.reset_index(drop=True, inplace=True)
        self.frame_selected_passbands["number of uses"] = self.frame_selected_passbands["number of uses"].astype(int)
        self.frame_selected_passbands["percentage of uses"] = self.frame_selected_passbands["percentage of uses"]*100
        self.frame_selected_passbands["percentage of uses"] = self.frame_selected_passbands["percentage of uses"].astype(int)

    def hold_classification_prediction_vector_subject(self, subject='', y_pred=[], y_true=[], size_train=0, size_test=0):
        """
        Store classifier predictions, real values of the test set and results into vectors for each subject
        :param classifier: object of the used classifier, containing y_true, y_pred and accuracy score
        :return:
        """
        self.list_subjects.append(subject)

        self.array_y_pred.append(y_pred)
        self.array_y_true.append(y_true)

        # self.vector_score.append(classifier.accuracy_score)
        self.vector_size_train.append(size_train)
        self.vector_size_test.append(size_test)

    def generate_performance_scores(self):

        # Start with the principle that all test sets are balanced
        balanced_classes = True
        self.score_type = 'accuracy'

        self.array_y_pred = np.array(self.array_y_pred)
        self.array_y_true = np.array(self.array_y_true)

        for i in range(len(self.array_y_pred)):

            # Check if classes are almost balanced
            count_elmt_y_true = Counter(self.array_y_true[i])
            theorical_nb_trial_per_class = self.vector_size_test[i]/len(list(count_elmt_y_true.keys()))

            for class_nb_elmt in count_elmt_y_true.values():
                # Calcul ratio
                ratio_ = class_nb_elmt/theorical_nb_trial_per_class
                if ratio_ < 0.90 or ratio_ > 1.10:

                    balanced_classes = False
                    self.score_type = 'f1-score'


        for i in range(len(self.array_y_pred)):

            # ==== Balanced classes : accuracy score ====
            if balanced_classes == True:
                score_subj = accuracy_score(self.array_y_true[i], self.array_y_pred[i], normalize=True)

            # ==== Unbalanced classes : f1 score ====
            else:
                score_subj = f1_score(self.array_y_true[i], self.array_y_pred[i], average='weighted')
                #score_subj = f1_score(self.array_y_true[i], self.array_y_pred[i])

            self.all_subj_perfomance_scores.append(score_subj)

        self.score_type = 'score'

    def build_frame_results(self, filter='', classifier='', calibration_type='', list_signal_types=[]):
        '''
        Create a pandas dataframe to store the results : rows are subjects' IDs; columns are accuracy_score, y_pred, y_true
        :return: a pandas dataframe [nb_subjects * (3 + 2*max_trials_test)]
        '''

        # Create a vector of data for each subject
        max_trials_test = max(self.vector_size_test)
        for i in range(len(self.list_subjects)):
            nb_trials_test = self.vector_size_test[i]
            diff_subj_max_trials_test = max_trials_test - nb_trials_test

            # Create a vector for each subject, containing main information + y_pred + y_true concatenate in a line
            # (completed with nans since all subejcts do not have the same number of trials in the test set)
            vector_subject = np.array([[self.list_subjects[i]] + [self.all_subj_perfomance_scores[i]] +
                                       [self.vector_size_train[i]] + [self.vector_size_test[i]] + list(
                self.array_y_pred[i]) +
                                       list(self.array_y_true[i]) + [np.nan for i in
                                                                     range(diff_subj_max_trials_test * 2)]])
            if i == 0:
                list_vector_subject = vector_subject
            else:
                list_vector_subject = np.concatenate([vector_subject, list_vector_subject], axis=0)

        self.frame_results = pd.DataFrame(list_vector_subject)
        self.frame_results = self.frame_results[::-1]
        self.frame_results = self.frame_results.rename(columns={0: 'subject',
                                                      1: self.score_type,
                                                      2: 'train set size',
                                                      3: 'test set size'})

        '''
        # Add a new column in first position with the name of the algorithm
        if filter != '':
            algo = filter + '_' + classifier
        else:
            algo = classifier
        '''
        # Add a new column in first position with the name of the algorithm
        if classifier == 'lda' or classifier == 'svm':

            algo = ''

            if 'heart_rate' in list_signal_types or 'breathing' in list_signal_types or 'eda' in list_signal_types:

                for signal in list_signal_types:

                    if signal != 'EEG':
                        if algo == '':
                            algo = signal
                        else:
                            algo = algo + '_' + signal

                if 'EEG' in list_signal_types :

                    if algo == '':
                        algo = filter
                    else:
                        algo = algo + '_' + filter

                algo = algo + '_' + classifier

            elif 'EEG' in list_signal_types:
                algo = filter + '_' + classifier

        else:
            algo = classifier

        print('')
        print(list_signal_types)
        print(filter)
        print('algorithms before saving')
        print(algo)
        print('')

        self.frame_results.insert(loc=1, column='algorithm', value=[algo for i in range(len(self.frame_results))])
        self.frame_results.insert(loc=1, column='calibration', value=[calibration_type for i in range(len(self.frame_results))])

        # Convert string type scores to float
        self.frame_results[self.score_type] = self.frame_results[self.score_type].astype(float)

        # Score from 0-1 format to 0-100
        self.frame_results[self.score_type] = self.frame_results[self.score_type]*100


    def display_and_store_statistics(self, list_plots=[], list_statistical_tests=[], results_path_folder_store=''):

        # Build a analyzer object, containg all methods allowing to make many analysis
        self.analyzer = analysis_constructor.analysis_constructor()

        # Feed the analyzer with the dataframe containing all results from
        self.analyzer.set_results_pandas_frame(df=self.frame_results)

        # Display plots
        self.analyzer.plotting_results(plot_types=list_plots, dv=self.score_type, factor_=['algorithm'], results_path_folder_store=results_path_folder_store)

        # Make the different statistical tests that have been asked by the user
        self.analyzer.apply_statistical_tests(test_types=list_statistical_tests, dv=self.score_type, factor_=['algorithm'])


    def store_results(self, results_path_folder_store='', calibration_type='', filter='', signals_type='', classifier='' ):
        """
        Store the dataframe containing all results (subject IDs, accuracy/f1-score, train/test sets size, etc)
        to the path specified by the user
        :param results_filename: string containg the the path and the file name.
        Ex: /data_store/results/bci_competition_4_dataset_2a/subject_specific/csp_lda.csv
        :return: Nothing
        """

        if filter != '':
            results_filename = results_path_folder_store + calibration_type + '/' + str(signals_type) + '_' + calibration_type + '_' + filter + '_' + classifier + '.csv'
        else:
            results_filename = results_path_folder_store + calibration_type + '/' + str(signals_type) + '_' + calibration_type + '_' + classifier + '.csv'
        self.frame_results.to_csv(results_filename, index=False)

        if 'fb' in filter or 'fb' in classifier:
            if filter != '':
                selected_passbands_filename = results_path_folder_store + calibration_type + '/' + 'selected_passbands/' + filter + '_' + classifier + '.csv'
            else:
                selected_passbands_filename = results_path_folder_store + calibration_type + '/' + 'selected_passbands/' + classifier + '.csv'
            self.frame_selected_passbands.to_csv(selected_passbands_filename, index=False)