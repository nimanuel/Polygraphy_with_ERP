clc; clear;


subject_list = {'subject1_session4', 'subject3_session3', ...
    'subject12_session3', 'subject9_session2', 'subject14_session5'};


t_low = 0.7; %sec
t_high = 0.9; %sec
Fs = 500; %Hz
Ts = 1/Fs;

honest_probe_path = '../data/honest_probe_renorm.mat';
guilty_probe_path = '../data/lying_probe_renorm.mat';
honest_target_path = '../data/honest_target_renorm.mat';
guilty_target_path = '../data/lying_target_renorm.mat';
honest_irr_path = '../data/honest_irrelevant_renorm.mat';
guilty_irr_path = '../data/lying_irrelevant_renorm.mat';


min_result_p = getMinVector(guilty_probe_path, honest_probe_path, subject_list, t_low, t_high, Ts, 10);
max_result_p = getMaxVector(guilty_probe_path, honest_probe_path, subject_list, t_low, t_high, Ts, 10);

min_result_t = getMinVector(guilty_target_path, honest_target_path, subject_list, t_low, t_high, Ts, 10);
max_result_t = getMaxVector(guilty_target_path, honest_target_path, subject_list, t_low, t_high, Ts, 10);

min_result_i = getMinVector(guilty_irr_path, honest_irr_path, subject_list, t_low, t_high, Ts, 10);
max_result_i = getMaxVector(guilty_irr_path, honest_irr_path, subject_list, t_low, t_high, Ts, 10);

min_max_result = [min_result_p; max_result_p; min_result_t; max_result_t; min_result_i; max_result_i];

%% plot

% lengths of variables:
nDataSets = 6;  % guilty/honest OR min/max
nVars = 2;      % num of subcategories (e.g, freq bands or P/T/I)
nVals = 5;      % num of signals taken (for each data set)
data = min_max_result;

% box chart

% Create column vector to indicate dataset
dataSet = categorical([ones(nVars*nVals,1); ...
    ones(nVars*nVals,1)*2; ...
    ones(nVars*nVals,1)*3; ...
    ones(nVars*nVals,1)*4; ...
    ones(nVars*nVals,1)*5; ...
    ones(nVars*nVals,1)*6;]);
dataSet = renamecats(dataSet,{'Min - Probe', 'Max - Probe', 'Min - Target', 'Max - Target', 'Min - Irrelevant', 'Max - Irrelevant'});
% Create column vector to indicate the variable
clear var
var(1:nVals,1) = "Var1";
var(end+1:end+nVals,1) = "Var2";
Var = categorical([var;var;var;var;var;var]);
% Create a table
testData = table(data,dataSet,Var);

% Actual visualization code using boxchart
boxchart(testData.dataSet,testData.data,"GroupByColor",testData.Var)
legend({'Guilty', 'Honest'},'Location','bestoutside','Orientation','vertical')
title('Min vs Max values')
grid on
grid minor

%%
function min_vec = getMinVector(guilty_path, honest_path, sub_list, t_low, t_high, Ts, channel)
    num_signals = numel(sub_list);
    min_vec = zeros(num_signals*2, 1);

    % guilty 
    for i = 1:num_signals
        var_name = sub_list{i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        min_vec(i,1) = min(abs(signal));
    end

    % honest
    for i = 1:num_signals
        var_name = sub_list{i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        min_vec((num_signals+i),1) = min(abs(signal));
    end
end

%%
function max_vec = getMaxVector(guilty_path, honest_path, sub_list, t_low, t_high, Ts, channel)
    num_signals = numel(sub_list);
    min_vec = zeros(num_signals*2, 1);

    % guilty 
    for i = 1:num_signals
        var_name = sub_list{i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        max_vec(i,1) = max(abs(signal));
    end

    % honest
    for i = 1:num_signals
        var_name = sub_list{i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        max_vec((num_signals+i),1) = max(abs(signal));
    end
end

%%
function [mean_signal, is_relevant] = avg_of_segments(signal, segment_len, sample_rate)

    numSegments = floor(length(signal)*sample_rate / segment_len);

    if (length(signal) == numSegments*segment_len/sample_rate)
        % Reshape the signal so that each segment is in a separate row
        reshaped_signal = reshape(signal, segment_len/sample_rate, numSegments);
        sum_signal = sum(reshaped_signal, 2);
        mean_signal = (sum_signal / numSegments).';
        is_relevant = true;
    else
        mean_signal = zeros(1, segment_len/sample_rate);
        is_relevant = false;
    end
    
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
        signal_one_channel = signal_w_all_channels(:,ch_num);
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








