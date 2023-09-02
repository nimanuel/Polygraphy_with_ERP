%clear all; close all; clc;

%% load data:
data = load("..\data_table_form\honest_irrelevant.mat", "subject1_session1");
m = data.subject1_session1;
subject_session = "subject4_session1";
data = load("..\data_table_form\honest_irrelevant.mat", subject_session);
m = data.(subject_session);
clear data

%% signals:
e1 = electrodes.enum.Fp1;
e2 = electrodes.enum.VEOG;

s1 = squeeze(m(1, e1.index, :));
s2 = squeeze(m(1, e2.index, :));


num_tests = shape([m]);
%%
num_tests = size(m,1);
for i = 2 : num_tests
    s1_ = squeeze(m(i, e1.index, :));
    s1 = s1 + s1_;

    s2_ = squeeze(m(i, e2.index, :));
    s2 = s2 + s2_;
end

%%
% times:
Fs = 500; %Hz
Ts = 1/Fs;                                       
t = Ts*(1:length(s1));  
t = t - 0.5;
t_base = Ts*(1:length(s1));  
t = t_base - 0.5;

%% plot
figure()
plot(t, s1, DisplayName=string(e1))
hold on
plot(t, s2, DisplayName=string(e2))
legend()
grid on

%% Analyze:
figure()
[c, lags] = xcorr(s1, s2);
t_corr =  lags/(2*Fs);

stem(t_corr, c)
xlabel('lag [sec]')
ylabel('r')
grid on;