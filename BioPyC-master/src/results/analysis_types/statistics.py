# -*- coding: utf-8 -*-

"""
The class statistics allows to apply statistical test on data
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import pandas as pd
import pingouin as pg


class statistics(object):

    def __init__(self):

        # Printing title of the statistics section
        print('')
        print('')
        print('')
        print('')
        print('\033[1m' + '##########')
        print('STATISTICS')
        print('##########')
        print('\033[0m')

    def rm_anova(self, df=None, dv='', factor_=[]):

        # One-way rm_anova
        if len(factor_) == 1:
            aov = pg.rm_anova(dv=dv, within=factor_[0],
                              subject='subject', data=df, detailed=True)
            type_anova = 'ONE-WAY'

        # Two-way rm_anova
        elif len(factor_) == 2:
            aov = pg.rm_anova(dv=dv, within=factor_,
                              subject='subject', data=df, detailed=True)
            type_anova = 'TWO-WAYS'

        else:
            print('There is no way to run a x-ways anova in python for x>2')

        print('')
        print('================================')
        print('{} REPEATED MEASURES ANOVA'.format(type_anova))
        print('================================')
        print('')
        print(aov)
        print('')

    def posthoc_ttest(self, df=None, dv='', factor_=[]):

        print('')
        print('====================================')
        print('PAIRWISE T-TEST with FDR correction')
        print('====================================')
        print('')

        if len(factor_) == 1:
            # FDR-corrected post hocs with Hedges'g effect size
            posthoc = pg.pairwise_ttests(data=df, dv=dv, within=factor_[0], subject='subject',
                                         padjust='fdr_bh', effsize='hedges')
            # Pretty printing of table
            pg.print_table(posthoc, floatfmt='.3f')

        if len(factor_) ==2:

            if 'subject_specific' in list(df['calibration'].unique()) and 'subject_independent' in list(df['calibration'].unique()):
                df_cal_0 = df[df['calibration'] == 'subject_specific']
                df_cal_1 = df[df['calibration'] == 'subject_independent']

                print('\033[1m')
                print('SUBJECT-SPECIFIC')
                print('\033[0m')
                posthoc = pg.pairwise_ttests(data=df_cal_0, dv=dv, within=factor_[0], subject='subject',
                                             padjust='fdr_bh', effsize='hedges')
                # Pretty printing of table
                pg.print_table(posthoc, floatfmt='.3f')

                print('\033[1m')
                print('SUBJECT-INDEPENDENT')
                print('\033[0m')

                posthoc = pg.pairwise_ttests(data=df_cal_1, dv=dv, within=factor_[0], subject='subject',
                                             padjust='fdr_bh', effsize='hedges')
                # Pretty printing of table
                pg.print_table(posthoc, floatfmt='.3f')



