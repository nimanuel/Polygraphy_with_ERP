# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of plottings
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0

from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class stats_type(object):

    def __init__(self):
        self.list_available_plottings = []
        self.container = None

    def display_widgets(self, study_parameters_object=None):

        general_widgets_ = general_widgets()

        # Listing all available filters in src
        self.list_available_stats = ['rm_anova', 'posthoc_ttest']


        self.container = general_widgets_.create_selectmultiple_widget_container(value='Available statistical tests',
                                                                                 options=self.list_available_stats)

        # Display the containers
        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_stat_selection = general_widgets_.button()
        display(self.button_stat_selection)

        self.button_stat_selection.disabled = False
        self.button_stat_selection.description = 'Select those stats'
        self.button_stat_selection.button_style = 'info'

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_stat_selection(b):
            # Getting the dataset the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one dataset is selected
            if len(repository_functions) == 0:
                raise Exception('Please select a plotting(s) before')

            study_parameters_object.list_statistical_tests = list(repository_functions['list_stats'])

            self.label_confirmation.value = "You chose to plot the following list of statistical tests:  {} ".format(
                study_parameters_object.list_statistical_tests)

            self.button_stat_selection.disabled = True
            self.button_stat_selection.description = 'Unavailable'
            self.button_stat_selection.button_style = 'danger'

        self.button_stat_selection.on_click(click_stat_selection)