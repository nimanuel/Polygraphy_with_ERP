% this function 
% this function is only being called from avg_with_channels.m
function [mean_signal] = avg_of_segments(signal)

    numSegments = size(signal,2);
    sum_signal = sum(signal, 2);
    mean_signal = (sum_signal / numSegments).';    
end
