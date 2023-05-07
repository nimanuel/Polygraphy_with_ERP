clear; 
clc;
close all;

%%
% eeglab;
% EEG = eeg_retrieve( data, 1 );


f = 250; %Hz
T = 1/f;
% 

table = load('Sub1_EEG_raw_set1_data.mat','EEG');
event_data = load('Sub1_event_set1_data.mat', "event");

event = event_data.event;
data = table.EEG;
ch01 = data(1,:);
ch01_subsampled = ch01(1:300:end);
% ch01_bpf = ch01(1:1/f:end);

ch02 = data(2,:);
ch02_subsampled = ch02(1:300:end);
% ch02_bpf = ch02(1:1/f:end);

ch03 = data(3,:);
ch03_subsampled = ch03(1:300:end);
% ch03_bpf = ch03(1:1/f:end);

% Create a vector of time stamps (assuming one second between each column)
timeStamps = 1:length(ch01); 
% timeStamps = T*timeStamps;
time_subsampled = timeStamps(1:300:end);
% time_bpf = timeStamps(1:1/f:end);

% time_stamps = linspace(0, length(ch01), f);


% Plot the data
plot(timeStamps, ch01,'-');
hold on;
plot (timeStamps, ch02, '-');
hold on;
plot (timeStamps, ch03, '-');
grid on
legend('ch01','ch02', 'ch03');


% event:
times = [event.latency];
type = [event.type];
hold on
scatter(times, type, DisplayName="Event")

% Add labels to the x-axis and y-axis
xlabel('Time (ms)');
ylabel('Data');

hold off;
