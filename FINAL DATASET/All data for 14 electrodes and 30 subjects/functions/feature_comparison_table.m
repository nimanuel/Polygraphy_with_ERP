% feature_comparison_table
% this table will help us eveluate the features 


% Assuming you want 3x3 for the example. Adjust for more columns.
% SIGNAL_NUM = 3;
FEATURE_NUM = 8;

feat_comp_table = cell(2, FEATURE_NUM+2); 

% 
% feat_comp_table{1,1} = 'signal1';
% feat_comp_table{2,1} = 'signal2';
% feat_comp_table{3,1} = 'signal3';
% for i = 1:SIGNAL_NUM
%     feature_vector = extractFeaturs(data_subject{5}{2}(:,1,i));
% 
%     for j = 2:(FEATURE_NUM+1)
%         feat_comp_table{i,j} = feature_vector(j-1);
% 
%     end
% end    
% 

fields = fieldnames(final_data);
for i = 1:numel(fields)
    field = fields{i};
    for j =1:size(final_data.(field),2)
        feature_vector = extractFeaturs(final_data.(field){1,j}.tab(5,:));
        feat_comp_table{j,1} = structGetName(final_data.(field){1,j});
        for t = 2:(FEATURE_NUM+1)
            
{j,t} = feature_vector(t-1);
        end
    end
end



% Create table
T = cell2table(feat_comp_table, 'VariableNames', {'Signal', 'min', 'max', 'entropy', ...
    'delta', 'alpha', 'beta', 'gamma', 'max slope', 'TAG'});  % Adjust 'VariableNames' for more columns.
disp(T);
% Write the table to an Excel file
filename = 'feature_comparison_table.xlsx';
writetable(T, filename);

%%
function [name] = structGetName(strt)
    name = "subject" + strt.sub + "_session" + strt.sess + "_rep" + strt.rep;
   
end
