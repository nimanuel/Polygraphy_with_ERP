% this function will apply featur extraction functions onto the signal it
% got, and place them in a vector
function [feature_vector] = extractFeaturs(signal)
    constScript; % holds all the constants
    % Min_Max
    featue_abs_min = min(abs(signal));
    featue_abs_max = max(abs(signal));    

    % Entropy
    featue_entropy = jfeeg('sh', signal);

    % Band Power
    opts.fs = fs;
    feature_dalta_bp = jfeeg('bpd' , signal, opts);
    feature_alpha_bp = jfeeg('bpa' , signal, opts);
    feature_beta_bp = jfeeg('bpb' , signal, opts);
    feature_gamma_bp = jfeeg('bpg' , signal, opts);

    % Max Slope
    feature_max_slope = max(abs(gradient(signal)));

    feature_vector = [featue_abs_min, ...
                        featue_abs_max, ...
                        featue_entropy, ...
                        feature_dalta_bp, ...
                        feature_alpha_bp, ...
                        feature_beta_bp, ...
                        feature_gamma_bp, ...
                        feature_max_slope];

end