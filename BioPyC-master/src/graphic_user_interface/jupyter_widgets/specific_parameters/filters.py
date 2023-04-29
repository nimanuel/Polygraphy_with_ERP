# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the filters
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0



from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets
import os


class filters(object):

    def __init__(self):
        self.list_available_filters = []
        self.container = None

    def display_widgets(self, study_parameters_object=None):

        general_widgets_ = general_widgets()

        # Listing all available filters in src
        self.list_available_filters = [f for f in os.listdir(study_parameters_object.application_directory + 'src/filters/') if
                                       os.path.isfile(
                                           os.path.join(study_parameters_object.application_directory + 'src/filters/', f))]

        self.list_available_filters = [filter_[:-3] for filter_ in self.list_available_filters]

        self.container = general_widgets_.create_selectmultiple_widget_container(value='Available filters',
                                                                                 options=self.list_available_filters)

        self.container_2 = general_widgets_.create_textbox_widget_container(value='CSP number of filter pairs',
                                                                                 options='3')

        self.container_3 = general_widgets_.create_textbox_widget_container(value='FBCSP number of filter pairs per band-pass',
                                                                                   options='2')

        self.container_4 = general_widgets_.create_textbox_widget_container(value='FBCSP number of features to keep',
                                                                                   options='4')


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
        self.button_filter_selection = general_widgets_.button()
        display(self.button_filter_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_filter_selection(b):
            # Getting the dataset the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)
            repository_functions_2 = general_widgets_.get_functions_values(self.container_2)
            repository_functions_3 = general_widgets_.get_functions_values(self.container_3)
            repository_functions_4 = general_widgets_.get_functions_values(self.container_4)

            # Check if at least one dataset is selected
            if len(repository_functions) == 0:
                raise Exception('Please select a filter(s) before')

            study_parameters_object.list_filters = [repository_functions['list_filters'][i] for i in
                                             range(len(repository_functions['list_filters']))]

            filter_parameter = {}
            filter_parameter['csp_lda_nb_filter_pairs'] = int(repository_functions_2['csp_lda_nb_filter_pairs'])
            filter_parameter['fbcsp_lda_nb_filter_pairs'] = int(repository_functions_3['fbcsp_lda_nb_filter_pairs'])
            filter_parameter['nb_features_to_keep'] = int(repository_functions_4['nb_features_to_keep'])
            study_parameters_object.filter_parameter = filter_parameter


            self.label_confirmation.value = "You chose to work on the {} filter(s) with the following parameters:\r {}".format(
                study_parameters_object.list_filters, study_parameters_object.filter_parameter)

            self.button_filter_selection.disabled = True
            self.button_filter_selection.description = 'Unavailable'
            self.button_filter_selection.button_style = 'danger'

        self.button_filter_selection.on_click(click_filter_selection)