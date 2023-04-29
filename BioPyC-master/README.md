# __BioPyC__

## An  open-source  python  platform  for  offline EEG and Bio signals decoding and analysis !

This application enables users to easily go through the following steps : 
- __Reading__ EEG and physiological signals (.gdf, .mat)
- __Filtering__ EEG signals (CSP, FBCSP, etc)
- __Classifying__ the signals (NN, Riemannian Geometry methods for EEG signals, LDA for both EEG and physiologicals signals)
- __Evaluating__ the algorithms by obtaining classification performances, for a given data set (classification accuracy, CV, etc)
- __Visualizing__ classification performances (barplots, boxplots, etc)
- __Statistical testing__ classification performances (1 & 2-ways RM-ANOVA)

BioPyC offers a unique interface to quickly create ML models and compare both EEG and physiological signals-based classifiers without any coding. 

## <font color = green> Python librairies (dependencies): </font>
- Python 3.5
- MNE (version 0.17 !! "pip3 install mne==0.17")
- scikit learn ("pip3 install sklearn")
- Jupyter Notebook ("pip3 install jupyter")
- Voila ("pip3 install voila")
- numpy ("pip3 install numpy")
- pandas ("pip3 install pandas")
- pingouin ("pip3 install pingouin")
- skfeature ("pip3 install skfeature-chappers")

Specific to phyiological signals (heart rate, EDA, ECG):
- pywt ("pip3 install PyWavelets")
- biosppy ("pip3 install biosppy")
- neurokit ("pip3 install neurokit")
- nolds (pip install 'nolds<0.5' --force-reinstall) -> you might get conflits with neurokit

## <font color = orange> 0 - Before to start using BioPyC </font>

#### <font color = orange> Download BioPyC in local on you computer </font>
Use "git clone" or the download the library on you computer.
- [optional] Go to the BioPyC folder on your computer
- [optional] Create a virtual environement to install all dependencies:
- [optional] Terminal: "python3 -m venv env_biopyc" 
- [optional] Terminal: "source env_biopyc/bin/activate"
- [optional] Terminal: "pip3 install mne==0.17 scikit-learn jupyter voila numpy pandas pingouin skfeature-chappers PyWavelets biosppy neurokit"
- [otpional] Terminal: "pip3 install 'nolds<0.5' --force-reinstall" 

#### <font color = green> Data storing: </font>
Then, you have to create three empty folders in "data_store". The first one "preprocessed_datasets", and the second "rawdata_datasets", are needed in order to place your dataset in one of these two data stores, based on the type of you data (preprocessed vs raw).
The third and last one will be called "results", in order to store your results later. Then, in "results", create a folder named after your dataset (ex: "bci_competition_4_dataset_2a"). In this new folder, create 3 subfolders, i.e., "figures", "subject_specific" and "subject_independent". In the subject_specific one, create 2 subfolders : "selected_features" and "selected_passbands".

## <font color = orange> 1 - Load the application</font>
BioPyC initializes all parameters that will then be updated by following the different steps of the BCI process bellow, i.e., reading data, pre-processing, signals processing & classification, performing data visualization and statistical tests.

## <font color = orange> 2 - Type of data/signals</font>

__A - Signals types__

Choose the type of data you would like to work on:
- __EEG signals__ this option will lead to study signals with algorithms for EEG signals
- __physiological signals__ this option will lead to study signals with algorithms for physiological signals (Heart Rate, breathing or Electrodermal Activity)
- __EEG and physiological signals__ this option will lead to study a combination of both EEG and physiological signals with algorithms made for it
- 

__B - Data types__

Choose the type of data you would like to work on:
- __raw data__ data that need to be pre-processed (=bandpassing, artifacts cleaning, epoching, etc) before to apply any algorithms on it.   
Your data set should be stored in "BioPyC/data_store/rawdata_datasets/"
- __preprocessed data__  data that have been preprocessed and saved as is. 
Your data set should be stored in "BioPyC/data_store/preprocessed_datasets/"

## <font color = orange> 3 - Reading the dataset</font>

#### Choose the dataset
This first step allows you to read data from a folder you previously slipped into the data store. You will find your folder by running the code below. 

The architecture of this folder has to be the following :
- __folder name__: name of your study. For example, if you want to analyze the "BCI competition IV dataset a", call it "bci_competition_4_dataset_a"
- __subfolders names__: names of the subjects. Ex : "subject_1", "subject_2", etc
- __files__: each subfolder, corresponding to each subject data, contains all files for this subject, each file being the data band passed in a particular frequency band. Ex : data band passed in a [8,12] Hz frequency band. 

Finally we have this tree structure : __example - data_store/EEG_data/raw_data/bci_competition_IV_dataset_a/subject_1/[8,12].mat__  

*NB If .mat format: we consider that the matlab structure header starts by "EEG". Feel free to change it /src/data/data_readers/mat.py*


## <font color = orange> 4 - Define Parameters</font>

#### A - Raw data: pre-processing parameters 

If your dataset contains raw signals, you have to specify some parameters for the pre-processing. 
- __list of subjects to keep__: list containing integers of the subjects you wan to keep (Ex: [1, 2, 3])
- __list of sessions__: list containing integers of the sessions (Ex: [1, 2]).  <font color = red>Have to be specified in each file name.</font>
- __list of runs__: list containing integers of the runs (Ex: [1,2,3,4]).  <font color = red>Have to be specified in each file name.</font>
- __t min__: start time window signal, can be before/after the stimulation (Ex: -2.5 for 2,5 sec before stimulation)
- __t max__: stop time window signal, can be before/after the stimulation (Ex: 0.5 for 0,5 sec after stimulation)
- __list of all channels__: list of channels ['channel_1', 'channels_2', etc]
- __list of EOG channels__: list of EOG channels ['eog_1', 'eog_2', etc]
- __list of channels to drop__: list of channels to drop ['unnamed_1', 'unnamed_2', etc]
