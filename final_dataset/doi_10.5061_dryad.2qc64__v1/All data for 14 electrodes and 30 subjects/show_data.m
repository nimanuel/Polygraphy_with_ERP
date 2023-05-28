clear; 
clc;
close all;

%%
% the signals are prepocessed as follows:
% band pass filter 0.1-30 HZ
% sampling at 500 Hz

filename = ".\honest\subject1\session1\probe\probe.txt";
% signal = textscan(FILE,'%n', 1, 'Delimiter', ' ');

signal = readtable(filename, 'Delimiter', ' ','VariableNamingRule','preserve');



                                        
Fs = 500; %Hz
Ts = 1/Fs;                                       
t = Ts*(1:width(signal))*2;   

% channel_name = 'FP1';
% row = t(1, :);
% eeg = table2array(row(:,2:end));


figure
plot(t, signal)
% xticks(ticks)% Time Vector
grid
title('Time Domain')
xlabel('Time (s)')
ylabel('Amplitude (Units)')

% fclose(FILE);
%%
%_____________________________________________________________

% Open the text file for reading
fileID = fopen('your_file.txt', 'r');

% Specify the format of the data in the file
formatSpec = '%f %f %f %f';  % Assuming the row contains four numeric values

% Read the row using textscan
rowData = textscan(fileID, formatSpec, 1, 'Delimiter', ' ');

% Close the file
fclose(fileID);

% Extract the data from the cell array
data = cell2mat(rowData);

% Display the row data
disp(data);