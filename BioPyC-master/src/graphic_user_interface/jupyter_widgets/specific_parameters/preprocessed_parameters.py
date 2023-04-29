# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the preprocessed parameters
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0




from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class preprocessed_parameters(object):

    def __init__(self):
        self.preprocessed_parameters = ''
        self.container = None

    def display_widgets(self, study_parameters_object=None,
                        classifiers_object=None,
                        filters_object=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for choosing preprocessed parameters user will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()

        # Creating a jupyter container with a selectmultiple box
        self.container = general_widgets_.create_textbox_widget_container(value='Band-pass delimiters',
                                                         options="['_','to', 'Hz']")

        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_preprocessed_parameters_selection = general_widgets_.button()
        display(self.button_preprocessed_parameters_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_preprocessed_parameters_selection(b):
            # Getting the data types the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one data type is selected
            if len(repository_functions) == 0:
                raise Exception('Not able to update band-pass delimiters: please input band-pass delimiters')

            ###########################################
            # Updating parameters for the next step
            ###########################################
            study_parameters_object.passband_delimiters = repository_functions['bandpass_delimiters']

            self.label_confirmation.value = "You chose {} as band-pass delimiters for your study".format(
                study_parameters_object.passband_delimiters)

            # Updating the button of the next step
            filters_object.button_filter_selection.disabled = False
            filters_object.button_filter_selection.description = "Select this (list of) filter(s)"
            filters_object.button_filter_selection.button_style = 'info'

            classifiers_object.button_classifier_selection.disabled = False
            classifiers_object.button_classifier_selection.description = "Select this (list of) classifier(s)"
            classifiers_object.button_classifier_selection.button_style = 'info'

            # Updating button of the current step
            self.button_preprocessed_parameters_selection.disabled = True
            self.button_preprocessed_parameters_selection.description = 'Unavailable'
            self.button_preprocessed_parameters_selection.button_style = 'danger'

        self.button_preprocessed_parameters_selection.on_click(click_preprocessed_parameters_selection)