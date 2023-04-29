# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the signal type
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0



from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class signals_type(object):

    def __init__(self):
        self.list_signals_types = ['EEG', 'eda', 'breathing', 'heart_rate']
        self.container = None

    def display_widgets(self, study_parameters_object, data_type_object):
        """
        This method allows to display jupyter's label and selectmultiple boxes for chosing data type user will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()

        # Creating a jupyter container with a selectmultiple box allowing to display available datasets in data_store
        self.container = general_widgets_.create_selectmultiple_widget_container(value='Signals types',
                                                                                 options=self.list_signals_types)

        self.container.children[0].children[0].layout = widgets.Layout(width='25%', height='50px')
        self.container.children[0].children[1].layout = widgets.Layout(width='25%', height='50px')
        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_signals_type_selection = general_widgets_.button(label="Select this signals type")
        self.button_signals_type_selection.button_style = 'info'
        self.button_signals_type_selection.disabled = False
        display(self.button_signals_type_selection)

        # Creating the labels field to display users' choices
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_signals_type_selection(b):

            # Getting the data types the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one data type is selected
            if len(repository_functions) == 0 :
                raise Exception('Please select a signals type before')

            ###########################################
            # Updating parameters for the next step
            ###########################################
            study_parameters_object.signals_type = self.signals_type = repository_functions['signals_type']
            #self.signals_type = repository_functions['signals_type']
            #study_parameters_object.signals_type = repository_functions['signals_type']

            self.label_confirmation.value = "You chose to work on {} signals".format \
                (self.signals_type)

            # Updating jupyter button widget for the next step
            data_type_object.button_data_type_selection.button_style = 'info'
            data_type_object.button_data_type_selection.disabled = False
            data_type_object.button_data_type_selection.description = "Select this signals type"

            # Updating jupyter button widget for the current step
            self.button_signals_type_selection.disabled = True
            self.button_signals_type_selection.description ='Unavailable'
            self.button_signals_type_selection.button_style = 'danger'

        self.button_signals_type_selection.on_click(click_signals_type_selection)