clear; 
clc;
close all;

%%
fs = 1000; %Hz
Ts = 1/fs;

%%
t = readtable('Time_domain_data_for_deception.xlsx', Sheet='s15');
% event_data = load('Sub1_event_set1_data.mat', "event");

allowed_electrodes = "FP1";
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
    

    % Define wavelet parameters
    wname = 'db6';      % wavelet name
    scales = 1:64;      % wavelet scales
    dt = Ts;         % sampling period
    
    % Perform continuous wavelet transform
    [cfs, frequencies] = cwt(eeg, wname, scales, 'SamplingPeriod', dt);

    
    % Extract features from the coefficients
    energy = sum(abs(coefficients).^2, 2);
    entropy = -sum(abs(coefficients).^2 .* log(abs(coefficients).^2), 2);
    
    % Reconstruct signal using inverse discrete wavelet transform
    reconstructed_signal = waverec2(coefficients, [], wname);
    
    % Plot original and reconstructed signals
    figure;
    subplot(2,1,1);
    plot(eeg);
    title('Original signal');
    subplot(2,1,2);
    plot(reconstructed_signal);
    title('Reconstructed signal');
    
    % Plot wavelet features
    figure;
    subplot(2,1,1);
    plot(frequencies, energy);
    title('Wavelet energy');
    subplot(2,1,2);
    plot(frequencies, entropy);
    title('Wavelet entropy');

    

end
legend
grid on