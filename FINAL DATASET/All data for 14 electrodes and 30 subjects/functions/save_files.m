% orgenizes the data in .mat tables for easy usedata_table_form
% lying probe
mkdir("..\data_table_form");
filepath = '..\data_table_form\lying_probe.mat';
save(filepath);
processFiles("..\lying", filepath, 'probe.txt')

% lying target
filepath = '..\data_table_form\lying_target.mat';
save(filepath);
processFiles("..\lying", filepath, 'target.txt')

% lying irrelevant
filepath = '..\data_table_form\lying_irrelevant.mat';
save(filepath);
processFiles("..\lying", filepath, 'irrelevant.txt')

% honest probe
filepath = '..\data_table_form\honest_probe.mat';
save(filepath);
processFiles("..\honest", filepath, 'probe.txt')

% honest target
filepath = '..\data_table_form\honest_target.mat';
save(filepath);
processFiles("..\honest", filepath, 'target.txt')

% honest irrelevant
filepath = '..\data_table_form\honest_irrelevant.mat';
save(filepath);
processFiles("..\honest", filepath, 'irrelevant.txt')

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
        
            % Load the data
            data = load(file_path);
            data = data.';
            data_with_avg = data;
            dir_list = strsplit(file_path, '\');
            var_name = strjoin({dir_list{3}, dir_list{4}}, '_');
            S.(var_name) = data_with_avg;
            save(save_path, '-struct', 'S', var_name, '-append');  
            disp(file_path);

        else
            % Recursively process files in subdirectories
            processFiles(file_path, save_path, stim_type);
        end
    end
end

