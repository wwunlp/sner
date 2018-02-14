"""Launcher for scikit-learn models"""
import time
import numpy as np
import pandas as pd
from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.metrics import median_absolute_error, precision_score, recall_score
from scipy.sparse import coo_matrix
import random
import os.path

def dec_model(params):
    """Initiates model as decision tree classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.tree.DecisionTreeClassifer): Selected model.

    Raises:
        None
    """

    if (params['random']):
        print("Random Decision Tree Parameters.")
        params['criterion'] = random.choice(["gini", "entropy"])
        params['splitter'] = random.choice(["best", "random"])
        params['max_features'] = random.choice(['auto', 'sqrt', 'log2', random.randrange(50, 1000, step=25), None])
        params['max_depth'] =  random.choice([None, random.randrange(5, 1000, step=5)])
        params['min_samples_split'] = random.choice([2, random.randrange(1, 50, step=1)])
        params['max_leaf_nodes'] = random.choice([None, random.randrange(2, 50, step=1)])
        params['min_samples_leaf'] = random.choice([1, random.randrange(5, 100, step=5)])
        print(params)
        
    model = tree.DecisionTreeClassifier(
        criterion=params['criterion'],
        splitter=params['splitter'],
        max_features=params['max_features'],
        max_depth=params['max_depth'],
        min_samples_split=params['min_samples_split'],
        max_leaf_nodes=params['max_leaf_nodes'],
        min_samples_leaf=params['min_samples_leaf']
    )

    return model



def forest_model(params):
    """Initiates model as Extra Trees Classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.naive_bayes.MultinomialNB): Selected model.

    Raises:
        None
    """
    if (params['random']):
        params['n_estimators'] = random.choice([1, 3, 5, 10, 20, 30, 40, 50, 75, 100])
    model = ExtraTreesClassifier(
        n_estimators=params['n_estimators'],
        random_state=0
    )

    return model



def nbc_model(params):
    """Initiates model as multinomial Naive Bayes classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.naive_bayes.MultinomialNB): Selected model.

    Raises:
        None
    """
    if (params['random']):
        params['alpha'] = random.randrange(1, 10, step=1) * 0.1
    model = MultinomialNB(
        alpha=params['alpha']
    )

    return model


def rdf_model(params):
    """Initiates model as random forest classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.ensemble.RandomForestClassifer): Selected model.

    Raises:
        None
    """

    if (params['random']):
        print("Random Decision Tree Parameters.")
        params['criterion'] = random.choice(["gini", "entropy"])
        params['max_features'] = random.choice(['auto', 'sqrt', 'log2', random.randrange(50, 1000, step=25), None])
        params['max_depth'] =  random.choice([None, random.randrange(5, 1000, step=5)])
        params['min_samples_split'] = random.choice([2, random.randrange(1, 50, step=1)])
        params['max_leaf_nodes'] = random.choice([None, random.randrange(2, 50, step=1)])
        params['min_samples_leaf'] = random.choice([1, random.randrange(5, 100, step=5)])
        params['n_estimators'] = random.choice([1, 3, 5, 10, 20, 30, 40, 50, 75, 100])
        print(params)
        
    model = RandomForestClassifier(
        criterion=params['criterion'],
        max_features=params['max_features'],
        max_depth=params['max_depth'],
        min_samples_split=params['min_samples_split'],
        max_leaf_nodes=params['max_leaf_nodes'],
        min_samples_leaf=params['min_samples_leaf'],
        n_estimators=params['n_estimators'],
        verbose=0
    )

    return model


def sgd_model(params):
    """Initiates model as linear classifier with stochastic gradient descent.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.linear_model.SGDClassifer): Selected model.

    Raises:
        None
    """

    
    if (params['random']):
        params['loss'] = random.choice(['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'])
        params['penalty'] = random.choice(['none', 'l2', 'l1', 'elasticnet'])
        params['alpha'] = random.choice([0.001, 0.0001, 0.00001])
    model = SGDClassifier(
        loss=params['loss'],
        penalty=params['penalty'],
        alpha=params['alpha']
    )

    return model


def svc_model(params):
    """Initiates model as c-support vector classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.svm.SVC): Selected model.

    Raises:
        None
    """

    if (params['random']):
        params['C'] = random.randrange(1, 13, step=1) * 0.1
        params['degree'] = random.choice([2, 3, 4, 5])
        params['kernel'] = random.choice(['linear', 'rbf', 'poly', 'sigmoid'])
        
    model = svm.SVC(
        decision_function_shape='ovo',
        C=params['C'],
        degree=params['degree'],
        kernel=params['kernel']
    )

    return model


def main(config):
    """Load and train a scikit-learn model as specified by the user in configs
    or command line arguments.  Test the models performance after training and
    then print performance information (precision, accuracy, recall).

    Args:
        config (dict): Configuration flags and values.

    Returns:
        None

    Raises:
        None
    """

    runModel(config)
    while (config['looping']):
        runModel(config)

def runModel(config):

    model_name = config['run']
    params = config['params']
    path = config['path']
    use_atf = config['flags']['use_atf']
    use_test = config['eval-test']

    if use_atf:
        print("Exporting ATF prediction.")
    
    output_path = path + "{}_{}_training_results.csv".format(
        model_name,
        time.strftime('%Y%m%d_%H%M')
    )


	
    #read the input data per the configuration information

    if (config['output-file'] != None):
        output_path = config['output-file']

    print("Reading data")
    feature_count = sum(1 for line in open(path + 'features.KEY', 'r'))

    Y = np.loadtxt(path + 'target_train.RT')
    A = np.loadtxt(path + 'features_train.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    X = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))


    devY = np.loadtxt(path + 'target_dev.RT')
    A = np.loadtxt(path + 'features_dev.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    devX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

    testX = None
    testY = None    
    if use_test:
            testY = np.loadtxt(path + 'target_test.RT')            
            A = np.loadtxt(path + 'features_test.sparseX', ndmin=2)
            I = A[:, 0]
            J = A[:, 1]
            data = A[:, 2]

            testX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))
    
    atfX = None
    if use_atf:
        A = np.loadtxt(path + 'features_atf.sparseX', ndmin=2)
        I = A[:, 0]
        J = A[:, 1]
        data = A[:, 2]
        atfX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))
	
    print("Training model")

	#select the model based on the configuration data
    if model_name == 'dec':
        model = dec_model(params)
    elif model_name == 'nbc':
        model = nbc_model(params)
    elif model_name == 'rdf':
        model = rdf_model(params)
    elif model_name == 'sgd':
        model = sgd_model(params)
    elif model_name == 'svc':
        model = svc_model(params)
    elif model_name == 'forest':
        model = forest_model(params)

	#train the model on the annotated data
    model.fit(X, Y)

    prediction = model.predict(X)
    trainMSE = mean_squared_error(Y, prediction)
    print("Train Error: {:.3f}".format(trainMSE))

	#generate predictions based off of the model, and evaluate its performance
    prediction = model.predict(devX)
    devMSE = mean_squared_error(devY, prediction)
    devMAE = median_absolute_error(devY, prediction)
    score = model.score(devX, devY)
    acc = accuracy_score(devY, prediction)
    prec = precision_score(devY, prediction, average=None)
    recall = recall_score(devY, prediction, average=None)
    avg_prec = (sum(prec) / len(prec))
    avg_recall = (sum(recall) / len(recall))
    print("Acc: %.5f Prec: %.4f Recall: %.4f"%(acc, avg_prec, avg_recall))
    #print("Precision: {:.4f}".format(avg_prec))
    #print(prec)
    #print("Recall: {:.4f}".format(avg_recall))
    #print(recall)

	#output results, if use_atf is not set then output a .csv file
    if not use_atf:
        data = params
        data.update({
        'avg_prec': avg_prec,
            'prec[0]': prec[0],
            'prec[1]': prec[1],
            'prec[2]': prec[2],
            'avg_recall': avg_recall,
            'recall[0]': recall[0],
            'recall[1]': recall[1],
            'recall[2]': recall[2]
        })

        useHeader = True
        if (os.path.isfile(output_path)):
            useHeader = False
        
        with open(output_path, 'a') as f:
            output = pd.DataFrame(data, index=[1])
            output.to_csv(f, header=useHeader)

    np.savetxt(
        path + 'dev_prediction.RT',
        prediction,
        delimiter=',',
        fmt='%d'
    )


    #if use_test is set, then evaluate test data as well
    if use_test:
        print("Evaluating on test dataset...")
        prediction = model.predict(testX)
        testMSE = mean_squared_error(testY, prediction)
        testMAE = median_absolute_error(testY, prediction)
        score = model.score(testX, testY)
        acc = accuracy_score(testY, prediction)
        prec = precision_score(testY, prediction, average=None)
        recall = recall_score(testY, prediction, average=None)
        avg_prec = (sum(prec) / len(prec))
        avg_recall = (sum(recall) / len(recall))
        print("Score: %.5f MSE: %.5f MAE: %.5f "% (score, testMSE, testMAE))
        print("Acc: %.5f Prec: %.4f Recall: %.4f"%(acc, avg_prec, avg_recall))
        print("Precision: %.5f, %.5f, %.5f (NotName, PN, GN)"%(prec[0], prec[1], prec[2]))
        print("Recall: %.5f, %.5f, %.5f (NotName, PN, GN)"%(recall[0], recall[1], recall[2]))

    #if use_atf is set, then output a .atf file containing the results        
    if use_atf:
        print("Predicting...")
        atf_prediction = model.predict(atfX)
        print("Saving...")
        np.savetxt(
            path + 'atf_prediction.RT',
            atf_prediction,
            delimiter=',',
            fmt='%d'
        )


    #export image of the tree if the decision tree model was used and not using random params
    if model_name == 'dec' and params['random'] == False:
        with open(path + 'decModel.dot', 'w') as f:
            with open(path + 'features.KEY', 'r') as f2:
                feature_labels = f2.read().splitlines()
                class_labels = (
                    'NotName',
                    'PersonalName',
                    'GeoName'
                )
                f = tree.export_graphviz(
                    model,
                    out_file=f,
                    feature_names=feature_labels,
                    class_names=class_labels
                )

    if model_name == 'forest':
        importances = model.feature_importances_
        std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
        indices = np.argsort(importances)[::-1]
        with open('FeatureRankings.txt', 'w') as feats:
            feats.write("Feature ranking:\n")
            with open(path + 'features.KEY', 'r') as f2:
                feature_labels = f2.read().splitlines()
                for f in range(X.shape[1]):
                    feats.write("%d. feature %d (%f) [%s]\n" % (f + 1, indices[f], importances[indices[f]], feature_labels[f]))
