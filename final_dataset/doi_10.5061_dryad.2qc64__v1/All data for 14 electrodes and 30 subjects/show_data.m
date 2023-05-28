clear; 
clc;
close all;

%%
% the signals are prepocessed as follows:
% band pass filter 0.1-30 HZ
% sampling at 500 Hz

filename =".\lying\subject1\session1\probe\probe.txt";
% signal = textscan(FILE,'%n', 1, 'Delimiter', ' ');

table = readtable(filename);


                                        
Fs = 500; %Hz
Ts = 1/Fs;                                       
t = Ts*(1:width(table));   

eeg_fp1 = table2array(table(1,1:end));
eeg_fp2 = table2array(table(2,1:end));
eeg_p3 = table2array(table(9,1:end));
eeg_p4 = table2array(table(11,1:end));

figure
plot(t, eeg_fp1);
hold on;
plot(t, eeg_fp2);
hold on;
plot(t, eeg_p3);
hold on;
plot(t, eeg_p4);
hold on;
legend('Fp1', 'Fp2', 'P3', 'P4');

grid
title('Time Domain')
xlabel('Time (s)')
ylabel('Amplitude (Units)')

hold off;

%%
