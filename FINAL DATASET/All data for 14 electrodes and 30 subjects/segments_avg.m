clear; close all; clc;


%%

data = load("lying\subject1\session2\target\target.txt");
data = data.';
eeg = data(:,1);
mean_seg= avg_with_channels(data, 1.6, 0.002, [1]);
mean_diff = avg_of_segments(eeg, 1.6, 0.002);
t_start = 0;
t_end = 1.6;

t = linspace(t_start, t_end, length(mean_seg)).';


figure;
ax1 = subplot(2,1,1);

    plot(t, mean_seg);
    hold on

xlabel("time [sec]")
title("All EEG")

figure;
ax2 = subplot(2,1,1);

    plot(t, mean_diff);
    hold on

xlabel("time [sec]")
title("EEG")
%%
function mean_signal = avg_of_segments(signal, segment_len, sample_rate)

   
    numSegments = floor(length(signal)*sample_rate / segment_len);

    % Reshape the signal so that each segment is in a separate row
    reshaped_signal = reshape(signal, segment_len/sample_rate, numSegments);
    sum_signal = sum(reshaped_signal,2);
    
    mean_signal = sum_signal / numSegments;

end
%%

function mean_signal_channels = avg_with_channels(signal_w_all_channels, segment_len, sample_rate, channels)

    sum_of_mean_signals = zeros(segment_len/sample_rate);

    for i = 1:numel(channels)
        % Access the current element using the loop index
        ch_num = channels(i);
        
        % Perform operations on the element
        signal_one_channel = signal_w_all_channels(:,ch_num);
        mean_signal = avg_of_segments(signal_one_channel, segment_len, sample_rate);
        sum_of_mean_signals = sum_of_mean_signals + mean_signal;
    end

    mean_signal_channels = sum_of_mean_signals/length(channels);

end


%%