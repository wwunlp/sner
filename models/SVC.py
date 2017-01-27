from scipy.sparse import coo_matrix
import numpy
from sklearn import datasets
from sklearn import tree
from sklearn import svm
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

outputfile = 'trainingResults_SVC.csv'

# write new file if it doesn't exist
if not os.path.isfile(outputfile):
    output = open(outputfile, 'w')
    output.write("kernel, C, degree, avg_prec, prec[0], prec[1], prec[2], avg_recall, recall[0], recall[1], recall[2]\n")
    output.close()

def runModel(hyperparams):
    #print(hyperparams)
    kernel = hyperparams['kernel']
    c = hyperparams['C']
    degree = hyperparams['degree']
    model = svm.SVC (decision_function_shape='ovo', C=c, degree=degree, kernel=kernel)
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
    result = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(kernel, c, degree,
                                                                avg_prec, prec[0], prec[1], prec[2],
                                                                avg_recall, recall[0], recall[1], recall[2]                                                                
                                                                )
    
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


def genHyper():
    hyperparams = {
        'kernel' : random.choice(['linear', 'rbf']),
        'C' : random.uniform(0.3, 1.3),
        'degree' : random.choice([2, 3]),        
    }
    return hyperparams

while True:
    runModel(genHyper())


#numpy.savetxt("predictions_random_forest.txt", prediction, fmt='%.5f')

#print(A.toarray())





