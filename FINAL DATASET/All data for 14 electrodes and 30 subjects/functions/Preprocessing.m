%% Preprocessing
% this code takes the data in table form, from "data_table_form" directory 
% Preprocess it, and save as vectors

constScript; % holds all the constants

% fs = 500;
% T = 0.002;
% sample_length = 1.6; %sec
% number_of_sumples = sample_length*T;

elects = [electrodes.enum.Fp1.index;
    electrodes.enum.Fp2.index;
    electrodes.enum.P3.index;
    electrodes.enum.P4.index];


% --------- LYING ------------ %
%                         3             800  
working_data = zeros(2,TAG_NUM, number_of_sumples);




for i = 1:length(lying_path_list) 
    path = lying_path_list{i};
    [sum_sig, counter] = processSignals(path, 10, sample_length, T);
    signal = sum_sig / counter;

    working_data(1, i, :) = signal;
end


% applying filters

lying_probe      = highpass(signals(1, :), f_low, fs);
lying_target     = highpass(signals(2, :), f_low, fs);
lying_irrelevant = highpass(signals(3, :), f_low, fs);

lying_probe      = lowpass(lying_probe, f_high, fs);
lying_target     = lowpass(lying_target, f_high, fs);
lying_irrelevant = lowpass(lying_irrelevant, f_high, fs);


% --------- HONEST ------------ %

% Specify the paths to data files

%                       800
signal = zeros(3, number_of_sumples);

for i = 1:length(honest_path_list) 
    path = honest_path_list{i};
    [sum_sig, counter] = processSignals(path, 10, sample_length, T);
    signal = sum_sig / counter;
    signals(i, :) = signal;
end

% applying filters

honest_probe      = highpass(signals(1, :), f_low, fs);
honest_target     = highpass(signals(2, :), f_low, fs);
honest_irrelevant = highpass(signals(3, :), f_low, fs);

honest_probe      = lowpass(honest_probe, f_high, fs);
honest_target     = lowpass(honest_target, f_high, fs);
honest_irrelevant = lowpass(honest_irrelevant, f_high, fs);


