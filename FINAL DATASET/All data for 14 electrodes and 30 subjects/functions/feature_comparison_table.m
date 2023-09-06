% feature_comparison_table
% this table will help us eveluate the features 

% Assuming you want 3x3 for the example. Adjust for more columns.
data = cell(2, 3); 

data{1,1} = 'lying';
data{2,1} = 'honest';

% Create table
T = cell2table(data, 'VariableNames', {'TAG', 'feature_1', 'feature_2'});  % Adjust 'VariableNames' for more columns.
disp(T);
% Write the table to an Excel file
filename = 'feature_comparison_table.xlsx';
writetable(T, filename);