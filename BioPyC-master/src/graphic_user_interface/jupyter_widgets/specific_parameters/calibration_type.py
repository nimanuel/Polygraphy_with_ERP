# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the calibration type
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0



from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class calibration_type(object):

    def __init__(self):
        self.list_calibration_types = ['subject_specific', 'subject_independent']
        self.container = None

    def display_widgets(self, study_parameters_object=None,
                        evaluation_type_object=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for choosing the calibration type user will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()

        # Creating a jupyter container with a selectmultiple box allowing to display available datasets in data_store
        self.container = general_widgets_.create_selectmultiple_widget_container(value='Calibration types',
                                                                                 options=self.list_calibration_types)

        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_calibration_type_selection = general_widgets_.button()
        display(self.button_calibration_type_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_calibration_type_selection(b):

            # Getting the data types the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one data type is selected
            if len(repository_functions) == 0:
                raise Exception('Not able to update calibration parameters : please select a calibration before')

            ###########################################
            # Updating parameters for the next step
            ###########################################
            study_parameters_object.calibration_type = list(repository_functions['calibration_type'])

            self.label_confirmation.value = "You chose {} as calibration for your study".format \
                (study_parameters_object.calibration_type)

            # Updating the button of the next step
            evaluation_type_object.button_evaluation_type_selection.disabled = False
            evaluation_type_object.button_evaluation_type_selection.description = "Select this evaluation type"
            evaluation_type_object.button_evaluation_type_selection.button_style = 'info'

            # Updating button of the current step
            self.button_calibration_type_selection.disabled = True
            self.button_calibration_type_selection.description = 'Unavailable'
            self.button_calibration_type_selection.button_style = 'danger'

        self.button_calibration_type_selection.on_click(click_calibration_type_selection)