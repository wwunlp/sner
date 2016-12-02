from scripts import utilities
from collections import defaultdict
import codecs
import editdistance


def getPersonalNames(csvFile):
    """
    Args:
        csvfile = A csv file with the name on line[5] and line[9] is an identifier of its
                  type, where we are looking for 'PN' indicating a personal name.
        

    Returns:
        Puts found names from the csv file and returns them in a dictionary
         of the form: { Name : Occurrences }

    Raises:
        None

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


def getPNs(data):
    """
    Collects names in Garshana csv and returns them
    """
    return getPersonalNames(data.attestations)


def getKgrams(names, k):
    """
    Args:
        names = dictionary of the form { Names : Occurrences }
        k = Max k-gram you want to retrieve.
            Special values of k = -1 returning dictionary of monograms.
                          and k = -2 returning dictionary of monograms,
                                  followed by a dictionary of bigrams.

        Example use to get all monograms, bigrams, and trigrams:
        getKgrams(getPNs(), 3)


    Returns:
        A dictionary of all grams up to order k

    Raises:
        None

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
    nameDict = getPNs(data)
    # sampleNames = {"ab-ac-ad-ae" : 3, "ab-ae-ad" : 5, "ae-ac-ac-ad" : 1}
    testGrams = getKgrams(nameDict, 4)
    for i in range(2, 4):
        for key, value in testGrams[i].iteritems():
            if (value > 1):
                print("Gram: " + key + " seen : " + str(value))
