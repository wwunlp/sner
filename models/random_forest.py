from scipy.sparse import coo_matrix
import numpy
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, median_absolute_error, accuracy_score, recall_score, precision_score
import random
import os.path

print("Reading data")


feature_count = sum(1 for line in open("data/features.KEY", "r"))



Y = numpy.loadtxt("data/target_train.RT")
A = numpy.loadtxt("data/features_train.sparseX", ndmin=2)
I = A[:, 0]
J = A[:, 1]
data = A[:, 2]
X = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))

print (X.shape)

devY = numpy.loadtxt("data/target_dev.RT")
A = numpy.loadtxt("data/features_dev.sparseX", ndmin=2)
I = A[:, 0]
J = A[:, 1]
data = A[:, 2]
devX = coo_matrix((data, (I, J)), shape=(int(max(I))+1, feature_count))


print (devX.shape)

print("Training model")

outputfile = 'trainingResults_randomforest.csv'

# write new file if it doesn't exist
if not os.path.isfile(outputfile):
    output = open(outputfile, 'w')
    output.write("n_est, criterion, max_features, max_depth, min_samples_split, max_leaf_nodes, min_samples_leaf, avg_prec, prec[0], prec[1], prec[2], avg_recall, recall[0], recall[1], recall[2]\n")
    
    output.close()

def runModel(hyperparams):
    #print(hyperparams)

    criterion = hyperparams['criterion']
    max_features = hyperparams['max_features']
    max_depth = hyperparams['max_depth']
    min_samples_split = hyperparams['min_samples_split']
    max_leaf_nodes = hyperparams['max_leaf_nodes']
    min_samples_leaf = hyperparams['min_samples_leaf']                    
    n_est = hyperparams['n_est']
    
    model = RandomForestClassifier(n_estimators=n_est,
                                   criterion=criterion,                                   
                                   max_features=max_features,
                                   max_depth=max_depth,
                                   min_samples_split=min_samples_split,
                                   max_leaf_nodes=max_leaf_nodes,
                                   n_jobs=-1,
                                   verbose=0,
                                   min_samples_leaf=min_samples_leaf)

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
    result = result.format(n_est, criterion,
                           max_features, max_depth, min_samples_split,
                           max_leaf_nodes, min_samples_leaf,                             
                           avg_prec, prec[0], prec[1], prec[2],
                           avg_recall, recall[0], recall[1], recall[2])
    

    output = open(outputfile, 'a')
    output.write(result)
    output.close()


    numpy.savetxt('data/dev_prediction.RT', prediction, delimiter=',',fmt='%d')
    
    #A = numpy.loadtxt("data/features_test.sparseX", ndmin=2)
    #I = A[:, 0]
    #J = A[:, 1]
    #data = A[:, 2]
    #testX = coo_matrix((data, (I, J)))

    #prediction = model.predict(testX)
    #numpy.savetxt("predictions.txt", prediction, fmt='%.5f')



def genHyper():
    hyperparams = {
        'n_est' : 480, #random.randrange(30, 500, step=10),
        'criterion' : 'entropy', #random.choice(['gini', 'entropy']),
        'max_features' : None, #random.choice([None, 'auto', 'sqrt', 'log2', random.randrange(100, 999)]),
        'max_depth' : None, #random.choice([None, random.randrange(3, 100, step=1)]),
        'min_samples_split' : 4, #random.randrange(1, 25, step=1),
        'max_leaf_nodes' : None, #random.choice([None, random.randrange(50, 500, step=1)]),        
        'min_samples_leaf' : 1 #random.choice([1, random.randrange(1, 25, step=1)])
        }
    return hyperparams


#while True:
runModel(genHyper())




