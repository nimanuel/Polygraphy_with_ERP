classdef enum 
    enumeration
        Fp1  % close to muse
        Fp2  % close to muse  
        F3 
        Fz   % close to muse's ground
        F4 
        C3 
        Cz 
        C4 
        P3   % close to muse
        Pz   
        P4   % close to muse
        Oz
        VEOG
        HEOG
    end


    methods 
        function tf = is_close_to_muse(obj)
            indices_close_to_muse = [1, 2, 9, 11];
            index = obj.index;
            if ismember(index, indices_close_to_muse)
                tf = true;
            else
                tf = false;
            end
        end

        function i = index(obj)       
            in_order = names_in_order();
            i = find(string(obj)==in_order);
        end

    end % methods


    methods (Static)
        function e = from_index(i)
            in_order = names_in_order();
            name = in_order(i);
            e = electrodes.enum(name);
        end
    end % static methods
end


%%

%{ 
    Muse electrodes
    AF7 AF8
    TP9 TP10

    Our closest:
    Fp1 Fp2
    P3  P4
%}

function lis = names_in_order()
    lis = ["Fp1", "Fp2", "F3", "Fz", "F4", ...
        "C3", "Cz", "C4", "P3", "Pz", "P4", "Oz", ...
        "VEOG", "HEOG"
    ];
end