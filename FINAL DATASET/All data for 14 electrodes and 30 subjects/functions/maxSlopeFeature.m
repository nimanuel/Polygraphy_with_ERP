
function max_slope_result = maxSlopeFeature(t_low, t_high, Ts, ...
    honest_probe_path, guilty_probe_path, ...
    honest_target_path, guilty_target_path, ...
    honest_irr_path, guilty_irr_path)

    en_result_p = getMaxSlopeVector(guilty_probe_path, honest_probe_path, subject_list, t_low, t_high, Ts, 10);
    en_result_t = getMaxSlopeVector(guilty_target_path, honest_target_path, subject_list, t_low, t_high, Ts, 10);
    en_result_i = getMaxSlopeVector(guilty_irr_path, honest_irr_path, subject_list, t_low, t_high, Ts, 10);
    max_slope_result = [en_result_p; en_result_t; en_result_i];
    
    % plot 
    nDataSets = 2;  % guilty/honest
    nVars = 3;      % P/T/I
    nVals = 5;      % num of signals taken (for each data set)
    data = max_slope_result;
    
    % box chart
    
    % Create column vector to indicate dataset
    dataSet = categorical([ones(nVars*nVals,1); ...
        ones(nVars*nVals,1)*2;]);
    dataSet = renamecats(dataSet,{'Guilty', 'Honest'});
    
    % Create column vector to indicate the variable
    clear var
    var(1:nVals,1) = "Var1";
    var(end+1:end+nVals,1) = "Var2";
    var(end+1:end+nVals,1) = "Var3";
    Var = categorical([var;var]);
    
    % Create a table
    testData = table(data,dataSet,Var);
    
    % Actual visualization code using boxchart
    boxchart(testData.dataSet,testData.data,"GroupByColor",testData.Var)
    legend({'Probe', 'Target', 'Irrelevant'},'Location','bestoutside','Orientation','vertical')
    title('Max Slope Value for Each Signal')
    grid on
    grid minor
end
