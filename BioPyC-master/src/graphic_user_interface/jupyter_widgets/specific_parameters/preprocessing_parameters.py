# -*- coding: utf-8 -*-

"""
The class mat is made for displaying the choice of the preprocessing parameters
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


from src.graphic_user_interface.jupyter_widgets.general_widgets import general_widgets
import ipywidgets as widgets

class preprocessing_parameters(object):

    def __init__(self):
        self.list_options = []
        self.container = None

    def display_widgets(self, study_parameters_object=None,
                        classifiers_object=None,
                        filters_object=None):
        """
        This method allows to display jupyter's label and selectmultiple boxes for choosing processing parameters user will use
        :return: Nothing returned, just displaying
        """
        general_widgets_ = general_widgets()


        # Creating a jupyter container with a selectmultiple box allowing to display available datasets in data_store
        self.container = general_widgets_.create_preprocessing_container(values=['List of subjects to keep',
                                                                                'List of sessions',
                                                                                'List of runs',
                                                                                'Specify labeling',
                                                                                'Dictionary of "labels: stimulations"',
                                                                                'Tmin (can be negative)',
                                                                                'Tmax (can be negative)',
                                                                                'List of all channels',
                                                                                'Dictionary of signal types / List of associated channels',
                                                                                'List of EOG (indexes or names)',
                                                                                'List of channels to drop'],
                                                                        options=['[31,33]',
                                                                                 #'[1,2,3,4,5,6,7,8,9]',
                                                                                 '[1]', # List of sessions to keep for the study
                                                                                 #'[1, 2]', # List of runs in each session to keep for each subject
                                                                                 '[1, 2,3,4]',# List of runs in each session to keep for each subject
                                                                                 'True', # labeling
                                                                                 '{}', # dictionary of labels/stimulations
                                                                                 "{'EEG': -4.0, 'breathing': -10.0}",
                                                                                 # "{'EEG': 2.5}",
                                                                                 "{'EEG': 0.0, 'breathing': 6.0}",
                                                                                 #"{'EEG': 4.5}",
                                                                                 "['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9', 'CP5', 'CP1', 'Pz',"
                                                                                 "'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'C4', 'T8', 'FT10',"
                                                                                 "'FC6', 'FC2', 'F4', 'F8', 'Fp2', 'AF7', 'AF3', 'AFz', 'F1', 'F5', 'FT7', 'FC3', 'FCz',"
                                                                                 "'C1', 'C5', 'TP7', 'CP3', 'P1', 'P5', 'PO7', 'PO3', 'POz', 'PO4', 'PO8', 'P6', 'P2',"
                                                                                 "'CPz', 'CP4', 'TP8', 'C6', 'C2', 'FC4', 'FT8', 'F6', 'F2', 'AF4', 'AF8', 'Channel 65',"
                                                                                 "'Channel 66', 'Channel 67', 'Channel 68', 'Channel 69', 'Channel 70', 'Channel 71',"
                                                                                 "'Channel 72', 'STI 014']",
                                                                                 #"{}", # dicionrt signaly type channel
                                                                                 "{'EEG': ['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 'T7', 'TP9', 'CP5', 'CP1', 'Pz',"
                                                                                 "'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'C4', 'T8',"
                                                                                 "'FC6', 'FC2', 'F4', 'Fp2', 'AF7', 'AF3', 'AFz', 'F1', 'F5', 'FT7', 'FC3', 'FCz',"
                                                                                 "'C1', 'C5', 'TP7', 'CP3', 'P1', 'P5', 'PO7', 'PO3', 'POz', 'PO4', 'PO8', 'P6', 'P2',"
                                                                                 "'CPz', 'CP4', 'TP8', 'C6', 'C2', 'FC4', 'FT8', 'F6', 'F2', 'AF4'], 'breathing': ['Channel 65']}",
                                                                                 #str(['EOG-left', 'EOG-central', 'EOG-right']),
                                                                                 str(['FT10', 'F8', 'AF8']),
                                                                                 #str(['STI 014'])
                                                                                 str(['Channel 66', 'Channel 69', 'Channel 70', 'Channel 71', 'Channel 72', 'STI 014'])
                                                                                 ])


        widgets.interactive(self.container)
        display(self.container)

        # Creating the jupyter button widget
        self.button_preprocessing_parameters_selection = general_widgets_.button()
        display(self.button_preprocessing_parameters_selection)

        # Creating the labels field
        self.label_confirmation = widgets.Label(value='')
        display(self.label_confirmation)

        def click_preprocessing_parameters_selection(b):

            # Getting the preprocessing parameters the user chose
            repository_functions = general_widgets_.get_functions_values(self.container)

            # Updating study parameters
            study_parameters_object.list_subjects_to_keep = eval(repository_functions['list_of_subjects_to_keep'])

            study_parameters_object.list_sessions = eval(repository_functions['list_of_sessions'])
            study_parameters_object.list_runs = eval(repository_functions['list_of_runs'])
            study_parameters_object.specify_labeling = eval(repository_functions['specify_labels'])
            study_parameters_object.dictionary_stimulations = eval(repository_functions['dictionary_labels_stimulations'])
            study_parameters_object.tmin = eval(repository_functions['tmin'])
            study_parameters_object.tmax = eval(repository_functions['tmax'])
            if repository_functions['list_all_channels'] != "[]":
                study_parameters_object.list_all_channels = eval(repository_functions['list_all_channels'])
            else:
                study_parameters_object.list_all_channels = []

            study_parameters_object.dictionary_signals_channels = eval(repository_functions['dictionary_signal_types_channels'])
            study_parameters_object.list_eog = eval(repository_functions['list_eog'])

            study_parameters_object.list_channels_to_drop = eval(repository_functions['list_channels_to_drop'])

            self.label_confirmation.value = "You chose to preprocess your data with the parameters above."


            # Updating the button of the next step
            filters_object.button_filter_selection.disabled = False
            filters_object.button_filter_selection.description = "Select this (list of) filter(s)"
            filters_object.button_filter_selection.button_style = 'info'

            classifiers_object.button_classifier_selection.disabled = False
            classifiers_object.button_classifier_selection.description = "Select this (list of) classifier(s)"
            classifiers_object.button_classifier_selection.button_style = 'info'

            # Updating button of the current step
            self.button_preprocessing_parameters_selection.disabled =True
            self.button_preprocessing_parameters_selection.description ='Unavailable'
            self.button_preprocessing_parameters_selection.button_style ='danger'

        self.button_preprocessing_parameters_selection.on_click(click_preprocessing_parameters_selection)