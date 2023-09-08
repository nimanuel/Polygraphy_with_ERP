% feature_comparison_table
% this table will help us eveluate the features 

FEATURE_NUM = 8;
feat_comp_table = cell(0, FEATURE_NUM+2); 

fields = fieldnames(final_data);
for i = 1:numel(fields)
    field = fields{i};
    for j =1:size(final_data.(field),2)
        if final_data.(field){1,j}.sub > 2  % only 2 subjects for now. delete "if" later
            continue;
        elseif final_data.(field){1,j}.rep > 30
            continue;
        end
        feature_vector = extractFeaturs(final_data.(field){1,j}.tab(5,:));
        feat_comp_table{end+1,1} = structGetName(final_data.(field){1,j});
        for t = 2:(FEATURE_NUM+1)
            feat_comp_table{end,t} = feature_vector(t-1);
           
        end
       feat_comp_table{end,FEATURE_NUM+2} = structGetTag(final_data.(field){1,j});
 
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

%%
function [tag] = structGetTag(strt)
    if (strcmp(strt.tag, "honest_target") || strcmp(strt.tag, "lying_target"))
        tag = 'T';
    elseif (strcmp(strt.tag, "lying_probe"))
        tag = 'GP';
    else
        tag = 'else';
    end
end