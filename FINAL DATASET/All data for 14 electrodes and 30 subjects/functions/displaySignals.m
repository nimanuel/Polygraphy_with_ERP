% displaySignals
% this code takes tha data in table form, from "data_table_form" directory 
% and plots it

% fs = 500;
% T = 0.002;
% sample_length = 1.6; %sec
% number_of_sumples = sample_length*T;

constScript; % holds all the constants

% --------- LYING ------------ %

% Specify the paths to data files

lying_path_list = {lying_probe_path, lying_target_path, lying_irrelevant_path};
signal = zeros(3, number_of_sumples);


for i = 1:length(lying_path_list) 
    path = lying_path_list{i};
    [sum_sig, counter] = processSignals(path, 10, sample_length, T);
    signal = sum_sig / counter;

    signals(i, :) = signal;
end


% building the plot for lying's signals
t = linspace(t_start, t_end, length(signals(1, :))).';

lying_probe      = highpass(signals(1, :), f_low, fs);
lying_target     = highpass(signals(2, :), f_low, fs);
lying_irrelevant = highpass(signals(3, :), f_low, fs);

lying_probe      = lowpass(lying_probe, f_high, fs);
lying_target     = lowpass(lying_target, f_high, fs);
lying_irrelevant = lowpass(lying_irrelevant, f_high, fs);


figure;
ax1 = subplot(2,1,1);
plot(t, lying_probe, "r",'LineWidth',1);
hold on;
plot(t, lying_target, "b--",'LineWidth',1);
hold on;
plot(t, lying_irrelevant, "m-.",'LineWidth',1);
hold on;
% scatter([0.5], 1, 'DisplayName', 'picture is shown', MarkerFaceColor='red', MarkerEdgeColor='red');
% scatter([0.8], 1, 'DisplayName', 'estimated P300', MarkerFaceColor='blue', MarkerEdgeColor='blue');
hold on;
xlabel("time [sec]");
title("LYING");
legend('Probe', 'Target', 'Irrelevant');
grid on;
hold on;

% --------- HONEST ------------ %

% Specify the paths to data files
honest_path_list = {honest_probe_path, honest_target_path, honest_irrelevant_path};
signal = zeros(3, 1.6/0.002);

for i = 1:length(honest_path_list) 
    path = honest_path_list{i};
    [sum_sig, counter] = processSignals(path, 10, sample_length, T);
    signal = sum_sig / counter;
    signals(i, :) = signal;
end


% building the plot for honesr's signals
t = linspace(t_start, t_end, length(signals(1, :))).';

honest_probe      = highpass(signals(1, :), f_low, fs);
honest_target     = highpass(signals(2, :), f_low, fs);
honest_irrelevant = highpass(signals(3, :), f_low, fs);

honest_probe      = lowpass(honest_probe, f_high, fs);
honest_target     = lowpass(honest_target, f_high, fs);
honest_irrelevant = lowpass(honest_irrelevant, f_high, fs);


ax2 = subplot(2,1,2);
plot(t, honest_probe, "r",'LineWidth',1);
hold on;
plot(t, honest_target, "b--",'LineWidth',1);
hold on;
plot(t, honest_irrelevant, "m-.",'LineWidth',1);
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


