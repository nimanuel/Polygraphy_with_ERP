
% this code takes tha data in table form, from "data_table_form" directory 
% and plots it
%% displaySignals
all_channels = [1,2,3,4,5,6,7,8,9,10,11,12];

% cannels tat correlate with MUSE's channels
channels_close_to_muse = [1,2,9,11];

%% --------- LYING ------------ %

% Specify the paths to data files

probe_path = "../data_table_form/lying_probe.mat";
target_path = "../data_table_form/lying_target.mat";
irrelevant_path = "../data_table_form/lying_irrelevant.mat";
path_list = {probe_path, target_path, irrelevant_path};
signal = zeros(3, 1.6/0.002);

for i = 1:length(path_list) 
    path = path_list{i};
    [sum_sig, counter] = processSignals(path, 10, 1.6, 0.002);
    signal = sum_sig / counter;

    signals(i, :) = signal;
end


%% building the plot for lying's signals
t_start = -0.5;
t_end = 1.1;
t = linspace(t_start, t_end, length(signals(1, :))).';

f_low = 0.3;
f_high = 30;
fs = 500;

probe      = highpass(signals(1, :), f_low, fs);
target     = highpass(signals(2, :), f_low, fs);
irrelevant = highpass(signals(3, :), f_low, fs);

probe      = lowpass(probe, f_high, fs);
target     = lowpass(target, f_high, fs);
irrelevant = lowpass(irrelevant, f_high, fs);

% probe      = signals(1, :);
% target     = signals(2, :);
% irrelevant = signals(3, :);
% save("../data_table_form/lying_final_signals.mat","probe", "target", "irrelevant");

figure;
ax1 = subplot(2,1,1);
plot(t, probe, "r",'LineWidth',1);
hold on;
plot(t, target, "b--",'LineWidth',1);
hold on;
plot(t, irrelevant, "m-.",'LineWidth',1);
hold on;
% scatter([0.5], 1, 'DisplayName', 'picture is shown', MarkerFaceColor='red', MarkerEdgeColor='red');
% scatter([0.8], 1, 'DisplayName', 'estimated P300', MarkerFaceColor='blue', MarkerEdgeColor='blue');
hold on;
xlabel("time [sec]");
title("LYING");
legend('Probe', 'Target', 'Irrelevant');
grid on;
hold on;

%% --------- HONEST ------------ %

% Specify the paths to data files
probe_path = "../data_table_form/honest_probe.mat";
target_path = "../data_table_form/honest_target.mat";
irrelevant_path = "../data_table_form/honest_irrelevant.mat";
path_list = {probe_path, target_path, irrelevant_path};
signal = zeros(3, 1.6/0.002);

for i = 1:length(path_list) 
    path = path_list{i};
    [sum_sig, counter] = processSignals(path, 10, 1.6, 0.002);
    signal = sum_sig / counter;
    signals(i, :) = signal;
end


%% building the plot for honesr's signals
t_start = -0.5;
t_end = 1.1;
t = linspace(t_start, t_end, length(signals(1, :))).';

f_low = 0.3;
f_high = 30;
fs = 500;

probe      = highpass(signals(1, :), f_low, fs);
target     = highpass(signals(2, :), f_low, fs);
irrelevant = highpass(signals(3, :), f_low, fs);

probe      = lowpass(probe, f_high, fs);
target     = lowpass(target, f_high, fs);
irrelevant = lowpass(irrelevant, f_high, fs);

% probe      = signals(1, :);
% target     = signals(2, :);
% irrelevant = signals(3, :);
% save("../data/honest_final_signals.mat","probe", "target", "irrelevant");


ax2 = subplot(2,1,2);
plot(t, probe, "r",'LineWidth',1);
hold on;
plot(t, target, "b--",'LineWidth',1);
hold on;
plot(t, irrelevant, "m-.",'LineWidth',1);
hold on;
% scatter([0.5], 1, 'DisplayName', 'picture is shown', MarkerFaceColor='red', MarkerEdgeColor='red');
% scatter([0.8], 1, 'DisplayName', 'estimated P300', MarkerFaceColor='blue', MarkerEdgeColor='blue');
hold on;
xlabel("time [sec]");
title("HONEST");
legend('Probe', 'Target', 'Irrelevant');
grid on;
hold on;
linkaxes([ax1, ax2], "xy");



%%
function [sum_of_signals, counter]= processSignals(file_path, ch_nums, seg_len, sample_rate)

    var_names = whos("-file",file_path);
    counter = 0;
    sum_of_signals = zeros(1, 1.6/0.002);

    % Iterate over each variable in the directory
    for i = 1:numel(var_names)

        % Get the current variable name
        current_var_name = var_names(i).name;

        if contains(current_var_name,'subject',IgnoreCase=true) == false || contains(current_var_name,'session',IgnoreCase=true) == false
            continue;
        end
        
         load(file_path, current_var_name);
    
        % Access the variable using its name
        data = eval(current_var_name);
        
        [temp_signal, is_signal_good] = avg_with_channels(data, seg_len, sample_rate, ch_nums);

            if (is_signal_good)
                sum_of_signals = sum_of_signals + temp_signal;
            else
                counter = counter - 1;
            end
            
            % Display the var name 
            disp(current_var_name);
            counter = counter + 1;

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


%%