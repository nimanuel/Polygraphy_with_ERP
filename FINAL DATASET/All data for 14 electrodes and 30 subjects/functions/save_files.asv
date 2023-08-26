% orgenizes the data in .mat tables for easy usedata_table_form
folderName = "..\data_table_form";  

% Check if the folder exists
if ~exist(folderName, 'dir')
    % If the folder doesn't exist, create it
    mkdir(folderName);
end


% lying probe
filepath = '..\data_table_form\lying_probe.mat';
save(filepath);
processFiles("..\lying", filepath, 'probe.txt')
%%
% lying target
filepath = '..\data_table_form\lying_target.mat';
save(filepath);
processFiles("..\lying", filepath, 'target.txt')
%%
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
    f = 500; % Hz
    event_len = 1.6; % event length
    box_num = f*event_len; % there are 30 segments os 1.6 sec for each data row

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
            numRows = size(data, 1);
            numColumns = size(data, 2);
            threeD_Array = reshape(data, numRows/box_num, numColumns, box_num);

  
            data_with_avg = threeD_Array;
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

