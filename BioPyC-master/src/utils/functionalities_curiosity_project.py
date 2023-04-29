# -*- coding: utf-8 -*-

"""
This script is used for the curiosity project only
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License v3.0


import numpy as np


def deal_with_event_stimulation(events_):
    grading_based_on_both_click_n_grades = True

    events_ = np.concatenate((np.array([events_[1]]).T, np.array([events_[3]]).T, np.array([events_[2]]).T), axis=1)

    list_event_to_keep = [33041, 33042, 33043, 33044, 33026, 33027, 33028, 33029, 33030, 33031, 33032]
    mask_event_to_keep = np.in1d(list(events_[:,2]), list_event_to_keep)
    events_ = events_[mask_event_to_keep, :]

    vector_stimu = events_[:, 2]
    mask_stimu_to_keep, kept_stimu, list_labels, list_grades = select_stimulation(vector_stimu)


    if len(list_labels) == len(list_grades) and len(kept_stimu) == len(mask_stimu_to_keep) :
        pass
    else:
        raise Exception('There is a problem with stimulation fittings for epoching with MNE ! ')

    events_ = events_[mask_stimu_to_keep, :]
    events_[:, 2] = kept_stimu
    events_curious = events_[events_[:, 2] < 2]

    if grading_based_on_both_click_n_grades == True:

        # Calculate the mean of grades for this run
        mean_run = np.mean(list_grades)
        #median = np.median(list_grades)
        #if median == 1.0:
        #    median = 2.0
        #if median == 7.0:
        #    median = 6.0

        # Double check for labeling, keep only the trials with no curiosity + low rate and curiosity + high rate
        trials_to_keep = []

        # For each trials, keep it on 2 conditions
        for i in range(len(events_curious)):
            #if (events_curious[i, 2] == 0 and list_grades[i] < median) or (events_curious[i, 2] == 1 and list_grades[i] > median):
            if (events_curious[i, 2] == 0 and list_grades[i] < mean_run-1) or (events_curious[i, 2] == 1 and list_grades[i] > mean_run+1):
                trials_to_keep.append(i)
        events_curious = events_curious[trials_to_keep, :]

    event_id = dict(no_curious=0, curious=1)

    return events_curious, event_id


def assign_grade(stimu):
    if stimu == 33026 :
        return 1
    elif stimu == 33027 :
        return 2
    elif stimu == 33028 :
        return 3
    elif stimu == 33029 :
        return 4
    elif stimu == 33030 :
        return 5
    elif stimu == 33031 :
        return 6
    elif stimu == 33032 :
        return 7


def select_stimulation(vector_stimu):
    '''
    This function is running along the vector of stimulations, keeping them in memory only if the order is following a certain logic. For example,
    some subjects  type on the keyboard, automatically sending commands, event when they were not suppose to do it.

    By running along the vector, we also build a vector of labels
    '''

    list_keyboard_command = [33026, 33027, 33028, 33029, 33030, 33031, 33032]

    mask_stimu_to_keep = [] # vector of concatenates loops of stimulations positions [2,3,4,7,8,9,11,15,16,17... etc]
    kept_stimu = [] # vector of concatenates loops of stimulations codes [33041, 33042, 33043, 33044, 33026, 33041, 33042, 33043, 33044, 33027.. etc]

    list_labels = []
    list_grades = []

    begin_loop = 0
    stimu_n = 0

    nb_stimu = len(vector_stimu)

    for stimu in vector_stimu :

        if stimu == 33041:
            if begin_loop == 0: # check for starting a loop at the first 33041 -> stimu for displaying question
                mask_stimu_to_keep.append(stimu_n)
                kept_stimu.append(stimu)
                begin_loop +=1

            elif kept_stimu[-1] == 33044: # begin loop -> 33041
                mask_stimu_to_keep.append(stimu_n)
                kept_stimu.append(stimu)
            list_grades_single_question = [] # some subjects type several times on the keyboard, lets avoid doublons

        if stimu == 33042 and kept_stimu[-1] == 33041:  # begin question will end with end question -> 33042
            mask_stimu_to_keep.append(stimu_n)
            kept_stimu.append(stimu)

        if stimu == 33043 and kept_stimu[-1] == 33042: # begin answer -> 33043
            kept_stimu[-1] = 1 # Renaming for epoching with MNE directly giving labels
            mask_stimu_to_keep.append(stimu_n)
            kept_stimu.append(stimu)
            list_labels.append(1)  # Label = 1 since curious

        if stimu == 33044 :
            if stimu == 33044 and kept_stimu[-1] == 33043: # begin grading -> 33044
                mask_stimu_to_keep.append(stimu_n)
                kept_stimu.append(stimu)


            elif stimu == 33044 and kept_stimu[-1] == 33042: # begin grading -> 33044
                kept_stimu[-1] = 0 # Renaming for epoching with MNE
                mask_stimu_to_keep.append(stimu_n)
                kept_stimu.append(stimu)
                list_labels.append(0) # Label = 0 since not curious, did not chose to display the answer

        if stimu_n+2<=nb_stimu:
            if np.isin(stimu, list_keyboard_command) and (kept_stimu[-1] == 33044 or vector_stimu[stimu_n+1] == 33044 or vector_stimu[stimu_n+2] == 33044) and len(list_grades_single_question)<1:
                list_grades.append(assign_grade(stimu))
                list_grades_single_question.append(assign_grade(stimu))

        elif stimu_n+1<=nb_stimu:
            if np.isin(stimu, list_keyboard_command) and (kept_stimu[-1] == 33044 or vector_stimu[stimu_n+1] == 33044) and len(list_grades_single_question)<1:
                list_grades.append(assign_grade(stimu))
                list_grades_single_question.append(assign_grade(stimu))

        else:
            if np.isin(stimu, list_keyboard_command) and kept_stimu[-1] == 33044 and len(list_grades_single_question)<1:
                list_grades.append(assign_grade(stimu))
                list_grades_single_question.append(assign_grade(stimu))
        stimu_n += 1

    return mask_stimu_to_keep, kept_stimu, list_labels, list_grades
