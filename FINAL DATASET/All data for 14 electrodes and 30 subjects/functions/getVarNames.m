%% get variable names
function var_names_list = getVarNames(mat_path)
    var_names = whos("-file", mat_path);
    var_names_list = {};
    for i = 1:numel(var_names)
        current_var_name = var_names(i).name;
        if contains(current_var_name, 'subject', 'IgnoreCase', true) == false ...
            || contains(current_var_name, 'session', 'IgnoreCase', true) == false
            continue;
        elseif i == 1
            var_names_list = {current_var_name};
        else
            var_names_list = [var_names_list, {current_var_name}];
        end
    end
end
