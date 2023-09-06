% TODO: ADD DESCRIPTION. IF USED IN 1 OR 2 FILES, NAME THEM
function [sum_of_signals, counter]= processSignals(file_path, ch_nums, seg_len, sample_rate)

    var_names = whos("-file",file_path);
    counter = 0;
    sum_of_signals = zeros(1, 1.6/0.002);

    % Iterate over each variable in the directory
    for i = 1:numel(var_names)

        % Get the current variable name
        current_var_name = var_names(i).name;

        if contains(current_var_name,'subject',IgnoreCase=true) == false || contains(current_var_name,'session',IgnoreCase=true) == false
            continue;
        end
        
         load(file_path, current_var_name);
    
        % Access the variable using its name
        data = eval(current_var_name);
        
        [temp_signal, is_signal_good] = avg_with_channels(data, seg_len, sample_rate, ch_nums);

            if (is_signal_good)
                sum_of_signals = sum_of_signals + temp_signal;
            else
                counter = counter - 1;
            end
            
            % Display the var name 
            disp(current_var_name);
            counter = counter + 1;

    end

end
