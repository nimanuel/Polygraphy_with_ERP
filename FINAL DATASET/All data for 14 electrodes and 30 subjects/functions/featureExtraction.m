
% load feature extraction toolbox folder
addpath("../EEG-Feature-Extraction-Toolbox-main");


% load signals
lying = load("../data/lying_final_signals.mat");
honest = load("../data/honest_final_signals.mat");

% h = honest, g = guilty
h_p = honest.probe.';
h_t = honest.target.';
h_i = honest.irrelevant.';
g_p = lying.probe.';
g_t = lying.target.';
g_i = lying.irrelevant.';



%% BAND POWER
opts.fs = 500;
disp('     alpha     beta      gamma     theta     delta');


% honest probe
fa = jfeeg('bpa', h_p, opts); 
fb = jfeeg('bpb', h_p, opts); 
fg = jfeeg('bpg', h_p, opts); 
ft = jfeeg('bpt', h_p, opts); 
fd = jfeeg('bpd', h_p, opts); 

% Feature vector
feat_h_p = [fa, fb, fg, ft, fd];

% Display features



% guilty probe
fa = jfeeg('bpa', g_p, opts); 
fb = jfeeg('bpb', g_p, opts); 
fg = jfeeg('bpg', g_p, opts); 
ft = jfeeg('bpt', g_p, opts); 
fd = jfeeg('bpd', g_p, opts); 

% Feature vector
feat_g_p = [fa, fb, fg, ft, fd];

% Display features


result = getBandPowers(g_p, 500);
disp(result)

%% 5 random subjects

subject_list = {'subject1_session4', 'subject3_session3', ...
    'subject12_session3', 'subject9_session2', 'subject14_session5'};
honest_probe_path = '../data/honest_probe_renorm.mat';
guilty_probe_path = '../data/lying_probe_renorm.mat';

probe_feat = getBandPowerMat(subject_list, honest_probe_path, guilty_probe_path, 500, 10);
save("probe_feat.mat", "probe_feat");


%% function for getting band power features of subjects

function result = getBandPowers(signal, fs) 
    opts.fs = fs;
    bp_keys = {'bpa','bpb','bpg','bpt','bpd'};
    result = zeros(1,5);
    
    for i = 1:numel(bp_keys)
        key = bp_keys{i};
        result(i) = jfeeg(key, signal, opts); 
    end

end


%% get bp vector for all subjects

% get subject and session numbers (make sure they exist for guilty because
% not all of them do !

function bp_result_mat = getBandPowerMat(sub_list, honest_path, guilty_path, fs, channel)
    num_signals = numel(sub_list);
    bp_result_mat = zeros(num_signals*2*5, 1);

    %guilty results

    for i = 1:num_signals
        var_name = sub_list{i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(0.6*500:0.6*500, :);
        bp_result_mat(5*(i-1)+1:5*i,1) = getBandPowers(signal, fs).';
    end


    % honest results

    for i = 1:numel(sub_list)
        var_name = sub_list{i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(0.6*500:0.6*500, :);
        bp_result_mat(5*(i-1+num_signals)+1:5*(i+num_signals),1) = getBandPowers(signal, fs).';
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

