# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the dataset
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class dataset(object):

    def __init__(self):
        self.container = None

    def display_widgets(self, study_parameters_object=None,
                        list_available_datasets=[],
                        preprocessing_parameters_object=None,
                        preprocessed_parameters_object=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for choosing the dataset user will use
        :return: Nothing returned, just displaying, and button click updates class attribute self.data_type
        """
        general_widgets_ = general_widgets()

        # Creating a jupyter container with a selectmultiple box allowing to display available datasets in data_store
        self.container = general_widgets_.create_selectmultiple_widget_container(value='Datasets',
                                                                                options=list_available_datasets)

        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_dataset_selection = general_widgets_.button()
        display(self.button_dataset_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_dataset_selection(b):

            # Getting the dataset the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Updating next step button
            if study_parameters_object.data_type == 'raw data':
                preprocessed_parameters_object.button_preprocessed_parameters_selection.button_style = 'danger'
                preprocessing_parameters_object.button_preprocessing_parameters_selection.disabled = False
                preprocessing_parameters_object.button_preprocessing_parameters_selection.button_style = 'info'
                preprocessing_parameters_object.button_preprocessing_parameters_selection.description = 'Select these pre-processing parameters'

            elif study_parameters_object.data_type == 'preprocessed data':
                preprocessing_parameters_object.button_preprocessing_parameters_selection.button_style = 'danger'
                preprocessed_parameters_object.button_preprocessed_parameters_selection.disabled = False
                preprocessed_parameters_object.button_preprocessed_parameters_selection.button_style = 'info'
                preprocessed_parameters_object.button_preprocessed_parameters_selection.description = 'Select this parameter'

            # Check if at least one dataset is selected
            if len(repository_functions) == 0:
                raise Exception('Not able to build the dataset : please select a dataset before')

            # Check there is no more than 1 dataset selected
            elif len(repository_functions['dataset']) != 1:
                raise Exception('This application can deal with 1 dataset only !')

            study_parameters_object.dataset = repository_functions['dataset'][0]

            self.label_confirmation.value = "You chose to work on the {} dataset".format(study_parameters_object.dataset)

            # Updating current step button
            self.button_dataset_selection.disabled = True
            self.button_dataset_selection.description = 'Unavailable'
            self.button_dataset_selection.button_style = 'danger'

        self.button_dataset_selection.on_click(click_dataset_selection)