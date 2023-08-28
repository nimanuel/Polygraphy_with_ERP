clear all; close all; clc; 
addpath(genpath(pwd));

%%
e = electrodes.enum.Fp1;
i = e.index;
disp(e.is_close_to_muse)

%%
e = electrodes.enum.from_index(14);
disp(e)

%%