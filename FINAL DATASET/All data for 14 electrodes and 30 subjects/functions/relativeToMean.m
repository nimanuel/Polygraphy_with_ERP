
% Specify the file path
file_path = '../data/lying_probe.mat';
save_path = '../data/lying_probe_renorm.mat';

renormalize(file_path, save_path);

%% renormalize channel signals

function []= renormalize(file_path, save_path)

    var_names = whos("-file",file_path);
    
    % Iterate through the variables
    for i = 1:numel(var_names)

        % Get the current variable name
        current_var_name = var_names(i).name;
    
        if contains(current_var_name,'subject',IgnoreCase=true) == true && contains(current_var_name,'session',IgnoreCase=true) == true
    
            load(file_path, current_var_name);
    
            % Access the variable using its name
            data = eval(current_var_name);
            
            % allocate new array for renormalized signals:
            renormalized_sig = zeros(length(data), 12);

            % get avg of channels (13th column)
            channels_avg = data(:, 13);
    
            % data = table - 12 channel columns and 13th col for avg of chanels
            for channel_index = 1:12
                renormalized_sig(:, channel_index) = data(:, channel_index) - channels_avg;
            end
        
            % export data to new variable in .mat file
            S.(current_var_name) = renormalized_sig;
            save(save_path, '-struct', 'S', current_var_name, '-append');

            
            % Display the variable name
            disp(['Variable Name: ' current_var_name]);
    
        end
    
    end
end







