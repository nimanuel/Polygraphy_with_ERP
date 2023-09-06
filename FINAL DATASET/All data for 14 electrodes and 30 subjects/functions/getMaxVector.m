function max_vec = getMaxVector(guilty_path, honest_path, sub_list, t_low, t_high, Ts, channel)
    num_signals = numel(sub_list);
    min_vec = zeros(num_signals*2, 1);

    % guilty 
    for i = 1:num_signals
        var_name = sub_list{i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        max_vec(i,1) = max(abs(signal));
    end

    % honest
    for i = 1:num_signals
        var_name = sub_list{i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(t_low/Ts:t_high/Ts);
        max_vec((num_signals+i),1) = max(abs(signal));
    end
end
