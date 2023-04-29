# -*- coding: utf-8 -*-

"""
The class analysis_constructor allows to organize the results data in order to analyze them
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import os
import pandas as pd
import pingouin as pg
from src.results.analysis_types import plotting, statistics

class analysis_constructor(object):
    """
    The class analysis_constructor allows to organize the results data in order to analyze them.
    There is two ways to obtain the data to analyze, first by looking at results files that have been saved,
    Second by directly getting data from the toolbox
    """
    def __init__(self):

        self.plot = ''
        self.stats = ''

        self.dictionary_files = {}
        self.results_df = pd.DataFrame({})

        self.list_algorithms = []


    def seek_for_results_files(self,
                               application_directory='',
                               dataset_name='',
                               calibration_types=[],
                               list_filters=[],
                               list_classifiers=[],
                               list_signal_types=[]):

        list_all_tested_methods = []
        for study_type in calibration_types:
            self.results_data_directory = application_directory + 'data_store/results/' + dataset_name + '/' + study_type + '/'
            #list_files = [f for f in os.listdir(self.results_data_directory) if
            #                                           os.path.isfile(os.path.join(self.results_data_directory, f)) and '.csv' in f]

            # Keep only files we use in the ongoing study
            for classifier in list_classifiers:
                if classifier == 'lda' or classifier == 'svm':
                    if 'EEG' in list_signal_types :
                        for filter in list_filters :
                            list_all_tested_methods.append(str(list_signal_types) + '_' + study_type + '_' + filter + '_' + classifier )
                            self.list_algorithms.append(filter + '_' + classifier)
                    elif 'heart_rate' in list_signal_types or 'breathing' in list_signal_types or 'eda' in list_signal_types:
                        list_all_tested_methods.append(str(list_signal_types) + '_' + study_type + '_' + classifier)
                        name_algo = ''
                        for signal in list_signal_types:
                            if signal != 'EEG' :
                                if name_algo == '':
                                    name_algo = signal
                                else:
                                    name_algo = name_algo + '_' + signal
                            if signal == 'EGG':
                                for filter in list_filters:
                                    if name_algo == '':
                                        name_algo = signal
                                    else:
                                        name_algo = name_algo + '_' + filter

                        self.list_algorithms.append(name_algo + '_' + classifier)

                else:
                    list_all_tested_methods.append(str(list_signal_types) + '_' + study_type + '_' + classifier)
                    self.list_algorithms.append(classifier)




            for elmt in list_all_tested_methods:
                key = elmt
                #self.list_algorithms.append(key)
                self.dictionary_files[key + '_' + study_type] = 'data_store/results/' + dataset_name + '/' + study_type + '/' + elmt + '.csv'


    def load_results_data_into_pandas_frame(self, list_classifier=[], list_filter=[], list_signal_types=[]):


        for key, file in self.dictionary_files.items():

            frame_ = pd.read_csv(file)


            # add a new column in first position, corresponding to the algorithm name
            self.results_df = pd.concat([self.results_df, frame_])


        # Filter the algorithms that are used for the study
        list_algorithms_to_keep_for_analysis = []



        for classifier in list_classifier:
            if classifier == 'lda' or classifier == 'svm':
                algo = ''
                if 'heart_rate' in list_signal_types or 'breathing' in list_signal_types or 'eda' in list_signal_types:

                    for signal in list_signal_types:
                        if signal != 'EEG':
                            if algo == '':
                                algo = signal
                            else:
                                algo = algo + '_' + signal

                if 'EEG' in list_signal_types:
                    algo_without_filter = algo
                    for filter in list_filter:
                        if algo == '':
                            algo = filter + '_' + classifier
                        else:
                            algo = algo_without_filter + '_' + filter + '_' + classifier
                        list_algorithms_to_keep_for_analysis.append(algo)

                else:
                    list_algorithms_to_keep_for_analysis.append(algo + '_' + classifier)



            else:
                algo = classifier
                list_algorithms_to_keep_for_analysis.append(algo)

        print('')
        print('list final algo')
        print(list_algorithms_to_keep_for_analysis)
        print('')


        '''
        if list_filter != []:
            for filter in list_filter:
                if 'lda' in list_classifier :
                    list_algorithms_to_keep_for_analysis.append(filter + '_lda')
                elif 'svm' in list_classifier:
                    list_algorithms_to_keep_for_analysis.append(filter + '_svm')
                else:
                    print('There is an issue with the filters: you need a linear classifier')

        if list_classifier != []:
            for classifier in list_classifier:
                list_algorithms_to_keep_for_analysis.append(classifier)
        '''

        self.results_df = self.results_df[self.results_df['algorithm'].isin(list_algorithms_to_keep_for_analysis)]


        # Modify name algorithms
        new_vector_algorithms = []
        for i in range(self.results_df.shape[0]):

            if self.results_df[['algorithm']].iloc[i, :].values[0] == 'riemann_tsc':
                new_vector_algorithms.append('TSC')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'riemann_fgmdm':
                new_vector_algorithms.append('FgMDM')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'riemann_fbfgmdm':
                new_vector_algorithms.append('FBFgMDM')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'riemann_fbtsc':
                new_vector_algorithms.append('FBTSC')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'fbcsp_lda':
                new_vector_algorithms.append('FBCSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'csp_lda':
                new_vector_algorithms.append('CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'lda':
                new_vector_algorithms.append('LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'svm':
                new_vector_algorithms.append('SVM')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'random_forest':
                new_vector_algorithms.append('RF')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'breathing_lda':
                new_vector_algorithms.append('Breathing+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'breathing_csp_lda':
                new_vector_algorithms.append('Breathing+CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'breathing_fbcsp_lda':
                new_vector_algorithms.append('Breathing+FBCSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'breathing_hear_rate_lda':
                new_vector_algorithms.append('Breathing+HR+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'breathing_heart_rate_csp_lda':
                new_vector_algorithms.append('Breathing+HR+CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'breathing_heart_rate_fbcsp_lda':
                new_vector_algorithms.append('Breathing+HR+FBCSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_lda':
                new_vector_algorithms.append('EDA+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_csp_lda':
                new_vector_algorithms.append('EDA+CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_fbcsp_lda':
                new_vector_algorithms.append('EDA+FBCSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_breathing_lda':
                new_vector_algorithms.append('EDA+Breathing+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_heart_rate_lda':
                new_vector_algorithms.append('EDA+HR+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_breathing_csp_lda':
                new_vector_algorithms.append('EDA+Breathing+CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_breathing_fbcsp_lda':
                new_vector_algorithms.append('EDA+Breathing+FBCSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_breathing_heart_rate_lda':
                new_vector_algorithms.append('EDA+Breathing+HR+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_breathing_heart_rate_csp_lda':
                new_vector_algorithms.append('EDA+Breathing+HR+CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'eda_breathing_heart_rate_fbcsp_lda':
                new_vector_algorithms.append('EDA+Breathing+HR+FBCSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'heart_rate_lda':
                new_vector_algorithms.append('HR+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'heart_rate_csp_lda':
                new_vector_algorithms.append('HR+CSP+LDA')
            elif self.results_df[['algorithm']].iloc[i, :].values[0] == 'heart_rate_fbcsp_lda':
                new_vector_algorithms.append('HR+FBCSP+LDA')


        self.results_df = self.results_df.drop(labels='algorithm', axis=1)

        self.results_df.insert(loc=1, column='algorithm', value=new_vector_algorithms)


    def set_results_pandas_frame(self, df=None):
        self.results_df = df

    def plotting_results(self, df=None, plot_types='', dv='', factor_=[], results_path_folder_store=''):

        if df is None:
            df = self.results_df

        # Set a plot object based on the script plotting
        if self.plot == '':
            self.plot = plotting.plotting()

        for plot_type in plot_types:

            if plot_type == 'table_results':

                self.plot.table_results(df=df, dv=dv, factor_=factor_, results_path_folder_store=results_path_folder_store)

            if plot_type == 'boxplot':

                self.plot.boxplot(df=df, dv=dv, factor_=factor_, results_path_folder_store=results_path_folder_store)

            if plot_type == 'barplot':

                self.plot.barplot(df=df, dv=dv, factor_=factor_, results_path_folder_store=results_path_folder_store)

            if plot_type == 'ttest_heatmap':

                self.plot.ttest_heatmap(df=df, dv=dv, factor_=factor_, results_path_folder_store=results_path_folder_store)

    def apply_statistical_tests(self, df=None, test_types='', dv='', factor_=[]):

        if df is None:
            df = self.results_df

        # Set the statistics object based on the script statistics
        if self.stats == '':
            self.stats = statistics.statistics()

        for test_ in test_types:

            if test_ == 'rm_anova':

                self.stats.rm_anova(df=df, dv=dv, factor_=factor_)

            if test_ == 'posthoc_ttest':

                self.stats.posthoc_ttest(df=df, dv=dv, factor_=factor_)

            elif test_ == 'nomality':
                pass


