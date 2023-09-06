% plot bandpass power features

function probe_bp_feat = BandpassFeature(honest_probe_path, guilty_probe_path)

    % load feature extraction toolbox folder
    addpath("../EEG-Feature-Extraction-Toolbox-main");
    
    % BAND POWER ANALYSIS
    
    list = getVarNames(guilty_probe_path);
    probe_bp_feat = getBandPowerMat(list, honest_probe_path, guilty_probe_path, 500, 10);
     
    % lengths of variables:
    nDataSets = 2;  % guilty, honest
    nVars = 5;      % frequency bands
    nVals = length(probe_bp_feat)/10;      % how many random sessions did we take? (1 means we took the feature of one signal)
    freq_bands = {'Alpha','Beta','Gamma','Theta','Delta'};
    
    % box chart
    
    % Create column vector to indicate dataset
    dataSet = categorical([ones(nVars*nVals,1); ...
        ones(nVars*nVals,1)*2]);
    dataSet = renamecats(dataSet,{'Guilty', 'Honest'});

    % Create column vector to indicate the variable
    clear var
    vars = ["Var1"; "Var2"; "Var3"; "Var4"; "Var5"];
    
    for i = 1 : 5 : 5*nVals
        var(i:i+4, 1) = vars;
    end
    
    Var = categorical([var;var]);

    % Create a table
    testData = table(data,dataSet,Var);
    
    % Actual visualization code using boxchart
    boxchart(testData.dataSet,testData.data,"GroupByColor",testData.Var)
    legend(freq_bands,'Location','bestoutside','Orientation','vertical')
    title('Band Power Desnity in Probe Signals for Different Frequency Bands for 2250 Samples')
    grid on
    grid minor
    

end

%%
function [mean_signal, is_relevant] = avg_of_segments(signal, segment_len, sample_rate)

    numSegments = size(signal,2);
    sum_signal = sum(signal, 2);
    mean_signal = (sum_signal / numSegments).';
    is_relevant = true;
    
end
%%

function [mean_signal_channels, is_signal_good] = avg_with_channels(signal_w_all_channels, segment_len, sample_rate, channels)

    sum_of_mean_signals = zeros(1, segment_len/sample_rate);
    num_of_channels_used = length(channels);
    is_signal_good = true;
    for i = 1:numel(channels)
        % Access the current element using the loop index
        ch_num = channels(i);
        
        % Perform operations on the element
        signal_one_channel = signal_w_all_channels(:,:, ch_num);
        [mean_signal, is_relevant] = avg_of_segments(signal_one_channel, segment_len, sample_rate);
        if (is_relevant)
            sum_of_mean_signals = sum_of_mean_signals + mean_signal;
        else
            num_of_channels_used = num_of_channels_used - 1;
        end
    end
    
    if (num_of_channels_used > 0)
        mean_signal_channels = sum_of_mean_signals/length(channels);
    else
        is_signal_good = false;
        mean_signal_channels = zeros(1, segment_len/sample_rate);
    end

end
