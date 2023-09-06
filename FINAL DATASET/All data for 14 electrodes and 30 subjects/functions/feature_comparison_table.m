% feature_comparison_table
% this table will help us eveluate the features 


% Assuming you want 3x3 for the example. Adjust for more columns.
SIGNAL_NUM = 3;
FEATURE_NUM = 8;
 

% sub5ses2e1 = data_subject{5}{2}(:,1,1);
% sub5ses2e2 = data_subject{5}{2}(:,1,2);
% sub5ses2e3 = data_subject{5}{2}(:,1,3);

% feature_vector1 = extractFeaturs(sub5ses2e1);
% feature_vector2 = extractFeaturs(sub5ses2e2);
% feature_vector3 = extractFeaturs(sub5ses2e3);
% 




feat_comp_table = cell(2, FEATURE_NUM+2); 

feat_comp_table{1,1} = 'signal1';
feat_comp_table{2,1} = 'signal2';
feat_comp_table{3,1} = 'signal3';

for i = 1:SIGNAL_NUM
    feature_vector = extractFeaturs(data_subject{5}{2}(:,1,i));

    for j = 2:(FEATURE_NUM+1)
        feat_comp_table{i,j} = feature_vector(j-1);

    end
end    

% Create table
T = cell2table(feat_comp_table, 'VariableNames', {'Signal', 'min', 'max', 'entropy', ...
    'delta', 'alpha', 'beta', 'gamma', 'max slope', 'TAG'});  % Adjust 'VariableNames' for more columns.
disp(T);
% Write the table to an Excel file
filename = 'feature_comparison_table.xlsx';
writetable(T, filename);
