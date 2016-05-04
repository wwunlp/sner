#!/usr/bin/python3


#       dictionaries of monograms, bigrams, and trigrams
#format is a name key, associated with a two element list containing the number of occurences of that gram
#the first element is number of occurences of that gram in total, the second is number of occurences within names

from collections import defaultdict

monograms = defaultdict(list)
bigrams = defaultdict(list)
trigrams = defaultdict(list)

#       utility functions to insert grams into maps
    
#isName takes one if it is a name, zero otherwise
def addMonogram(gram, isName):
    list = monograms[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[isName] += 1

def addBigram(gram, isName):
    list = bigrams[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[isName] += 1

def addTrigram(gram, isName):
    list = trigrams[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[isName] += 1


#       xml parser to fetch names from the xml file and harvest the grams
#not sure how to do this for format reasons



#       collect percentage statistics from the gram maps
#probably should be written to a file?

def analyzeData():
    print('monogram analysis')
    for k,v in monograms.items():
        outputAnalysis(k,v)
    if len(monograms) <= 0:
        print("no monograms")


    print('\nbigram analysis')
    for k,v in bigrams.items():
        outputAnalysis(k,v)
    if len(bigrams) <= 0:
        print("no bigrams")

        
    print('\ntrigram analysis')
    for k,v in trigrams.items():
        outputAnalysis(k,v)
    if len(trigrams) <= 0:
        print("no trigrams")


def outputAnalysis(k,v):
    print('{0:10}: {1:.3f}, tot. occurences: {2}'.format(k, v[1]/v[0], v[0]))

#       testing
testnames = ("potatoes", "potatoes", "boil", "em", "em")
testwords = ("potatoes", "potatoes", "potatoes", "boil", "em", "mash", "em", "stick", "em", "in", "a", "stew", "em", "em")

for x in testnames:
    addMonogram(x, 1)

for x in testwords:
    addMonogram(x, 0)

analyzeData()
