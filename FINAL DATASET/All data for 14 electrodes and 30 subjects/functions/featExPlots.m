
% lengths of variables:
nDataSets = 2;  % guilty, honest
nVars = 3;      % probe, target, irrelevant
nVals = 10;      % how many random sessions did we take? (1 means we took the feature of one signal)


% input data to be a vector containing all feature lists
% col1 = lying probe
% col2 = lying target
% ...
data = rand(nVals*nVars*nDataSets,1);


%% box chart

% Create column vector to indicate dataset
dataSet = categorical([ones(nVars*nVals,1); ...
    ones(nVars*nVals,1)*2]);
dataSet = renamecats(dataSet,{'Guilty', 'Honest'});
% Create column vector to indicate the variable
clear var
var(1:nVals,1) = "Var1";
var(end+1:end+nVals,1) = "Var2";
var(end+1:end+nVals,1) = "Var3";
Var = categorical([var;var]);
% Create a table
testData = table(data,dataSet,Var);

% Actual visualization code using boxchart
boxchart(testData.dataSet,testData.data,"GroupByColor",testData.Var)
legend(["Probe","Target", "Irrelevant"],'Location','bestoutside','Orientation','vertical')
title('Features of 10 Random Subjects')
grid on






