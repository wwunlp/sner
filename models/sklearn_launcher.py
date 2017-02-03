"""Launcher for scikit-learn models"""
import time
import numpy as np
import pandas as pd
from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.metrics import median_absolute_error, precision_score, recall_score
from scipy.sparse import coo_matrix


def dec_model(params):
    """Initiates model as decision tree classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.tree.DecisionTreeClassifer): Selected model.

    Raises:
        None
    """

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


def nbc_model(params):
    """Initiates model as multinomial Naive Bayes classifier.

    Args:
        params (dict): Dictionary of hyperparameters.

    Returns:
        model (sklearn.naive_bayes.MultinomialNB): Selected model.

    Raises:
        None
    """

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

    model = svm.SVC(
        decision_function_shape='ovo',
        C=params['C'],
        degree=params['degree'],
        kernel=params['kernel']
    )

    return model


def main(config):
    """Load and train scikit-learn models.

    Args:
        config (dict): Configuration flags and values.

    Returns:
        None

    Raises:
        None
    """

    model_name = config['run']
    params = config['params']
    path = config['path']
    output_path = path + "{}_{}_training_results.csv".format(
        model_name,
        time.strftime('%Y%m%d_%H%M')
    )

    print("Reading data")

    feature_count = sum(1 for line in open(path + 'features.KEY', 'r'))

    Y = np.loadtxt(path + 'target_train.RT')
    A = np.loadtxt(path + 'features_train.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    X = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

    print (X.shape)

    devY = np.loadtxt(path + 'target_dev.RT')
    A = np.loadtxt(path + 'features_dev.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    devX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

    A = np.loadtxt(path + 'features_atf.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    atfX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

    print(devX.shape)
    print(atfX.shape)

    print("Training model")

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

    model.fit(X, Y)

    prediction = model.predict(X)
    trainMSE = mean_squared_error(Y, prediction)
    print("Train Error: {:.3f}".format(trainMSE))

    prediction = model.predict(devX)
    devMSE = mean_squared_error(devY, prediction)
    devMAE = median_absolute_error(devY, prediction)
    score = model.score(devX, devY)
    acc = accuracy_score(devY, prediction)
    prec = precision_score(devY, prediction, average=None)
    recall = recall_score(devY, prediction, average=None)
    avg_prec = (sum(prec) / len(prec))
    avg_recall = (sum(recall) / len(recall))
    print("Accuracy: {:.5f}".format(acc))
    print("Precision: {:.4f}".format(avg_prec))
    print(prec)
    print("Recall: {:.4f}".format(avg_recall))
    print(recall)

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

    output = pd.DataFrame(data, index=[1])
    output.to_csv(path_or_buf=output_path)

    atf_prediction = model.predict(atfX)
    np.savetxt(
        path + 'atf_prediction.RT',
        atf_prediction,
        delimiter=',',
        fmt='%d'
    )

    if model_name == 'dec':
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
