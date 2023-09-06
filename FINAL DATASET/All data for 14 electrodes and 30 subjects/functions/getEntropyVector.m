function entopy_vec = getEntropyVector(guilty_path, honest_path, sub_list, t_low, t_high, Ts, channel)
    addpath("../EEG-Feature-Extraction-Toolbox-main");

    num_signals = numel(sub_list);
    entopy_vec = zeros(num_signals*2, 1);

    % guilty 
    for i = 1:num_signals
        var_name = sub_list{i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        entopy_vec(i,1) = jfeeg('sh', signal);
    end

    % honest
    for i = 1:num_signals
        var_name = sub_list{i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        entopy_vec((num_signals+i),1) = jfeeg('sh', signal);
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


