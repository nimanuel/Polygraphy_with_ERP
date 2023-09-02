% dataStructOrganizer
% orgenizes the data in cell arrays of subjects
% each subject holds a matrix of 4 cannels, and an average of the channels
constScript; % holds all the constants
%%
elects = [electrodes.enum.Fp1.index;
    electrodes.enum.Fp2.index;
    electrodes.enum.P3.index;
    electrodes.enum.P4.index];

% create table for one subject
mat_sub_data = cell(5, 4);  % Assuming you want 3x3 for the example. Adjust for more columns.
mat_sub_data{1,1} = 'Fp1';
mat_sub_data{2,1} = 'Fp2';
mat_sub_data{3,1} = 'P3';
mat_sub_data{4,1} = 'P4';
mat_sub_data{5,1} = 'average';
Table_for_subj = cell2table(mat_sub_data, 'VariableNames', {'Electrodes', 'Probe', 'Target', 'Irrelevant'});  % Adjust 'VariableNames' for more columns.
disp(Table_for_subj);
% % Write the table to an Excel file
% filename = 'dataStruct_Organizer_Table.xlsx';
% writetable(Table_for_subj, filename);

%% experiment to show Nir
% data_cell = {};
% for subject_num = 1:1  %       ????
%     data_cell{end + 1} = createSubjectArray(mat_sub_data, subject_num);
% end
% disp(data_cell);
%%


data_cell = {};
for subject_num = 1:SUBJECT_NUMBER  %       ????
    data_cell{end + 1} = createSubjectArray(channel_matrix, subject_num);
    
end



% target = (1:10);
% subject1.honest_target = target;
% subject1.honest_target = target;
% 
% subject1.probe = target;
% subject2.target = target;
% 
% cell = {subject1,subject2};
% disp(cell{1}.target);

%%

temp = create_subject_table(1);




%%
% add 

function[sub] = createSubjectArray(channel_matrix, subject_num)
    
    fieldName = ['subject' num2str(subject_num)];
    subStruct.channels = channel_matrix;
    sub.(fieldName) = subStruct;

end



%%
function [subject_table] = create_subject_table(subject_num)
%     lying_path_list = {lying_probe_path, lying_target_path, lying_irrelevant_path};
%     honest_path_list = {honest_probe_path, honest_target_path, honest_irrelevant_path};
%     var_name = sub_list{:, i};
%     load(guilty_path, var_name);
%     signal = eval(var_name);

% lying probe
    fieldName = ['subject' num2str(subject_num) '_session1'];
    path = lying_path_list[1];
    load(path,"subject1_session1");
    signal = eval("fieldName");
    subject_table = zeros(size(signal(1),size(signal(2),5)));
    counter =1;
    for i = 1:CHANNEL_NUMBER
        if (ismember(i, elects))
            subject_table(:,:,counter) = signal(:,:,i);
            counter = counter + 1;
        end
    end 
end







