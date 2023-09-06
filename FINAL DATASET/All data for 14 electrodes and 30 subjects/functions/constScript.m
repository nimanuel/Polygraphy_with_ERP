% constScript; % holds all the constants
% General
fs = 500;
T = 0.002;
sample_length = 1.6; %sec
number_of_sumples = 800;
TAG_NUM = 3; % Probe, Target, Irrelevant
SUBJECT_NUMBER = 15;
SESSION_NUMBER = 5;
% % 
% all_channels = [1,2,3,4,5,6,7,8,9,10,11,12];
% 
% % cannels tat correlate with MUSE's channels
% channels_close_to_muse = [1,2,9,11];
CHANNEL_NUMBER = 14;
% paths 
lying_probe_path = "../data_table_form/lying_probe.mat";
lying_target_path = "../data_table_form/lying_target.mat";
lying_irrelevant_path = "../data_table_form/lying_irrelevant.mat";

honest_probe_path = "../data_table_form/honest_probe.mat";
honest_target_path = "../data_table_form/honest_target.mat";
honest_irrelevant_path = "../data_table_form/honest_irrelevant.mat";


lying_path_list = {lying_probe_path, lying_target_path, lying_irrelevant_path};
honest_path_list = {honest_probe_path, honest_target_path, honest_irrelevant_path};

% EEG toolbix path
addpath("../EEG-Feature-Extraction-Toolbox-main");
% Preprocessing
f_low = 0.3;
f_high = 30;
t_start = -0.5;
t_end = 1.1;

addpath("..");
