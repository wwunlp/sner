"""Launcher for scikit-learn models"""
import time
import os.path
import numpy as np
from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.metrics import median_absolute_error, precision_score, recall_score
from scipy.sparse import coo_matrix


def dec_model(hyperparams):
    """
    dec
    """

    model = tree.DecisionTreeClassifier(
        criterion=hyperparams['criterion'],
        splitter=hyperparams['splitter'],
        max_features=hyperparams['max_features'],
        max_depth=hyperparams['max_depth'],
        min_samples_split=hyperparams['min_samples_split'],
        max_leaf_nodes=hyperparams['max_leaf_nodes'],
        min_samples_leaf=hyperparams['min_samples_leaf']
    )

    return model


def nbc_model(hyperparams):
    """
    nbc
    """

    mn_model = MultinomialNB(alpha=alpha)
    ber_model = BernoulliNB(alpha=alpha, binarize=binarize)

    return mn_model, ber_model


def rdf_model(hyperparams):
    """
    rdf
    """

    model = RandomForestClassifier(
        criterion=hyperparams['criterion'],
        max_features=hyperparams['max_features'],
        max_depth=hyperparams['max_depth'],
        min_samples_split=hyperparams['min_samples_split'],
        max_leaf_nodes=hyperparams['max_leaf_nodes'],
        min_samples_leaf=hyperparams['min_samples_leaf'],
        n_est=hyperparams['n_est'],
        verbose=0
    )

    return model


def sgd_model(hyperparams):
    """
    sgd
    """

    model = SGDClassifier(
        loss=loss,
        penalty=penalty,
        alpha=alpha
    )

    return model


def svc_model(hyperparams):
    """
    svc
    """

    model = svm.SVC(
        decision_function_shape='ovo',
        C=c,
        degree=degree,
        kernel=kernel
    )

    return model


def main(config, sklearn_model):
    """
    main
    """

    path = config['path']
    output_path = path + "{}_{}_training_results.csv".format(
        sklearn_model,
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

    print (devX.shape)
    print(atfX.shape)

    print("Training model")

    hyperparams = {
        'criterion'        : 'gini',
        'splitter'         : 'best',
        'max_features'     : None,
        'max_depth'        : None,
        'min_samples_split': 2,
        'max_leaf_nodes'   : None,
        'min_samples_leaf' : 1,
    }




# write new file if it doesn't exist
    if not os.path.isfile(output_path):
        output = open(output_path, 'w')
        output.write("criterion, splitter, max_features, max_depth, min_samples_split, max_leaf_nodes, min_samples_leaf, avg_prec, prec[0], prec[1], prec[2], avg_recall, recall[0], recall[1], recall[2]\n")

        output.close()

    model = dec_model(hyperparams)

    model.fit(X, Y)
    

    prediction = model.predict(X)
    trainMSE = mean_squared_error(Y, prediction)
    print( "Train Error: %.3f" % trainMSE)
    
    prediction = model.predict(devX)
    devMSE = mean_squared_error(devY, prediction)
    devMAE = median_absolute_error(devY, prediction)
    score = model.score(devX, devY)
    acc = accuracy_score(devY, prediction)
    prec = precision_score(devY, prediction, average=None)
    recall = recall_score(devY, prediction, average=None)
    avg_prec = (sum(prec) / len(prec))
    avg_recall = (sum(recall) / len(recall))
    print( "Accuracy : %.5f" % acc)
    print( "Precision : %.4f" % avg_prec)
    print(prec)
    print( "Recall : %.4f" % avg_recall)
    print(recall)
    
    result = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n'
    result = result.format(criterion, splitter,
                           max_features, max_depth, min_samples_split,
                           max_leaf_nodes, min_samples_leaf,                             
                           avg_prec, prec[0], prec[1], prec[2],
                           avg_recall, recall[0], recall[1], recall[2])
    
    
    output = open(outputfile, 'a')
    output.write(result)
    output.close()


    atf_prediction = model.predict(atfX)
    np.savetxt('data/atf_prediction.RT', atf_prediction, delimiter=',',fmt='%d')
