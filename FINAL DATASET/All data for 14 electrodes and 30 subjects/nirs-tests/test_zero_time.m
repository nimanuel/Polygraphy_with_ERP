clear all; close all; clc;

%% load data:
data = load("data_table_form\honest_irrelevant.mat", "subject1_session1");
m = data.subject1_session1;
clear data

%% signals:
e1 = electrodes.enum.Fp1;
e2 = electrodes.enum.VEOG;

s1 = squeeze(m(1, e1.index, :));
s2 = squeeze(m(1, e2.index, :));

55
num_tests = shape(m)

%%
% times:
Fs = 500; %Hz
Ts = 1/Fs;                                       
t = Ts*(1:length(s1));  
t = t - 0.5;

%% plot
figure()
plot(t, s1, DisplayName=string(e1))
hold on
plot(t, s2, DisplayName=string(e2))
legend()
grid on