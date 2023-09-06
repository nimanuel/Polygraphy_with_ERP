function min_vec = getMinVector(guilty_path, honest_path, sub_list, t_low, t_high, Ts, channel)
    num_signals = numel(sub_list);
    min_vec = zeros(num_signals*2, 1);

    % guilty 
    for i = 1:num_signals
        var_name = sub_list{:, i};
        load(guilty_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(floor(t_low/Ts):floor(t_high/Ts));
        min_vec(i,1) = min(abs(signal));
    end

    % honest
    for i = 1:num_signals
        var_name = sub_list{:, i};
        load(honest_path, var_name);
        signal = eval(var_name);
        signal = avg_with_channels(signal, 1.6, 0.002, [channel]);
        signal = signal(floor(t_low/Ts):floor(t_high/Ts));
        min_vec((num_signals+i),1) = min(abs(signal));
    end
end