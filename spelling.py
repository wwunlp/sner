#!/usr/bin/python3

#imports

from collections import defaultdict
import readnames
import utilities

#       dictionaries of monograms, bigrams, and trigrams
#other global declarations
#format is a name key, associated with a two element list containing the number of occurences of that gram
#the first element is number of occurences of that gram in total, the second is number of occurences within names

monograms = defaultdict(list)
bigrams = defaultdict(list)
trigrams = defaultdict(list)
rules = {}

#       utility functions to insert grams into maps
    
def gramhelper(gramDict, gram, namecount, totalcount):
    list = gramDict[gram]
    
    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[0] += totalcount
    list[1] += namecount

def addMonogram(gram, namecount, totalcount):
    gramhelper(monograms, gram, namecount, totalcount)

def addBigram(gram, namecount, totalcount):
    gramhelper(bigrams, gram, namecount, totalcount)

def addTrigram(gram, namecount, totalcount):
    gramhelper(trigrams, gram, namecount, totalcount)

#       load name data

def loadData(allgrams,f):
    #load ngrams found in names
    namegrams = readnames.getKgrams(readnames.getPNs(),3)
    
    if len(namegrams) >= 1:
        print("loading monograms in names")
        for k,v in namegrams[0].items():
            klower = k.lower()
            if klower in allgrams:
                totalcount = allgrams[klower]
                addMonogram(klower,v,totalcount)
            else:
                print("ERROR: monogram \"{0}\" found in name dataset but not overall dataset".format(klower))
                
    print()
    
    if len(namegrams) >= 2:
        print("loading bigrams in names")
        for k,v in namegrams[1].items():
            klower = k.lower()
            if klower in allgrams:
                totalcount = allgrams[klower]
                addBigram(klower,v,totalcount)
            else:
                print("ERROR: bigram \"{0}\" found in name dataset but not overall dataset".format(klower))

    print()
    
    if len(namegrams) >= 3:
        print("loading trigrams in names")
        for k,v in namegrams[2].items():
            klower = k.lower()
            if klower in allgrams:
                totalcount = allgrams[klower]
                addTrigram(klower,v,totalcount)
            else:
                print("ERROR: trigram \"{0}\" found in name dataset but not overall dataset".format(klower))
            
#       collect percentage statistics from the gram maps

def analyzeData(f):
    f.write("N-gram,Percentage,Occurence, Total Occurence\n".encode('utf-8'))
    
    print('monogram analysis')
    for k,v in monograms.items():
        outputAnalysis(k,v,f)
    if len(monograms) <= 0:
        print("no monograms")
    print("done.")

    print('\nbigram analysis')
    for k,v in bigrams.items():
        outputAnalysis(k,v,f)
    if len(bigrams) <= 0:
        print("no bigrams")
    print("done.")

 
    print('\ntrigram analysis')
    for k,v in trigrams.items():
        outputAnalysis(k,v,f)
    if len(trigrams) <= 0:
        print("no trigrams")
    print("done.")

    f.close()

def outputAnalysis(k,v,f):
    significance = v[1] / v[0]
    if significance > 1:
        print("ERROR: ngram \"{0}\" has greater than 100% significance ({1:.4}) {2}:{3}".format(k,significance,v[1],v[0]))
    f.write("{0},{1},{2},{3}\n".format(k, significance, v[1], v[0]).encode('utf-8'))


#main

def main(syll_count):
    f = open('results/spelling.csv', 'wb')
    loadData(syll_count,f)
    print()
    analyzeData(f)
