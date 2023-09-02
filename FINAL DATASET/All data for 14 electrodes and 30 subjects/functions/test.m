constScript; % holds all the constants


temp = create_subject_table(1);
%%

function [subject_table] = create_subject_table(subject_num)
constScript; % holds all the constants
%     lying_path_list = {lying_probe_path, lying_target_path, lying_irrelevant_path};
%     honest_path_list = {honest_probe_path, honest_target_path, honest_irrelevant_path};
%     var_name = sub_list{:, i};
%     load(guilty_path, var_name);
%     signal = eval(var_name);

% lying probe
    fieldName = ['subject' num2str(subject_num) '_session1'];
    path1 = lying_path_list{1};
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




