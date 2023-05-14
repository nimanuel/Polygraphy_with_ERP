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

    % get the maximum amplitude
    max_amplitude = max(abs(eeg));

    plot(times, eeg, DisplayName=channel_name);
    hold on
    % display the result
    plot(times(eeg == max_amplitude), max_amplitude,'r*', DisplayName='max amplitude');
    

    disp(['features of: ', channel_name]);
    disp(['max amplitude: ', num2str(max_amplitude)]);

    % Calculate the positive area under the curve
    positive_eeg = eeg;
    positive_eeg(positive_eeg < 0) = 0; % set negative values to zero
    positive_area = trapz(times, positive_eeg);
    disp(['positive area: ', num2str(positive_area)]);

    % Calculate the negative area under the curve
    negative_eeg = eeg;
    negative_eeg(negative_eeg > 0) = 0; % set negative values to zero
    negative_area = trapz(times, negative_eeg);
    disp(['negative area: ', num2str(negative_area)]);

    % Calculate the total area
    total_area = positive_area + negative_area;
    disp(['total area: ', num2str(total_area)]);

    disp('-------------------');
    
    hold on
    
end


legend
grid on