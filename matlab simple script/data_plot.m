clear;
load("online.mat", "online")
load("training.mat", "training")
load("BCICIV_calib_ds1a.mat","cnt")

% 
% % display signal of 3 channels
% plot(online(:,2:5))
% 
% % display signal of 3 channels
% plot(training(:,2:5))

plot(cnt)
