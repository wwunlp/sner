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

outputfile = 'trainingResults_ranforest3.csv'

# write new file if it doesn't exist
if not os.path.isfile(outputfile):
    output = open(outputfile, 'w')
    output.write("n_est, depth, bootstrap, max features, min weight, min samples, Train Error, MSE, MAE, Score\n")
    output.close()

def runModel(hyperparams):
    #print(hyperparams)
    n_est = hyperparams['n_est']
    depth = hyperparams['depth']
    bootstrap = hyperparams['bootstrap']
    max_features = hyperparams['max_features']
    min_weight = hyperparams['min_weight_fraction_leaf']
    min_samples = hyperparams['min_samples_leaf']
    model = RandomForestClassifier(n_estimators=n_est, max_depth = depth, verbose = 0,
                                  n_jobs=-1, bootstrap=bootstrap, max_features=max_features,
                                  min_weight_fraction_leaf=min_weight, min_samples_leaf=min_samples)
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
    print( "Accuracy : %.5f" % acc)
    print( "Precision : %.4f" % (sum(prec) / len(prec)))
    print(prec)
    print( "Recall : %.4f" % (sum(recall) / len(recall)))
    print(recall)
    result = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(n_est, depth, bootstrap,
                                                                max_features, min_weight, min_samples,
                                                                trainMSE, devMSE, devMAE, score)
    
    output = open(outputfile, 'a')
    output.write(result)
    output.close()
    
    #A = numpy.loadtxt("data/features_test.sparseX", ndmin=2)
    #I = A[:, 0]
    #J = A[:, 1]
    #data = A[:, 2]
    #testX = coo_matrix((data, (I, J)))

    #prediction = model.predict(testX)
    #numpy.savetxt("predictions.txt", prediction, fmt='%.5f')



hyperparams = {
    'n_est' : 500, # : random.randrange(30, 500,step=10),
    'depth' : 100, # : random.choice([None, random.randrange(1, 200, step=1)]),
    'bootstrap' : False, # : random.choice([True, False]),
    'max_features' : 500, # : random.randrange(2000, 15000), #random.choice(['auto', 'sqrt', 'log2', random.randrange(1, 15000)]),
    'min_weight_fraction_leaf' : 0, # : random.choice([0, random.uniform(0.01, 0.5)]),
    'min_samples_leaf' : 1 # : random.choice([1, random.randrange(1, 25, step=1)])
}    
runModel(hyperparams)


#numpy.savetxt("predictions_random_forest.txt", prediction, fmt='%.5f')

#print(A.toarray())





