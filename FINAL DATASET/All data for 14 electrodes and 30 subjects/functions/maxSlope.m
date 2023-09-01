clc; clear;

% load feature extraction toolbox folder
addpath("../EEG-Feature-Extraction-Toolbox-main");

subject_list = {'subject1_session4', 'subject3_session3', ...
    'subject12_session3', 'subject9_session2', 'subject14_session5'};


t_low = 0.7; %sec
t_high = 0.9; %sec
Fs = 500; %Hz
Ts = 1/Fs;

honest_probe_path = '../data_table_form/honest_probe.mat';
guilty_probe_path = '../data_table_form/lying_probe.mat';
honest_target_path = '../data_table_form/honest_target.mat';
guilty_target_path = '../data_table_form/lying_target.mat';
honest_irr_path = '../data_table_form/honest_irrelevant.mat';
guilty_irr_path = '../data_table_form/lying_irrelevant.mat';


en_result_p = getMaxSlopeVector(guilty_probe_path, honest_probe_path, subject_list, t_low, t_high, Ts, 10);

en_result_t = getMaxSlopeVector(guilty_target_path, honest_target_path, subject_list, t_low, t_high, Ts, 10);

en_result_i = getMaxSlopeVector(guilty_irr_path, honest_irr_path, subject_list, t_low, t_high, Ts, 10);

en_result = [en_result_p; en_result_t; en_result_i];

%% plot 


nDataSets = 2;  % guilty/honest
nVars = 3;      % P/T/I
nVals = 5;      % num of signals taken (for each data set)
data = en_result;

% box chart

% Create column vector to indicate dataset
dataSet = categorical([ones(nVars*nVals,1); ...
    ones(nVars*nVals,1)*2;]);
dataSet = renamecats(dataSet,{'Guilty', 'Honest'});

% Create column vector to indicate the variable
clear var
var(1:nVals,1) = "Var1";
var(end+1:end+nVals,1) = "Var2";
var(end+1:end+nVals,1) = "Var3";
Var = categorical([var;var]);

% Create a table
testData = table(data,dataSet,Var);

% Actual visualization code using boxchart
boxchart(testData.dataSet,testData.data,"GroupByColor",testData.Var)
legend({'Probe', 'Target', 'Irrelevant'},'Location','bestoutside','Orientation','vertical')
title('Max Slope Value for Each Signal')
grid on
grid minor


%%
function max_slope_vec = getMaxSlopeVector(guilty_path, honest_path, sub_list, t_low, t_high, Ts, channel)
    num_signals = numel(sub_list);
    max_slope_vec = zeros(num_signals*2, 1);

    % guilty 
    for i = 1:num_signals
        var_name = sub_list{i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(floor(t_low/Ts):floor(t_high/Ts));
        slopes = gradient(signal);
        max_slope_vec(i,1) = max(abs(slopes));
    end

    % honest
    for i = 1:num_signals
        var_name = sub_list{i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(floor(t_low/Ts):floor(t_high/Ts));
         slopes = gradient(signal);
        max_slope_vec(num_signals+i,1) = max(abs(slopes));
    end
end

%%
function [mean_signal, is_relevant] = avg_of_segments(signal, segment_len, sample_rate)

    numSegments = size(signal,2);
    sum_signal = sum(signal, 2);
    mean_signal = (sum_signal / numSegments).';
    is_relevant = true;
    
end
%%

function [mean_signal_channels, is_signal_good] = avg_with_channels(signal_w_all_channels, segment_len, sample_rate, channels)

    sum_of_mean_signals = zeros(1, segment_len/sample_rate);
    num_of_channels_used = length(channels);
    is_signal_good = true;
    for i = 1:numel(channels)
        % Access the current element using the loop index
        ch_num = channels(i);
        
        % Perform operations on the element
        signal_one_channel = signal_w_all_channels(:,:, ch_num);
        [mean_signal, is_relevant] = avg_of_segments(signal_one_channel, segment_len, sample_rate);
        if (is_relevant)
            sum_of_mean_signals = sum_of_mean_signals + mean_signal;
        else
            num_of_channels_used = num_of_channels_used - 1;
        end
    end
    
    if (num_of_channels_used > 0)
        mean_signal_channels = sum_of_mean_signals/length(channels);
    else
        is_signal_good = false;
        mean_signal_channels = zeros(1, segment_len/sample_rate);
    end

end

