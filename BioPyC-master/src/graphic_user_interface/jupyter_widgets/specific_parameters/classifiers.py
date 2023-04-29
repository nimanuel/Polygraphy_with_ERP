# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the classifier
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets
import os

class classifiers(object):

    def __init__(self):
        self.list_available_classifiers = []
        self.container = None

    def display_widgets(self, study_parameters_object=None, calibration_type_object=None):

        general_widgets_ = general_widgets()

        # Listing all available classifiers in src
        self.list_available_classifiers = [f for f in os.listdir(study_parameters_object.application_directory + 'src/classifiers/') if
                                       os.path.isfile(
                                           os.path.join(study_parameters_object.application_directory + 'src/classifiers/', f))]

        self.list_available_classifiers = [filter_[:-3] for filter_ in self.list_available_classifiers]

        self.container = general_widgets_.create_selectmultiple_widget_container(value='Available classifiers',
                                                                                 options=self.list_available_classifiers)

        self.container_2 = general_widgets_.create_textbox_widget_container(value='Filter Bank Riemmanian Methods number features to keep',
                                                                                 options='4')

        self.container_3 = general_widgets_.create_textbox_widget_container(value='Single pass-band',
                                                                            options='[[8,12]]')

        self.container_4 = general_widgets_.create_textbox_widget_container(value='Filter Bank pass-bands',
                                                                            options='[[4,8],[8,12],[12,16],[16,20],[20,24],[24,28],[28,32],[32,36],[36,40]]')

        # Display the containers
        widgets.interactive(self.container)
        display(self.container)

        widgets.interactive(self.container_2)
        display(self.container_2)

        widgets.interactive(self.container_3)
        display(self.container_3)

        widgets.interactive(self.container_4)
        display(self.container_4)

        # Creating the jupyter button widget
        self.button_classifier_selection = general_widgets_.button()
        display(self.button_classifier_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_classifier_selection(b):
            # Getting the dataset the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)
            repository_functions_2 = general_widgets_.get_functions_values(self.container_2)
            repository_functions_3 = general_widgets_.get_functions_values(self.container_3)
            repository_functions_4 = general_widgets_.get_functions_values(self.container_4)


            # Check if at least one dataset is selected
            if len(repository_functions) == 0:
                raise Exception('Please select a filter(s) before')

            study_parameters_object.list_classifiers = [repository_functions['list_classifiers'][i] for i in
                                             range(len(repository_functions['list_classifiers']))]

            classifier_parameter = {}
            classifier_parameter['nb_features_to_keep'] = int(repository_functions_2['nb_features_to_keep'])
            study_parameters_object.classifier_parameter = classifier_parameter

            study_parameters_object.passband_repository['single'] = eval(repository_functions_3['single_passband'])

            study_parameters_object.passband_repository['filter_bank'] = eval(repository_functions_4['filter_bank_passbands'])


            self.label_confirmation.value = "You chose to work on the {} classifier(s) with the following parameters:\r {}".format(
                study_parameters_object.list_classifiers, study_parameters_object.classifier_parameter)

            # Updating the button of the next step
            calibration_type_object.button_calibration_type_selection.disabled = False
            calibration_type_object.button_calibration_type_selection.description = "Select this calibration type"
            calibration_type_object.button_calibration_type_selection.button_style = 'info'

            # Updating button of the current step
            self.button_classifier_selection.disabled = True
            self.button_classifier_selection.description = 'Unavailable'
            self.button_classifier_selection.button_style = 'danger'


        self.button_classifier_selection.on_click(click_classifier_selection)