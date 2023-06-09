%% Load:
clear; close all; clc;
data = load("lying\subject1\session2\irrelevant\irrelevant.txt");
data = data.';

%% time
t_start = 0;
t_end = (1.1+0.5)*30*4;
mean = data(:,1);
t = linspace(t_start, t_end, length(mean)).';

trim_times  = 0.0 : 1.6 : t_end;
event_times = 0.5 : 1.6 : t_end;
p300_times = event_times + 0.300;

%% Plot data:
figure;
ax1 = subplot(2,1,1);

N = size(data ,2)-2;
for i = 1 : N
    mean = data(:, i);
    plot(t, mean, DisplayName=string(i));
    hold on
end
xlabel("time [sec]")
title("All EEG")
add_times(event_times, trim_times, p300_times)

%% mean
ax2 = subplot(2,1,2);

eeg = data(:,1:end-2);
mean = sum(eeg, 2)/N;

plot(t, mean, Color='black')
xlabel("time [sec]")
title("Mean")
add_times(event_times, trim_times, p300_times)


linkaxes([ax1, ax2], "xy");


%%

%%

%% Subs:


function [] = add_times(event_times, trim_times, p300_times)
    for i = 1 : length(event_times)
        event_time = event_times(i);
        hold on
        scatter(event_time, 1, MarkerFaceColor='red', MarkerEdgeColor='red');
    end
    
    for i = 1 : length(trim_times)
        trim_time = trim_times(i);
        hold on
        xline(trim_time, LineStyle=':', Color='black');
    end
    
    for i = 1 : length(p300_times)
        p300_time = p300_times(i);
        hold on
        scatter(p300_time, 1, MarkerFaceColor='blue', MarkerEdgeColor='blue', Marker='*');
    end
end