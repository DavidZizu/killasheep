import pickle
from sklearn.preprocessing import StandardScaler
from transform_data import transform_data
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


MODEL_NAME = 'MLPClassifier'


if __name__=='__main__':
	# Load train and test data
	print 'Uploading datasets...'
	X_train, Y_train = transform_data('train_split/')
	X_test, Y_test = transform_data('test_split/')


        X = list(X_train) + list(X_test)

        q = StandardScaler()
        q.fit(X)

        with open('scaler.pkl', 'wb') as f:
        	f.write(pickle.dumps(q))

        X = q.transform(X)

        X_train, X_test = X[:len(X_train)], X[len(X_train):]

        print X_train[0].shape, X_test[0].shape

	print 'Learning on {} elements'.format(len(X_train))
	print 'Predicting on {} elements'.format(len(X_test))


	if MODEL_NAME == 'MLPClassifier':
		model = MLPClassifier(hidden_layer_sizes=(28 * 28, 28 * 28, 28 * 28, 28 * 28, 28 * 28, 100, 100), solver='sgd',  verbose=True, max_iter=6005, alpha=0.005)
	elif MODEL_NAME == 'svc':
		model = SVC(verbose=True)
	elif MODEL_NAME == 'KNeighborsClassifier':
		model = KNeighborsClassifier(n_neighbors=5)
	elif MODEL_NAME == 'GaussianProcessClassifier':
		model = GaussianProcessClassifier()
	elif MODEL_NAME == 'DecisionTreeClassifier':
		model = DecisionTreeClassifier()
	elif MODEL_NAME == 'RandomForestClassifier':
		model = RandomForestClassifier()
	elif MODEL_NAME == 'AdaBoostClassifier':
		model = AdaBoostClassifier()
	elif MODEL_NAME == 'GaussianNB':
		model = GaussianNB()
	elif MODEL_NAME == 'QuadraticDiscriminantAnalysis':
		model = QuadraticDiscriminantAnalysis()
	else:
		print 'Specify the model name'
		exit()



	print 'Training model...'
	model.fit(X_train, Y_train)

	print X_test

	print 'Making predictions...'
	prediction = model.predict(X_test)

	print sum(prediction[i] == Y_test[i] for i in range(len(Y_test))) / float(len(Y_test))

	f = open('models/' + MODEL_NAME + '.pkl', 'wb')
	f.write(pickle.dumps(model))
	f.close()
