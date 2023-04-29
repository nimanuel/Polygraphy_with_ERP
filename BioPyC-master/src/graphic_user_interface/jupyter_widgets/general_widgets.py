# -*- coding: utf-8 -*-

"""
The class mat is made for displaying general widgets
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0



import ipywidgets as widgets

class general_widgets(object):

    def __init__(self):
        pass

    # Set buttons
    def button(self, label='Unavailable', disabled=True):
        """
        This methods creates a jupyter button widget
        :param label: label to display on button, to make user´s life easier
        :return:
        """
        # add button that allows you to chose your data set
        button_ = widgets.Button(description=label,
                                 button_style='warning',
                                 disabled=disabled,
                                 layout=widgets.Layout(width='50%',
                                                       height='40px'))

        return button_

    # Set functions values
    def get_functions_values(self, container_functions):
        """
        Extraction of the different values from the container
        """
        repository_functions = {}
        for l in container_functions.children:
            description = l.children[0].value
            l = l.children[1]
            #if l.value:

            if description == 'Signals types':
                repository_functions['signals_type'] = l.value
            if description == 'Data types':
                repository_functions['data_type'] = l.value

            elif description == 'Calibration types':
                repository_functions['calibration_type'] = l.value
            elif description == 'Evaluation types':
                repository_functions['evaluation_type'] = l.value

            elif description == 'Cross-validation types':
                repository_functions['cross-validation_type'] = l.value
            elif description == 'Training split ratio':
                repository_functions['training_split_ratio'] = l.value
            elif description == 'Split type':
                repository_functions['type_split'] = l.value
            elif description == 'K-folds':
                repository_functions['nb_kfold'] = l.value


            elif description == 'Datasets':
                repository_functions['dataset'] = l.value

            # Preprocessing parameters
            elif description == 'List of subjects to keep':
                repository_functions['list_of_subjects_to_keep'] = l.value
            elif description == 'List of sessions':
                repository_functions['list_of_sessions'] = l.value
            elif description == 'List of runs':
                repository_functions['list_of_runs'] = l.value
            elif description == 'List of band-pass':
                repository_functions['list_of_band-pass'] = l.value
            elif description == 'Specify labeling':
                repository_functions['specify_labels'] = l.value
            elif description == 'Dictionary of "labels: stimulations"':
                repository_functions['dictionary_labels_stimulations'] = l.value
            elif description == 'Tmin (can be negative)':
                repository_functions['tmin'] = l.value
            elif description == 'Tmax (can be negative)':
                repository_functions['tmax'] = l.value

            # channels and preprocessing
            elif description == 'List of all channels':
                repository_functions['list_all_channels'] = l.value
            elif description == 'Dictionary of signal types / List of associated channels':
                repository_functions['dictionary_signal_types_channels'] = l.value
            elif description == 'List of EOG (indexes or names)':
                repository_functions['list_eog'] = l.value
            elif description == 'List of channels to drop':
                repository_functions['list_channels_to_drop'] = l.value

            # Preprocessed data parameters
            elif description == 'Band-pass delimiters':
                repository_functions['bandpass_delimiters'] = l.value

            # Filters
            elif description == 'Available filters':
                repository_functions['list_filters'] = l.value
            elif description == 'CSP number of filter pairs':
                repository_functions['csp_lda_nb_filter_pairs'] = l.value
            elif description == 'FBCSP number of filter pairs per band-pass':
                repository_functions['fbcsp_lda_nb_filter_pairs'] = l.value
            elif description == 'FBCSP number of features to keep':
                repository_functions['nb_features_to_keep'] = l.value

            # CLassifiers
            elif description == 'Available classifiers':
                repository_functions['list_classifiers'] = l.value
            elif description == 'Filter Bank Riemmanian Methods number features to keep':
                repository_functions['nb_features_to_keep'] = l.value
            elif description == 'Single pass-band':
                repository_functions['single_passband'] = l.value
            elif description == 'Filter Bank pass-bands':
                repository_functions['filter_bank_passbands'] = l.value


            elif description == 'passband(s)':
                repository_functions['passband'] = l.value

            #elif description == 'Training split ratio':
            #    repository_functions['training_split_ratio'] = l.value

            elif description == 'type of split':
                repository_functions['type_split'] = l.value
            elif description == 'results filename':
                repository_functions['results_filename'] = l.value
            elif description == 'study types':
                repository_functions['study_type'] = l.value

            # Stats and plottings
            elif description == 'Available plottings':
                repository_functions['list_plottings'] = l.value
            elif description == 'Available statistical tests':
                repository_functions['list_stats'] = l.value



        return repository_functions

    # Create a select multiple
    def create_selectmultiple_widget_container(self,
                                               value=None,
                                               options=None
                                               ):
        """
        This method create a container with two horizontally adjusted boxes, first the label box, then the selectmultiple box
        :param value: name of the label, i.e. the functonality we ask the user to chose
        :param label_flex: relative horizontal size fo the label box in the container
        :param selectmultiple_flex: relative horizontal size fo the selectmultiple box in the container
        :param options:
        :return: jupyter container containing the selectmultiple box and the associated label
        """
        function_ = [
            widgets.HBox([widgets.Label(value=value,
                                        layout=widgets.Layout(width='25%', height='60px')
                                        ),
                          widgets.SelectMultiple(
                              options=options,
                              value=[],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='60px')
                          )])
        ]

        container_function = widgets.VBox()
        container_function.children = [i for i in function_]
        return container_function

    def create_textbox_widget_container(self,
                                        value=None,
                                        options=None
                                        ):
        """
        This method create a container with two horizontally adjusted boxes, first the label box, then the textbox
        :param value: name of the label, i.e. the functonality we ask the user to chose
        :param label_flex: relative horizontal size fo the label box in the container
        :param textbox_flex: relative horizontal size fo the textbox in the container
        :return: jupyter container containing the textbox and the associated label
        """
        function_ = [
            widgets.HBox([widgets.Label(value=value,
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options,
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )])
        ]
        container_function = widgets.VBox()
        container_function.children = [i for i in function_]
        return container_function

    def create_preprocessing_container(self,
                                       values=[],
                                       options=[]
                                       ):
        """
        This method create a container with two horizontally adjusted boxes, first the label box, then the selectmultiple box
        :param value: name of the label, i.e. the functonality we ask the user to chose
        :param label_flex: relative horizontal size fo the label box in the container
        :param selectmultiple_flex: relative horizontal size fo the selectmultiple box in the container
        :param options:
        :return: jupyter container containing the selectmultiple box and the associated label
        """

        function_ = [
            widgets.HBox([widgets.Label(value=values[0],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[0],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[1],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[1],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[2],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[2],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[3],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[3],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[4],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[4],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[5],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[5],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[6],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[6],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[7],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[7],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[8],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[8],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[9],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[9],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )]),
            widgets.HBox([widgets.Label(value=values[10],
                                        layout=widgets.Layout(width='25%', height='40px')
                                        ),
                          widgets.Text(
                              value=options[10],
                              disabled=False,
                              layout=widgets.Layout(width='25%', height='40px')
                          )])
        ]
        container_function = widgets.VBox()
        container_function.children = [i for i in function_]
        return container_function