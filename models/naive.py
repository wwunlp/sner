from scipy.sparse import coo_matrix
import numpy
from sklearn import datasets
from sklearn import tree
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
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

outputfile = 'trainingResults_NB.csv'

# write new file if it doesn't exist
if not os.path.isfile(outputfile):
    output = open(outputfile, 'w')
    output.write("model, alpha, binarize, avg_prec, prec[0], prec[1], prec[2], avg_recall, recall[0], recall[1], recall[2]\n")
    output.close()

def runModel(hyperparams):
    #print(hyperparams)
    model_type = hyperparams['model']
    alpha = hyperparams['alpha']
    binarize = hyperparams['binarize']
    
    model = MultinomialNB (alpha=alpha)
    if (model_type == 'Bernoulli'):
        model = BernoulliNB (alpha=alpha, binarize=binarize)
    
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
    result = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(model_type, alpha, binarize, 
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
        'model' : random.choice(['Bernoulli', 'Multinomial']),
        'alpha' : random.uniform(0.1, 1.5),
        'binarize' : random.uniform(1, 7)
        
    }
    return hyperparams

while True:
    runModel(genHyper())

def main(data, options):
    """
    main
    """
    pass
