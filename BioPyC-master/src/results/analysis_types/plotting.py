# -*- coding: utf-8 -*-

"""
The class plotting allows to plot results from dat analysis
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import pandas as pd
import seaborn as sns
import scikit_posthocs as sp
import matplotlib.pyplot as plt
import numpy as np


class plotting(object):

    def __init__(self):

        # Printing title of the statistics section
        print('')
        print('')
        print('')
        print('')
        print('\033[1m' + '#############')
        print('VISUALIZATION')
        print('#############')
        print('\033[0m')

    def table_results(self, df=None, dv='', factor_=[], results_path_folder_store=''):

        print('==============')
        print('TABLE RESULTS')
        print('==============')

        if len(factor_) == 1:
            # Get mean for each values of the factor
            if len(np.unique(list(df[factor_[0]]))) == 1:
                resume_df = df[dv].mean()
            else:
                resume_df = df[[factor_[0], dv]].groupby(factor_[0]).mean()

        if len(factor_) == 2:
            if len(np.unique(list(df[factor_[0]]))) == 1:
                pass
            elif len(np.unique(list(df[factor_[1]]))) == 1:
                pass
            elif len(np.unique(list(df[factor_[0]]))) != 1 and len(np.unique(list(df[factor_[1]]))) != 1:

                print('\033[1m')
                print('Mean {} over algorithms and calibration types :'.format(dv))
                print('\033[0m')
                resume_df = df.pivot_table(index=factor_[0], columns=factor_[1],values=dv, aggfunc='mean')

        # printing the pandas frame containing the results
        print('')
        print(resume_df)
        print('')


    def boxplot(self, df=None, dv='', factor_=[], results_path_folder_store=''):

        # Calculate min_perf for defining size of the graph
        min_perf = min(df[dv]) - 20
        sns.set(style="whitegrid")
        if len(factor_) == 1:
            #sns.set(font_scale=1)
            ax = sns.boxplot(x=factor_[0],
                             y=dv,
                             data=df,
                             width=.8)
            ax.set(ylim=(min_perf, 100))

        elif len(factor_) == 2:
            ax = sns.boxplot(x=factor_[0],
                             y=dv,
                             hue=factor_[1],
                             data=df,
                             width=.8)
            ax.set(ylim=(min_perf, 100))
        else:
            print('There is no way to plot a boxplot with more than 2 factors')

        # printing the boxplot
        print('========')
        print('BOXPLOT')
        print('========')
        print('')
        fig = ax.get_figure()
        plt.show()
        print('')

        fig.savefig(results_path_folder_store + "/figures/boxplot.png", format='png', dpi=800)

    def barplot(self, df=None, dv='', factor_=[], results_path_folder_store=''):

        # printing the barplot
        print('========')
        print('BARPLOT')
        print('========')
        print('')
        sns.set(style="whitegrid")
        if len(factor_) == 1:
            # ###############################################
            # Forcing
            # ###############################################
            #list_subj = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] + [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27] + [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
            #list_subj_str= [str(elmt) for elmt in list_subj]
            #df['subject'] = list_subj_str

            # ###############################################
            new_list_subj = []
            nb_different_sub = len(np.unique(list(df['subject'])))
            nb_algo = len(list(df['subject']))/nb_different_sub
            nb_algo = int(nb_algo)
            for i in range(nb_algo):

                for j in range(nb_different_sub):
                    new_list_subj.append(str(j+1))

            df['subject'] = pd.Series(new_list_subj)


            #sns.set(font_scale=1)
            if len(list(df['algorithm'])) > 1:
                #sns.set(style="whitegrid")
                ax = sns.catplot(x='subject', y=dv, data=df, hue="algorithm", kind='bar', height=2.5, aspect=4)
                ax.set_xlabels('subjects', fontsize=15)
                ax.set_xticklabels(df['subject'])
                ax.set_ylabels('scores (%)', fontsize=15)
            else:
                pass
                # ax = sns.catplot(x='subject', y=dv, data=df, capsize=.2)


            #ax.set_xlabels('subject', fontsize=15)
            #ax.set_xticklabels(df['subject'], rotation=30)
            #ax.set_ylabels('score (%)', fontsize=15)

        elif len(factor_) == 2:
            if 'subject_specific' in list(df['calibration'].unique()) and 'subject_independent' in list(
                    df['calibration'].unique()):
                df_cal_0 = df[df['calibration'] == 'subject_specific']
                df_cal_1 = df[df['calibration'] == 'subject_independent']

                #sns.set(font_scale=1)

                if len(list(df['algorithm'])) > 1:
                    sns.set(style="whitegrid")
                    ax = sns.catplot(x='subject', y=dv, data=df, col_wrap=1, hue="algorithm", col='calibration', kind ='bar', height=2.5, aspect=4)
                    ax.set_xlabels('subjects', fontsize=15)
                    #ax.set_xticklabels(df['subject'], rotation=30)
                    ax.set_ylabels('scores (%)', fontsize=15)
                else:
                    pass
                    #ax = sns.catplot(x='subject', y=dv, data=df, capsize=.2)
            else:
                raise Exception('One of your factor should be the calibration, and contain "subject_specific" and "subject_independent" values')

        else:
            print('There is no way to plot a boxplot with more than 2 factors')


        #fig = ax.get_figure()
        fig=ax
        plt.show()


        fig.savefig(results_path_folder_store + "/figures/barplot.png", format='png', dpi=800)

    def ttest_heatmap(self, df=None, dv='', factor_=[], results_path_folder_store=''):

        # printing the heatmap
        print('==============')
        print('TTEST HEATMAP')
        print('==============')
        print('')

        if len(list(df[factor_[0]].unique())) > 1:
            if len(factor_) == 1:
                pc = sp.posthoc_ttest(df, val_col=dv, group_col=factor_[0], p_adjust='fdr_bh')
                heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True,
                                'cbar_ax_bbox': [0.80, 0.35, 0.04, 0.3]}

                ax = sp.sign_plot(pc, **heatmap_args)[0].set_xlabel(list(df['calibration'].unique())[0], fontsize=15)

                fig = ax.get_figure()
                plt.show()
                fig.savefig(results_path_folder_store + "/figures/ttest.png", format='png', dpi=800)

            elif len(factor_) == 2:

                if 'subject_specific' in list(df['calibration'].unique()) and 'subject_independent' in list(df['calibration'].unique()):
                    df_cal_0 = df[df['calibration'] == 'subject_specific']
                    df_cal_1 = df[df['calibration'] == 'subject_independent']

                    heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True,
                                    'cbar_ax_bbox': [0.80, 0.35, 0.04, 0.3]}

                    pc_0 = sp.posthoc_ttest(df_cal_0, val_col=dv, group_col=factor_[0], p_adjust='fdr_bh')
                    ax_0 = sp.sign_plot(pc_0, **heatmap_args)[0].set_xlabel('subject_specific', fontsize=15)
                    fig = ax_0.get_figure()
                    plt.show()
                    print('')
                    fig.savefig(results_path_folder_store + "/figures/ttest_subject_specific.png", format='png')

                    pc_1 = sp.posthoc_ttest(df_cal_1, val_col=dv, group_col=factor_[0], p_adjust='fdr_bh')
                    ax_1 = sp.sign_plot(pc_1, **heatmap_args)[0].set_xlabel('subject_independent', fontsize=15)

                    fig = ax_1.get_figure()
                    plt.show()
                    print('')
                    fig.savefig(results_path_folder_store + "/figures/ttest_subject_independent.png", format='png')

                else:
                    raise Exception('One of your factor should be the calibration, and contain "subject_specific" and "subject_independent" values')
            else:
                raise Exception('So far BioPyC can deal with 1 or 2 factors only.')
        else:
            raise Exception('You need at least 2 different values for the feature "{}", here there is only {}, i.e. {}'.format(factor_[0], len(list(df[factor_[0]].unique())),list(df[factor_[0]].unique())))


