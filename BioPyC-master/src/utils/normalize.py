
import numpy as np
from src.utils import discretizing

def normalize_data(features, labels, mean_features = None, std_features = None):
	'''
	This function is made to shape data using mutal informaiton based algorithms. 
	First, we normalize the features,
	Then we discretize them
	input : 
		- features :  A matrix representing the training feature vectors with associated labels. This matrix is a matrix with size [nT,nF+1] where
				- nT = number of training data
				- nF = number of features (input dimension)
		- nb_features
	output:
		- selected_features
	'''
	features = np.concatenate((features, np.array([labels]).T), axis=1)

	# Defining if it is a test set, or a train set
	if mean_features is None and std_features is None :
		set_type = 'train'
	else:
		set_type = 'test'



	# Normalizing each feature independently (substracting the mean, dividing by the standard deviation)
	nb_training_vectors = np.shape(features)[0]
	labels = features[:,-1]

	if set_type == 'train' :
		mean_features = np.mean(features[:,:-1], axis = 0)
		std_features = np.std(features[:,:-1],axis =0)

	# actual_normalization  (+re-adding the labels)
	train_features = (features[:,:-1] - np.kron(np.ones((nb_training_vectors,1)),mean_features)) / np.kron(np.ones((nb_training_vectors,1)),std_features)
	train_features = np.concatenate((train_features, np.array([labels]).T), axis = 1)


	# Discretising the data set 
	discrete_train_features = discretizing.discretize_dataset(train_features, [2, 0.5])
	if set_type == 'train' : 
		
		return discrete_train_features, mean_features, std_features
	else :
		return discrete_train_features
	# feature selection based on MRMR 
	#train_labels = discrete_train_features[:,-1]



def just_normalize(features, mean_features = None, std_features = None):
	'''
	This function is made to shape data using mutal informaiton based algorithms. 
	First, we normalize the features,
	Then we discretize them
	input : 
		- features :  A matrix representing the training feature vectors with associated labels. This matrix is a matrix with size [nT,nF+1] where
				- nT = number of training data
				- nF = number of features (input dimension)
		- nb_features
	output:
		- selected_features
	'''

	# Defining if it is a test set, or a train set
	if mean_features is None and std_features is None :
		set_type = 'train'
	else:
		set_type = 'test'

	# Normalizing each feature independently (substracting the mean, dividing by the standard deviation)
	nb_training_vectors = np.shape(features)[0]
	labels = features[:,-1]

	if set_type == 'train' :
		mean_features = np.mean(features[:,:-1], axis = 0)
		std_features = np.std(features[:,:-1],axis =0)

	# actual_normalization  (+re-adding the labels)
	train_features = (features[:,:-1] - np.kron(np.ones((nb_training_vectors,1)),mean_features)) / np.kron(np.ones((nb_training_vectors,1)),std_features)
	train_features = np.concatenate((train_features, np.array([labels]).T), axis = 1)


	if set_type == 'train' : 
		
		return train_features, mean_features, std_features
	else :
		return train_features
	# feature selection based on MRMR 
	#train_labels = discrete_train_features[:,-1]