# -*- coding: utf-8 -*-
"""
This file contains both calls for the GUI and calls for the model
"""
# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

import os
from src.graphic_user_interface import gui

class application(object):

    def __init__(self):
        # Localize the toolbox on your computer
        self.application_path = str(os.path.dirname(os.path.abspath(__file__))) + '/'
        self.interface = gui.gui(self.application_path)

    def select_data_type(self):
        """
        This method calls the gui to display available rawdata dataset(s). The jupyter notebook then allows the user to select his dataset.
        Second, this dataset selection leads to the the build of a dataset object, containg many information avout the dataset.
        :return: Nothing
        """
        self.interface.display_data_types()

    def select_dataset(self):
        """
        This method calls the gui to display available dataset(s). The jupyter notebook then allows the user to select his dataset.
        Second, this dataset selection leads to the the build of a dataset object, containg many information avout the dataset.
        :return: Nothing
        """
        self.interface.display_available_datasets()

    def select_data_options(self):
        """
        This method calls the gui to display available option(s). The jupyter notebook then allows the user to select options for his study.
        :return: Nothing
        """
        self.interface.display_data_options()

    def select_filter(self):
        """
        This method calls the gui to display available filter(s). The jupyter notebook then allows the user to select a filter
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_available_filters()
        else:
            raise Exception('Please select a dataset before to apply a filter')

    def select_classifier(self):
        """
        This method calls the gui to display available classifier(s). The jupyter notebook then allows the user to select a classifier
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_available_classifiers()
        else:
            raise Exception('Please select a dataset before to apply a filter')

    def select_study_type(self):
        """
        This method calls the gui to display available study type(s). The jupyter notebook then allows the user to select a study type
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_available_study_types()
        else:
            raise Exception('Please select a dataset before to apply a study type')

    def select_passband(self):
        """
        This method calls the gui for inputing the passband(s).
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_textbox_passband()
        else:
            raise Exception('Please select a dataset before to chose a passband')

    def detect_passband_in_filenames(self):
        """
        This method calls the gui for inputing the passband(s).
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_textbox_passband_delimiter()
        else:
            raise Exception('Please select a dataset before to detect passband delimiters')

    def select_training_set_size_ratio(self):
        """
        This method calls the gui for inputing the training set size ratio.
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_textbox_training_ratio()
        else:
            raise Exception('Please select a dataset before to indicate your training set size ratio')

    def select_results_filename(self):
        """
        This method calls the gui for inputing the results filename.
        :return: Nothing
        """
        if self.interface.dataset != None:
            self.interface.display_textbox_results_filename()
        else:
            raise Exception('Please select a dataset before to indicate your training set size ratio')

    def run_study(self, studies_parameters=None, b=None, out=None):
        """
        This method calls the gui for running the study, based on parameters thanks to the methods above
        :return: Nothing
        """

        #with out:
        self.interface.run_study_voila(studies_parameters)


if __name__ == '__main__':
    application()