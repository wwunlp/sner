"""
Generates dictionaries of monograms, bigrams, and trigrams, mapping them to
lists containing the number of times they occur in names, and the number of
times they occur in total.  This is information later used to evaluate these
grams usefulness as name recognition rules.
"""

from scripts import readnames, utilities
from collections import defaultdict

monograms = defaultdict(list)
bigrams = defaultdict(list)
trigrams = defaultdict(list)
rules = {}

def gramhelper(gramDict, gram, namecount, totalcount):
    """
	Utility function to insert arbitrary n-grams into dictionaries that
	associate them with lists containing the number of times that gram occurred
	as well as the number of times that gram occurred in a name.
	
    Args:
            gramDict = dictionary to recieve an n-gram
            gram = gram to be inserted into the dict
            namecount = the occurrences for this n-gram in a name
            totalcount = how many times this gram has occurred in the corpus in any word

    Returns:
            Updates gramDict with the information from gram

    Raises:

    """
    list = gramDict[gram]

    if(len(list) == 0):
        list.append(0)
        list.append(0)

    list[0] += totalcount
    list[1] += namecount


"""
The following three functions work similarly, adding the gram and count of an
  individual name and total count of that gram occurring to the dictionary of
  the related gram size.
Args:
    gram = string version of gram to be added
    namecount = how many times this particular name has occurred (?)
    totalcount = how many times this gram has occurred in the corpus

Returns:
    Updated gram mapping, increasing the count of that name occurring and that
      individual gram occurring.

Raises:

"""
    
def addMonogram(gram, namecount, totalcount):
    gramhelper(monograms, gram, namecount, totalcount)


def addBigram(gram, namecount, totalcount):
    gramhelper(bigrams, gram, namecount, totalcount)


def addTrigram(gram, namecount, totalcount):
    gramhelper(trigrams, gram, namecount, totalcount)

# Load name data


def loadData(data, allgrams, f):
    """
    Loads name data
    Args:
        data(string) = name of the corpus data file
        allgrams(dict) = dictionary of all grams of the form:
                   { gram : namecount, totalcount }
        f (file) = object used to access the output file

    Returns:
        Fills allgrams dictionary.

    Raises:
        If grams are found in name dataset but not in overall dataset, will
          print out the type of gram and oddity.

    """
    
    # Load ngrams found in names
    namegrams = readnames.getKgrams(readnames.getPNs(data), 3)

    if len(namegrams) >= 1:
        print("loading monograms in names")
        for k, v in namegrams[0].items():
            klower = k.lower()
            if klower in allgrams:
                totalcount = allgrams[klower]
                addMonogram(klower, v, totalcount)
            else:
                print("ERROR: monogram \"{0}\" found in name dataset but" +
                      "not overall dataset".format(klower))

    print()

    if len(namegrams) >= 2:
        print("loading bigrams in names")
        for k, v in namegrams[1].items():
            klower = k.lower()
            if klower in allgrams:
                totalcount = allgrams[klower]
                addBigram(klower, v, totalcount)
            else:
                print("ERROR: bigram \"{0}\" found in name dataset but" +
                      "not overall dataset".format(klower))

    print()

    if len(namegrams) >= 3:
        print("loading trigrams in names")
        for k, v in namegrams[2].items():
            klower = k.lower()
            if klower in allgrams:
                totalcount = allgrams[klower]
                addTrigram(klower, v, totalcount)
            else:
                print("ERROR: trigram \"{0}\" found in name dataset but" +
                      "not overall dataset".format(klower))

# Collect percentage statistics from the gram maps


def analyzeData(f):
    """
    Collect percentage statistics from the gram maps and writes them to a .csv
	output file.
    Args:
        f(file) = the csv file in utf-8 format being written to, with fields:
            N-Gram, Percentage, Occurence, Total Occurence

    Returns:
        None

    Raises:
		None

    """
    
    f.write("N-gram, Percentage, Occurence, Total Occurence\n".encode('utf-8'))

    print('monogram analysis')
    for k, v in monograms.items():
        outputAnalysis(k, v, f)
    if len(monograms) <= 0:
        print("no monograms")
    print("done.")

    print('\nbigram analysis')
    for k, v in bigrams.items():
        outputAnalysis(k, v, f)
    if len(bigrams) <= 0:
        print("no bigrams")
    print("done.")

    print('\ntrigram analysis')
    for k, v in trigrams.items():
        outputAnalysis(k, v, f)
    if len(trigrams) <= 0:
        print("no trigrams")
    print("done.")

    f.close()


def outputAnalysis(k, v, f):
    """
    Args:
        k(string) = 
        v = (?)
        f = csv file we are writing to.
    Returns:

    Raises:
        If an n-gram has greater than 100% significance, reports the n-gram.

    """
    
    significance = v[1] / v[0]
    if significance > 1:
        print("ERROR: ngram \"{0}\" has greater than 100% significance" +
              "({1: .4}) {2}: {3}".format(k, significance, v[1], v[0]))
    f.write("{0},{1},{2},{3}\n".format(k,
            significance, v[1], v[0]).encode('utf-8'))


# Main


def main(data, syll_count):
    f = open('results/spelling.csv', 'wb')
    loadData(data, syll_count, f)
    print()
    analyzeData(f)
