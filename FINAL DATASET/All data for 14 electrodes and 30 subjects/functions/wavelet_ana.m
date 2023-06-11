% import signals 

honest_probe_path = '../data/honest_probe_renorm.mat';
guilty_probe_path = '../data/lying_probe_renorm.mat';
honest_target_path = '../data/honest_target_renorm.mat';
guilty_target_path = '../data/lying_target_renorm.mat';
honest_irr_path = '../data/honest_irrelevant_renorm.mat';
guilty_irr_path = '../data/lying_irrelevant_renorm.mat';

t_low = 0.7;
t_high = 0.9;
Ts = 0.002;
channel = 10;

path_to_use = guilty_probe_path;

var_name = 'subject3_session4';
load(path_to_use, var_name);
signal = eval(var_name);
signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
signal = signal(floor(t_low/Ts):floor(t_high/Ts));
sigal = signal.';

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



