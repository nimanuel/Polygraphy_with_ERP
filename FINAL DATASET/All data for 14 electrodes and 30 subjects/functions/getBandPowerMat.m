% get bp vector for all subjects

function bp_result_mat = getBandPowerMat(var_names, honest_path, guilty_path, fs, channel)
    num_signals = numel(var_names);
    bp_result_mat = zeros(num_signals*2*5, 1);
    
   
    % guilty results

    for i = 1:num_signals
        var_name = var_names{:, i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(:, 0.6*500:0.9*500);
        bp_result_mat(5*(i-1)+1:5*i,1) = getBandPowers(signal, fs).';
    end


    % honest results

    for i = 1:num_signals
        var_name = var_names{:, i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(1, 0.6*500:0.9*500);
        bp_result_mat(5*(i-1+num_signals)+1:5*(i+num_signals),1) = getBandPowers(signal, fs).';
    end

end

%% function for getting band power features of subjects

function result = getBandPowers(signal, fs) 
    opts.fs = fs;
    bp_keys = {'bpa','bpb','bpg','bpt','bpd'};
    result = zeros(1,5);
    
    for i = 1:numel(bp_keys)
        key = bp_keys{i};
        result(i) = jfeeg(key, signal, opts); 
    end

end

