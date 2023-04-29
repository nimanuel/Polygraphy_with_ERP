# -*- coding: utf-8 -*-

"""
The class dataset_constructor allows to seek for files, load and organize the data
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import os
from collections import OrderedDict, Counter
import numpy as np

class dataset_constructor(object):
    """

    """

    def __init__(self, application_directory, dataset_name, data_type):

        self.data_type = data_type # raw or preprocessed data
        self.application_directory = application_directory
        self.dataset_name = dataset_name
        self.dataset_directory = ''
        self.subjects_list = [] # List of subjects the method found in the dataset
        self.repository_subjects_files = OrderedDict() # dictionary - subject as key, list of subjects files as value
        self.format = ''  # format of files you will be using : it can be .mat, .gdf, .pkl, etc
        self.list_subjects_to_keep = []

        self.pass_bands = None
        self.pass_band_type = None

        self.repository_passbanded_filename = None
        self.repository_multipassbanded_filename = None
        self.tokens = None
        self.special_reading = None

        self.split_ratio = None  # if cross validation
        self.study_type = None  # could be normal, cross-validation, cross-subject
        self.algorithm_type = None


    def seek_for_subjects_files(self):
        """
        This method allows to check existing data and extract paths to each subject's files
        """

        # Define the path following if those are preprocessed data or not
        if self.data_type == 'preprocessed data':
            self.dataset_directory = self.application_directory + 'data_store/preprocessed_datasets/' + self.dataset_name + '/'  # Location in the data store
        elif self.data_type == 'raw data':
            self.dataset_directory = self.application_directory + 'data_store/rawdata_datasets/' + self.dataset_name + '/'  # Location in the data store
        else:
            raise Exception('Weird, this error should never happen')

        # Looking for dataset subfolders corresponding to each subjects
        if self.list_subjects_to_keep == []:
            try:
                self.subjects_list = [f for f in os.listdir(self.dataset_directory) if
                                      os.path.isdir(os.path.join(self.dataset_directory, f))]
            except ValueError:
                print('Your folder / dataset is empty !')
        else:
            self.subjects_list = self.list_subjects_to_keep

        # Sorting the list of subjects
        self.subjects_list = self.sort_subjects_list(self.subjects_list)
        self.list_subjects_to_keep = self.subjects_list

        try:
            for subject in self.subjects_list:
                self.repository_subjects_files[subject] = [f for f in os.listdir(self.dataset_directory + subject + '/') if
                                                   os.path.isfile(os.path.join(self.dataset_directory + subject + '/', f))]
        except ValueError:
            print('Your subfolders corresponding to subjects data are empty !')


    def seek_for_files_format(self) :

        print('Since you did not specify the file format, we are seeking for it...')

        # Looking for formats ".xxx" of each subjects' files
        format_list, number_files = [], []
        for files_list in self.repository_subjects_files.values():
            number_files_list = len(files_list)
            for file in files_list:
                if file[-4] == '.': # Looking for format ".xxx"
                    format_list.append(file[-4:])
                elif file[-7] == '.': # exception for .pickle
                    format_list.append(file[-7:])

        dictionay_format = Counter(format_list)

        # Display information about the dataset to the user
        print('We found your dataset, it coutains ' + str(
            len(self.subjects_list)) + ' sub-folders, corresponding to your '+ str(
            len(self.subjects_list)) + ' subjects. Moreover, each of these subfolders countains ' +
              str(int(np.mean(number_files_list))) + ' files. The distribution of these files formats is as follow : \n')

        # Display information about the dataset to the user
        cpt_key = 0
        for key, value in dictionay_format.items():
            cpt_key += 1
            if cpt_key == len(dictionay_format):
                print(key + '  :  ' + str(value) + ' files\n\n')
            else:
                print(key + '  :  ' + str(value) + ' files')

        # Display information about the dataset type to the user
        if cpt_key == 1:
            self.format = key
            print('Since ' + self.format + ' is the only format, the application saves it as the default format you will use')
        else:
            max_number_files = max(list(dictionay_format.values()))
            if list(dictionay_format.values()).count(max_number_files) > 1:
                if ".gdf" in dictionay_format.keys():
                    self.format = ".gdf"
                elif ".mat" in dictionay_format.keys():
                    self.format = ".mat"
            else:
                self.format = list(dictionay_format.keys())[list(dictionay_format.values()).index(max(list(dictionay_format.values())))]
            print('Since ' + self.format + ' has the major number of files in subjects sub-folders, the application saves it as the default format you will use')

    def sort_subjects_list(self, subjects_list):
        """
        This method allows to sort list of subjects
        :param subjects_list: list of the different subjects ['subject_3', 'subject_1', 'subject_2']
        :return: sorted list of the different subjects ['subject_1', 'subject_2', 'subject_3']
        """
        ID_list = []
        for elmt in subjects_list:
            ID_list.append(int(elmt.split('_')[1]))
        ID_list.sort()

        new_list = []
        for ID in ID_list:
            new_list.append('subject_' + str(ID))

        return new_list

