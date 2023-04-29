# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the data type
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0



from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets
import os

class data_type(object):

    def __init__(self):
        # Listing all data types supported by BioPyC
        self.list_data_types = ['raw data', 'preprocessed data']

        self.list_available_datasets = []
        self.container = None

    def display_widgets(self, study_parameters_object=None, dataset_object=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for chosing data type user will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()

        # Creating a jupyter container with a selectmultiple box allowing to display available datasets in data_store
        self.container = general_widgets_.create_selectmultiple_widget_container(value='Data types',
                                                                                options=self.list_data_types)

        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_data_type_selection = general_widgets_.button()
        display(self.button_data_type_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_data_type_selection(b):

            # Getting the data types the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one data type is selected
            if len(repository_functions) == 0:
                raise Exception('Not able to build the dataset : please select a dataset before')

            # Check there is no more than 1 data type selected
            elif len(repository_functions['data_type']) != 1:
                raise Exception('This application can deal with 1 dataset only so far !')


            ###########################################
            # Updating parameters for the next step
            ###########################################
            # self.data_type = repository_functions['data_type'][0]
            study_parameters_object.data_type = self.data_type = repository_functions['data_type'][0]

            self.label_confirmation.value = "You chose to work on {}, you will therefore have to choose a dataset that is stored in the {} BioPyC's data store.".format \
                (self.data_type, self.data_type)

            # Listing all available datasets in user's data_store
            if study_parameters_object.data_type == 'preprocessed data': # If preprocessed, the user just have to pick a data set in the data store for preprocessed data
                self.list_available_datasets = [f for f in os.listdir
                    (study_parameters_object.application_directory + 'data_store/preprocessed_datasets') if
                                                os.path.isdir(os.path.join
                                                    (study_parameters_object.application_directory +'data_store/preprocessed_datasets',
                                                    f))]

            elif study_parameters_object.data_type == 'raw data':  # If raw data,
                self.list_available_datasets = [f for f in os.listdir(
                    study_parameters_object.application_directory + 'data_store/rawdata_datasets')
                                                if
                                                os.path.isdir(
                                                    os.path.join(
                                                        study_parameters_object.application_directory + 'data_store/rawdata_datasets',
                                                        f))]



            dataset_object.container.children[0].children[1].options = self.list_available_datasets
            dataset_object.button_dataset_selection.disabled = False
            dataset_object.button_dataset_selection.button_style = 'info'
            dataset_object.button_dataset_selection.description = 'Select this dataset'

            self.button_data_type_selection.disabled = True
            self.button_data_type_selection.description = 'Unavailable'
            self.button_data_type_selection.button_style = 'danger'

        self.button_data_type_selection.on_click(click_data_type_selection)