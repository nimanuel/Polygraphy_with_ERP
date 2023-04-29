# -*- coding: utf-8 -*-

"""
"""

# Aurélien Appriou <aurelien.appriou@inria.fr>
# 02/07/2019
# copyright "https://choosealicense.com/licenses/agpl-3.0/" - GNU Affero General Public License


import numpy as np

def discretize_dataset(data_set, alpha):
	'''
	a function to discretize a data set containing continuous feature vectors.
	The discretization is done using mean+/-alpha*std. For instance if alpha =
	[0 1], a given feature will be discretize in four different (integer)
	values (1, 2, 3 and 4), corresponding to continuously values in the ranges
	[-inf, mean-1*std], [mean-1*std, mean(-0*std)], [mean(+0*std), mean+1*std], [mean+1*std, inf].
	
	Input:
	dataSet: 
	   the data set to be discretized, which is a matrix of feature vectors. 
	   this matrix is a matrix with size [nT,nF+1] where
	          nT          = number of data,
	          nF          = number of features (input dimension),
	          lastcol     = class labels (one per data) 
	alpha:
	   the list of thresholds for discretization (see exemple above)
	
	discreteDataSet: 
	   the discretized data set, with values in 1, 2, 3 ... N 
	   with N depending on the number of thresholds alpha (see exemple above)
	'''

	# building the interval list for discrtization
	alpha = np.sort(alpha)[::-1] # sorting alpha in descending order

	if alpha[-1] == 0 :
		alpha = np.concatenate((-alpha[:-1], alpha[::-1]))
	else:
		alpha = np.concatenate((-alpha, alpha[::-1]))

	# Computing the mean and standard deviation for each feature
	features = data_set[:, :-1] # removing the labels
	labels = data_set[:,-1]
	nb_training_vectors = np.shape(features)[0]
	#mean_features = np.mean(features, axis = 0)
	#std_features = np.std(features, axis = 0)

	# normalizing the features
	#features = (features - np.kron(np.ones((nb_training_vectors,1)),mean_features)) / np.kron(np.ones((nb_training_vectors,1)),std_features)

	# starting the discretization 
	current_state = 1
	new_features = np.zeros((np.shape(features)))
	new_features[features[:,:] < alpha[0]] = current_state
	current_state +=1

	for i in range(len(alpha)-1):
		new_features[(features[:,:] >= alpha[i]) & (features[:,:]<alpha[i+1])] = current_state
		current_state+=1
	new_features[features[:,:] >= alpha[-1]] = current_state

	discret_data_set = np.concatenate((new_features, np.array([labels]).T), axis = 1) 
	
	discret_data_set = discret_data_set.astype(int)


	return discret_data_set








