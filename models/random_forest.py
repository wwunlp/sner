"""Random Forest Model"""
import random
import time
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.metrics import median_absolute_error, precision_score, recall_score
# from classes import Display


def main(config):
    """
    main
    """

    path = config['path']

    print("Reading data")

    feature_count = sum(1 for line in open(path + 'features.KEY', 'r'))

    Y = np.loadtxt(path + 'target_train.RT')
    A = np.loadtxt(path + 'features_train.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    X = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

    print(X.shape)

    devY = np.loadtxt(path + 'target_dev.RT')
    A = np.loadtxt(path + 'features_dev.sparseX', ndmin=2)
    I = A[:, 0]
    J = A[:, 1]
    data = A[:, 2]
    devX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

    print(devX.shape)

    print("Training model")

    cols = {
        'n_est'             : [],
        'criterion'         : [],
        'max_features'      : [],
        'max_depth'         : [],
        'min_samples_split' : [],
        'max_leaf_nodes'    : [],
        'min_samples_leaf'  : [],
        'avg_prec'          : [],
        'prec[1]'           : [],
        'prec[2]'           : [],
        'avg_recall'        : [],
        'recall[0]'         : [],
        'recall[1]'         : [],
        'recall[2]'         : []
    }

    output = pd.DataFrame(data=cols)

    hyperparams = {
        'n_est' : random.randrange(30, 500, step=10),
        'criterion' : random.choice(['gini', 'entropy']),
        'max_features' :
            random.choice([
                None,
                'auto',
                'sqrt',
                'log2',
                random.randrange(100, 999)
            ]),
        'max_depth' : random.choice([None, random.randrange(3, 100, step=1)]),
        'min_samples_split' : random.randrange(1, 25, step=1),
        'max_leaf_nodes' :
            random.choice([
                None,
                random.randrange(50, 500, step=1)
            ]),
        'min_samples_leaf' : random.choice([1, random.randrange(1, 25, step=1)])
    }

    criterion = hyperparams['criterion']
    max_features = hyperparams['max_features']
    max_depth = hyperparams['max_depth']
    min_samples_split = hyperparams['min_samples_split']
    max_leaf_nodes = hyperparams['max_leaf_nodes']
    min_samples_leaf = hyperparams['min_samples_leaf']
    n_est = hyperparams['n_est']

    model = RandomForestClassifier(
        n_estimators=n_est,
        criterion=criterion,
        max_features=max_features,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        max_leaf_nodes=max_leaf_nodes,
        n_jobs=-1,
        verbose=0,
        min_samples_leaf=min_samples_leaf
    )

    model.fit(X, Y)


    prediction = model.predict(X)
    trainMSE = mean_squared_error(Y, prediction)
    print("Train Error: %.3f" % trainMSE)

    prediction = model.predict(devX)
    devMSE = mean_squared_error(devY, prediction)
    devMAE = median_absolute_error(devY, prediction)
    score = model.score(devX, devY)
    acc = accuracy_score(devY, prediction)
    prec = precision_score(devY, prediction, average=None)
    recall = recall_score(devY, prediction, average=None)
    avg_prec = (sum(prec) / len(prec))
    avg_recall = (sum(recall) / len(recall))
    print("Accuracy : %.5f" % acc)
    print("Precision : %.4f" % avg_prec)
    print(prec)
    print("Recall : %.4f" % avg_recall)
    print(recall)

    output.loc[1, 'n_est'] = n_est
    output.loc[1, 'criterion'] = criterion
    output.loc[1, 'max_features'] = max_features
    output.loc[1, 'max_depth'] = max_depth
    output.loc[1, 'min_samples_split'] = min_samples_split
    output.loc[1, 'max_leaf_nodes'] = max_leaf_nodes
    output.loc[1, 'min_samples_feaf'] = min_samples_leaf
    output.loc[1, 'avg_prec'] = avg_prec
    output.loc[1, 'prec[0]'] = prec[0]
    output.loc[1, 'prec[1]'] = prec[1]
    output.loc[1, 'prec[2]'] = prec[2]
    output.loc[1, 'avg_recall'] = avg_recall
    output.loc[1, 'recall[0]'] = recall[0]
    output.loc[1, 'recall[1]'] = recall[1]
    output.loc[1, 'recall[2]'] = recall[2]

    file_name = "rdf_{}_output.csv".format(time.strftime('%Y%m%d_%H%M'))
    output_path = path + file_name
    output.to_csv(path_or_buf=output_path)
