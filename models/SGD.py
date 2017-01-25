from scipy.sparse import coo_matrix
import numpy
from sklearn import datasets
from sklearn import tree
from sklearn.linear_model import SGDClassifier
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

outputfile = 'trainingResults_SGD.csv'

# write new file if it doesn't exist
if not os.path.isfile(outputfile):
    output = open(outputfile, 'w')
    output.write("loss, penalty, alpha, avg_prec, prec[0], prec[1], prec[2], avg_recall, recall[0], recall[1], recall[2]\n")
    output.close()

def runModel(hyperparams):
    #print(hyperparams)
    loss = hyperparams['loss']
    penalty = hyperparams['penalty']
    alpha = hyperparams['alpha']
    model = SGDClassifier (loss=loss, penalty=penalty, alpha=alpha)
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
    result = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(loss, penalty, alpha,
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
        'loss' : random.choice(['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive']),
        'penalty' : random.choice(['l2', 'l1', 'none', 'elasticnet']),
        'alpha' : random.uniform(0.00001, 0.01)    
    }
    return hyperparams

while True:
    runModel(genHyper())


#numpy.savetxt("predictions_random_forest.txt", prediction, fmt='%.5f')

#print(A.toarray())





