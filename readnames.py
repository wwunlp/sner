

import codecs
from collections import defaultdict
import utilities
import editdistance


def getPersonalNames(csvFile):
    """
    Find names in given csv file and returns them in a dictionary
     with their counts
    Assumes that the 5th value on each line is the actual name and
    that the 9th value is an identifier for the type with "PN"
     indicating a Personal name
    """
    names = defaultdict(int)
    try:
        open_file = codecs.open(csvFile, 'r', encoding='utf-16')
        for line in open_file:
            line_list = line.split(',')
            name = line_list[5].rstrip()
            name = utilities.clean_line(name)

            text = line_list[4].rstrip()
            text = utilities.clean_line(text)
            text = text.split(' ')

            edit_distance = []
            for word in text:
                edit_distance.append(editdistance.eval(name, word))

            name = text[edit_distance.index(min(edit_distance))]
            nameType = line_list[9].rstrip()
            if (nameType == "PN"):
                names[name] = names[name] + 1
        open_file.close()
    except IOError:
        print("Cannot open: " + csvFile)

    return names


def getPNs():
    """
    Collects names in Garshana csv and returns them
    """
    return getPersonalNames("Garshana Dataset/Attestations_PNs.csv")


def getKgrams(names, k):
    """
    names is assumed to be a dictionary with keys representing names
     and values their occurences
    k is the max order of grams you wish to retrieve
    -1 will return a list containing a dictionary of monograms
    -2 will return a list with a dict of monograms followed by
     a dict of bigrams
    Example use for monogram, bigram, and trigrams:
    getKgrams(getPNs(), 3)
    """
    grams = [None] * k

    for i in range(0, k):
            grams[i] = defaultdict(int)

    for name, value in names.items():
        syllables = name.split('-')

        for i in range(1, k + 1):
            end = len(syllables) - i + 1
            for j in range(0, end):
                gram = '-'.join(syllables[j:j + i])
                grams[i-1][gram] = grams[i-1][gram] + value

    return grams


def testKgrams():
    """
    A simple test to print off Trigrams and Quadgrams that
    occur more than once [note: duplicate names will trigger these]
    """
    nameDict = getPNs()
    # sampleNames = {"ab-ac-ad-ae" : 3, "ab-ae-ad" : 5, "ae-ac-ac-ad" : 1}
    testGrams = getKgrams(nameDict, 4)
    for i in range(2, 4):
        for key, value in testGrams[i].iteritems():
            if (value > 1):
                print("Gram: " + key + " seen : " + str(value))
