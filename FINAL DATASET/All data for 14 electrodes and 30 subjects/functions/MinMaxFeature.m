% min max feature extraction and plot

function min_max_result = MinMaxFeature(t_low, t_high, Ts, ...
    honest_probe_path, guilty_probe_path, ...
    honest_target_path, guilty_target_path, ...
    honest_irr_path, guilty_irr_path)

    var_names_g_probe = getVarNames(guilty_probe_path);
    var_names_g_target = getVarNames(guilty_target_path);
    var_names_g_irrelevant = getVarNames(guilty_irr_path);
    
    var_names = intersect(intersect(var_names_g_probe,var_names_g_target,'stable'),...
        var_names_g_irrelevant,'stable');
    
    min_result_p = getMinVector(guilty_probe_path, honest_probe_path, var_names, t_low, t_high, Ts, 10);
    max_result_p = getMaxVector(guilty_probe_path, honest_probe_path, var_names, t_low, t_high, Ts, 10);
    
    min_result_t = getMinVector(guilty_target_path, honest_target_path, var_names, t_low, t_high, Ts, 10);
    max_result_t = getMaxVector(guilty_target_path, honest_target_path, var_names, t_low, t_high, Ts, 10);
    
    min_result_i = getMinVector(guilty_irr_path, honest_irr_path, var_names, t_low, t_high, Ts, 10);
    max_result_i = getMaxVector(guilty_irr_path, honest_irr_path, var_names, t_low, t_high, Ts, 10);
    
    min_max_result = [min_result_p; max_result_p; min_result_t; max_result_t; min_result_i; max_result_i];

    % plot

    % lengths of variables:
    nDataSets = 6;                          % guilty/honest OR min/max
    nVars = 2;                              % num of subcategories (e.g, freq bands or P/T/I)
    nVals = length(min_max_result)/12;       % num of signals taken (for each data set)
    
    data = min_max_result;
    
    % box chart
    
    % Create column vector to indicate dataset
    dataSet = categorical([ones(nVars*nVals,1); ...
        ones(nVars*nVals,1)*2; ...
        ones(nVars*nVals,1)*3; ...
        ones(nVars*nVals,1)*4; ...
        ones(nVars*nVals,1)*5; ...
        ones(nVars*nVals,1)*6;]);
    dataSet = renamecats(dataSet,{'Min', 'Max', 'Min - Target', 'Max - Target', 'Min - Irrelevant', 'Max - Irrelevant'});
    % Create column vector to indicate the variable
    clear var
    var(1:nVals,1) = "Var1";
    var(end+1:end+nVals,1) = "Var2";
    Var = categorical([var;var;var;var;var;var]);
    % Create a table
    testData = table(data,dataSet,Var);
    
    % Actual visualization code using boxchart
    boxchart(testData.dataSet,testData.data,"GroupByColor",testData.Var)
    legend({'Guilty', 'Honest'},'Location','bestoutside','Orientation','vertical')
    title('Min vs Max values for Each type of signal in 2250 Samples')
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
