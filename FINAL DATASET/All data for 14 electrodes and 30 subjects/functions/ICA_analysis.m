% Assume you have an EEG data matrix called "eegData" with dimensions [channels x samples]
filepath = '..\data\lying_probe_w_artifacts.mat';
eegData = load(filepath, "subject1_session1");  % Example random EEG data

% Create an EEGLAB-compatible structure
EEG = struct();
EEG.data = eegData;  % EEG data matrix [channels x samples]
EEG.srate = 500;  % Sampling rate in Hz
% EEG.chanlocs = struct();  % Channel locations structure (optional)
EEG.setname = '';



% 
% EEG =
%              setname: 'EEG Data'
%             filename: 'eeglab_data_epochs_ica.set'
%             filepath: filepath
%              subject: ''
%                group: ''
%            condition: ''
%              session: []
%             comments: [9×769 char]
%               nbchan: 14
%               trials: 30
%                 pnts: 
%                srate: 500
%                 xmin: 
%                 xmax: 
%                times: 
%                 data: 
%               icaact: 
%              icawinv: 
%            icasphere: 
%           icaweights: 
%          icachansind: 
%             chanlocs: [1×14 struct]
%           urchanlocs: [1×14 struct]
%             chaninfo: [1×1 struct]
%                  ref: 'common'
%                event: 
%              urevent: 
%     eventdescription: 
%                epoch: 
%     epochdescription: {}
%               reject: [1×1 struct]
%                stats: [1×1 struct]
%             specdata: []
%           specicaact: []
%           splinefile: []
%        icasplinefile: ''
%               dipfit: []
%              history: ''
%                saved: 'yes'
%                  etc: [1×1 struct]
%              datfile: 'eeglab_data_epochs_ica.fdt'
%                  run: []
% 
% 
% 
% 
% 
% 
% 


% Save the structure to a .mat file
save('eeg_data.mat', 'EEG');

