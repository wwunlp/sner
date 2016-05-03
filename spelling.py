#!/usr/bin/python3


#dictionaries of monograms, bigrams, and trigrams
#format is a name key, associated with a two element list containing the number of occurences of that gram
#the first element is number of occurences of that gram in total, the second is number of occurences within names

from collections import defaultdict

monograms = defaultdict(list)
bigrams = defaultdict(list)
trigrams = defaultdict(list)

#utility functions to insert grams into maps
    
#isName takes one if it is a name, zero otherwise
def addMonogram(gram, isName):
    list = monograms[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[isName] += 1

def addBigram(gram):
    list = bigrams[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[isName] += 1

def addTrigram(gram):
    list = bigrams[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[isName] += 1


#xml parser to fetch names from the xml file and harvest the grams



#collect percentage statistics from the gram maps

