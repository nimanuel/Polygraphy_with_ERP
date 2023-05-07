clear; 
clc;
close all;

%%
fs = 1000; %Hz
Ts = 1/fs;

%%
t = readtable('Time_domain_data_for_deception.xlsx', Sheet='s15');
% event_data = load('Sub1_event_set1_data.mat', "event");

allowed_electrodes = ["FP1", "FP2", "TP7", "TP8"];
%%
figure()

times = table2array(t(1, 2:end));
for iRow = 2 : size(t, 1)
    row = t(iRow, :);
    channel_name = row.Var1{1};
    channel_name = channel_name(2:end-1);
    channel_name = string(channel_name );

    if ~ismember(channel_name, allowed_electrodes)
        continue
    end

    eeg = table2array(row(:,2:end));

    plot(times, eeg, DisplayName=channel_name);
    hold on
end
legend
grid on