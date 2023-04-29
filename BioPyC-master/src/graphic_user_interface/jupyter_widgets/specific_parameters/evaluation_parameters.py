# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the evalutation
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class evaluation_parameters(object):

    def __init__(self):
        self.list_evaluation_parameters = []
        self.container = None
        self.evaluation_parameters = None
        self.parameter_type = ''


    def display_widgets(self, widget_type = '',
                        study_parameters_object=None,
                        evaluation_parameters_object=None,
                        evaluation_parameters_object_2=None,
                        evaluation_parameters_object_3=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for choosing data evaluation parameters will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()

        if widget_type == 'select_multiple':
            # Creating a jupyter container with a selectmultiple box
            self.container = general_widgets_.create_selectmultiple_widget_container(value='Evaluation Parameters',
                                                                    options=self.list_evaluation_parameters)
        elif widget_type == 'textbox':
            # Creating a jupyter container with a selectmultiple box
            self.container = general_widgets_.create_textbox_widget_container(value='Evaluation Parameters',
                                                             options='')

        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_evaluation_parameters_selection = general_widgets_.button()
        display(self.button_evaluation_parameters_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_evaluation_parameters_selection(b):

            # Getting the data types the user has chosen
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Check if at least one data type is selected
            if len(repository_functions) == 0 :
                raise Exception('Not able to update evaluation parameters : please select parameter before')


            ###########################################
            # Updating parameters for the next step
            ###########################################

            if self.parameter_type == 'cross-validation_type':
                study_parameters_object.cross_val_type = repository_functions['cross-validation_type'][0]
            if self.parameter_type == 'type_split':
                study_parameters_object.type_split = repository_functions['type_split'][0]
            if self.parameter_type == 'training_split_ratio':
                study_parameters_object.training_split_ratio = float(repository_functions['training_split_ratio'])
            if self.parameter_type == 'nb_kfold':
                study_parameters_object.kfold = repository_functions['nb_kfold']

            if self.parameter_type == 'cross-validation_type' and study_parameters_object.evaluation_type == 'cross-validation':

                if study_parameters_object.cross_val_type == 'k-fold':
                    evaluation_parameters_object_3.parameter_type = 'nb_kfold'

                    evaluation_parameters_object_2.container.children[0].children[0].value = 'Split type'
                    evaluation_parameters_object_2.container.children[0].children[1].options = ['shuffle', 'chronological']
                    evaluation_parameters_object_2.button_evaluation_parameters_selection.description = 'Select this split type'
                    evaluation_parameters_object_2.button_evaluation_parameters_selection.disabled = False
                    evaluation_parameters_object_2.button_evaluation_parameters_selection.button_style = 'info'

                    evaluation_parameters_object_3.container.children[0].children[0].value = 'K-folds'
                    evaluation_parameters_object_3.container.children[0].children[1].value = '5'
                    evaluation_parameters_object_3.button_evaluation_parameters_selection.description = 'Select this number of splits'
                    evaluation_parameters_object_3.button_evaluation_parameters_selection.disabled = False
                    evaluation_parameters_object_3.button_evaluation_parameters_selection.button_style = 'info'

                elif study_parameters_object.cross_val_type == 'leave-one-out':


                    evaluation_parameters_object_2.container.children[0].children[0].value = 'Unavailable'
                    evaluation_parameters_object_2.container.children[0].children[1].options = []
                    evaluation_parameters_object_2.button_evaluation_parameters_selection.disabled = True
                    evaluation_parameters_object_2.button_evaluation_parameters_selection.description ='Unavailable'
                    evaluation_parameters_object_2.button_evaluation_parameters_selection.button_style = 'danger'

                    evaluation_parameters_object_3.container.children[0].children[0].value = 'Unavailable'
                    evaluation_parameters_object_3.container.children[0].children[1].value = ''
                    evaluation_parameters_object_3.button_evaluation_parameters_selection.disabled = True
                    evaluation_parameters_object_3.button_evaluation_parameters_selection.description ='Unavailable'
                    evaluation_parameters_object_3.button_evaluation_parameters_selection.button_style = 'danger'

                self.label_confirmation.value = "You chose {} as cross-validation type for your study".format \
                    (study_parameters_object.cross_val_type)

            elif self.parameter_type == 'type_split':
                self.label_confirmation.value = "You chose {} as split type for your study".format \
                    (study_parameters_object.type_split)

            elif self.parameter_type == 'training_split_ratio':
                self.label_confirmation.value = "You chose {} as training split ratio for your study".format \
                    (study_parameters_object.training_split_ratio)

            elif self.parameter_type == 'nb_kfold':
                self.label_confirmation.value = "You chose {} as number of kfold for your study".format \
                    (study_parameters_object.kfold)



            self.button_evaluation_parameters_selection.disabled =True
            self.button_evaluation_parameters_selection.description ='Unavailable'
            self.button_evaluation_parameters_selection.button_style = 'danger'

        self.button_evaluation_parameters_selection.on_click(click_evaluation_parameters_selection)