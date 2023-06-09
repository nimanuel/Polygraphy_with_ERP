
read = "./honest/subject1/session1/probe/probe.txt";

% Specify the existing Excel file path
filepath = '.\file.xlsx';
% 
% % Specify the sheet name for the new sheet
% sheetname = 'probesheet';
% 
% data = load(read);
% data = data.';
% 
% % Save the matrix to a new sheet in the Excel file
% writematrix(data, filepath, 'Sheet', sheetname);

processFiles(".\lying", filepath, 'probe.txt')

%%

% Recursive function to process files
function []= processFiles(dir_path, save_path, stim_type)
    % Get a structure array containing information about the files
    files = dir(dir_path);
    % Iterate over each file in the directory
    for i = 1:numel(files)
        % Obtain the file name
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
            
           
            % get sheet name (subject and session)
            dir_list = strsplit(file_path, '\');
            sheetname = strjoin({dir_list{3}, dir_list{4}}, '_');
            
            % Save the matrix to a new sheet in the Excel file
            writematrix(data, save_path, 'Sheet', sheetname);

            % Display the file name (optional)
            disp(file_path);

        else
            % Recursively process files in subdirectories
            processFiles(file_path, save_path, stim_type);
        end
    end
end

