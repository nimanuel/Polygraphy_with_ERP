% ICA for removing eye artifacts

function clean_data = ICA(path)

    addpath("..");

    % Load the 3D matrix from the file
    load(path, 'matrix');

    % electrodes to use
    elects = [electrodes.enum.Fp1.index;
        electrodes.enum.Fp2.index;
        electrodes.enum.P3.index;
        electrodes.enum.P4.index];
    
    % Access the specified rows
    selectedRows = matrix(elects, :, :);
    
    % e = electrodes.enum.Fp1.index

    q = 1;
    Mdl = rica(raw_data,q,'NonGaussianityIndicator',ones(6,1));
    
    unmixed = transform(Mdl,raw_data);

end
%%

% x = ICA("../data_table_form/honest_probe.mat");

