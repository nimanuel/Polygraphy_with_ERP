
% load feature extraction toolbox folder
addpath("../EEG-Feature-Extraction-Toolbox-main");

% some global constants
all_channels = [1,2,3,4,5,6,7,8,9,10,11,12];
channels_close_to_muse = [1,2,9,11];
seg_len = 1.6;
Fs = 500; %Hz


% load signals
lying = load("../data/lying_final_signals.mat");
honest = load("../data/honest_final_signals.mat");

mean_signal = honest.probe;
X = mean_signal.';
%%
% Band Power Alpha
opts.fs = 500;
f1 = jfeeg('ar', X, opts); 

% Display features
disp(f1);

%%

opts.fs = 500;
fa = jfeeg('bpa', X, opts); 
fb = jfeeg('bpb', X, opts); 
fg = jfeeg('bpg', X, opts); 
ft = jfeeg('bpt', X, opts); 
fd = jfeeg('bpd', X, opts); 


% Feature vector
feat = [fa, fb, fg, ft, fd];

% Display features
disp(feat)



