
filepath = '..\data\lying_probe_w_artifacts.mat';
save(filepath);

processFiles("..\lying", filepath, 'probe.txt')


%%

% Recursive function to process files
function []= processFiles(dir_path, save_path, stim_type)

    % Get a structure array containing information about the files
    files = dir(dir_path);

    % Iterate over each file in the directory
     for i = 1:numel(files)

        % Get the current variable name
        filename = files(i).name;

        % Exclude "." and ".." entries
        if strcmp(filename, '.') || strcmp(filename, '..')
            continue;
        end
        
        % Construct the full file path
        file_path = fullfile(dir_path, filename);

        % Check if the item is a file (excluding directories)
        if files(i).isdir == 0 && strcmp(filename,stim_type)

            % Perform the desired operations on the file

            % Load the data
            data = load(file_path);
            data = data.';

            % % Delete the last two columns
            % data(:, end-1:end) = [];
            % 
            % % Calculate the average of each column
            % channel_avg = mean(data, 2);
            % 
            % % Add the column average to the data
            % data_with_avg = [data channel_avg];
            data_with_avg = data;
            % get sheet name (subject and session)
            dir_list = strsplit(file_path, '\');
            var_name = strjoin({dir_list{3}, dir_list{4}}, '_');

            S.(var_name) = data_with_avg;
            
            save(save_path, '-struct', 'S', var_name, '-append');  


            % Save the matrix to a new sheet in the Excel file
            % writematrix(data_with_avg, save_path, 'Sheet', sheet_name);

            % Display the file name (optional)
            disp(file_path);

        else
            % Recursively process files in subdirectories
            processFiles(file_path, save_path, stim_type);
        end
    end
end

