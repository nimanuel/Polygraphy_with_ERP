# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the evaluation type
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class evaluation_type(object):

    def __init__(self):
        self.list_evaluation_types = ['classic', 'cross-validation']
        self.container = None
        self.evaluation_type = None

    def display_widgets(self, study_parameters_object=None, evaluation_parameters_object=None, evaluation_parameters_object_2=None, evaluation_parameters_object_3=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for choosing evaluation types user will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()

        # Creating a jupyter container with a selectmultiple box allowing to display evaluation types
        self.container = general_widgets_.create_selectmultiple_widget_container(value='Evaluation types',
                                                                                options=self.list_evaluation_types)

        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_evaluation_type_selection = general_widgets_.button()
        display(self.button_evaluation_type_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_evaluation_type_selection(b):

            # Getting the data types the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one data type is selected
            if len(repository_functions) == 0:
                raise Exception('Not able to update evaluation types : please select an evaluation before')

            ###########################################
            # Updating parameters for the next step
            ###########################################
            study_parameters_object.evaluation_type = repository_functions['evaluation_type'][0]

            self.label_confirmation.value = "You chose {} as evaluation for your study".format \
                (study_parameters_object.evaluation_type)


            if study_parameters_object.evaluation_type == 'cross-validation':
                evaluation_parameters_object.container.children[0].children[0].value = 'Cross-validation types'
                evaluation_parameters_object.container.children[0].children[1].options = ['k-fold', 'leave-one-out']
                evaluation_parameters_object.button_evaluation_parameters_selection.description = 'Select this cross-validation type'
                evaluation_parameters_object.button_evaluation_parameters_selection.disabled = False
                evaluation_parameters_object.button_evaluation_parameters_selection.button_style = 'info'


            elif study_parameters_object.evaluation_type == 'classic':
                evaluation_parameters_object_3.parameter_type = 'training_split_ratio'

                evaluation_parameters_object_3.container.children[0].children[0].value = 'Training split ratio'
                evaluation_parameters_object_3.container.children[0].children[1].value = '0.5'
                evaluation_parameters_object_3.button_evaluation_parameters_selection.description = 'Select this training split ratio'
                evaluation_parameters_object_3.button_evaluation_parameters_selection.disabled = False
                evaluation_parameters_object_3.button_evaluation_parameters_selection.button_style = 'info'

                evaluation_parameters_object_2.container.children[0].children[0].value = 'Split type'
                evaluation_parameters_object_2.container.children[0].children[1].options = ['shuffle', 'chronological']
                evaluation_parameters_object_2.button_evaluation_parameters_selection.description = 'Select this split type'
                evaluation_parameters_object_2.button_evaluation_parameters_selection.disabled = False
                evaluation_parameters_object_2.button_evaluation_parameters_selection.button_style = 'info'

                #evaluation_parameters_object_2.container.children[0].children[0].value = 'Unavailable'
                #evaluation_parameters_object_2.container.children[0].children[1].options = []
                #evaluation_parameters_object_2.button_evaluation_parameters_selection.disabled = True
                #evaluation_parameters_object_2.button_evaluation_parameters_selection.description = 'Unavailable'
                #evaluation_parameters_object_2.button_evaluation_parameters_selection.button_style = 'danger'

                evaluation_parameters_object.container.children[0].children[0].value = 'Unavailable'
                evaluation_parameters_object.container.children[0].children[1].options = ''
                evaluation_parameters_object.button_evaluation_parameters_selection.disabled = True
                evaluation_parameters_object.button_evaluation_parameters_selection.description = 'Unavailable'
                evaluation_parameters_object.button_evaluation_parameters_selection.button_style = 'danger'


            self.button_evaluation_type_selection.disabled =True
            self.button_evaluation_type_selection.description ='Unavailable'
            self.button_evaluation_type_selection.button_style = 'danger'

        self.button_evaluation_type_selection.on_click(click_evaluation_type_selection)