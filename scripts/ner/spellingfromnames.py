# This file is meant to generate spelling rules from a list of identified name
# tokens.

from classes import Rule, Token
from scripts.ner import rulefilter, rulesperformance


# Stolen from readnames.py, identifies spelling patterns in the form of k-grams
# Produces a list of monograms on up to k-grams
def getKgrams(names, k):
    """
    names is assumed to be a dictionary with keys representing names and values
     their occurences
    k is the max order of grams you wish to retrieve
    -1 will return a list containing a dictionary of monograms
    -2 will return a list with a dict of monograms followed by a dict of
     bigrams
    Example use for monogram, bigram, and trigrams:
    getKgrams(getPNs(), 3)
    """
    grams = list()

    for name in names:
        syllables = str(name).split('-')

        for i in range(1, k + 1):
            end = len(syllables) - i + 1
            for j in range(0, end):
                gram = '-'.join(syllables[j: j + i])
                grams.append(gram)

    return grams


def gramsToRules(kgrams, allrules):
    rules = set()

    for gram in kgrams:
        rule = Rule(Rule.Types.spelling, gram, -1)
        if not rule in allrules:
            rules.add(rule)

    return rules


def run(corpus, allrules, names, maxrules):
    # Uses up to trigrams currently
    maxGram = 3

    # Get all possible spelling rules from the names passed in
    kgrams = getKgrams(names, maxGram)
    rules = gramsToRules(kgrams, allrules)

    rulesperformance.run(corpus, rules)

    rules = rulefilter.run(rules, maxrules)

    return rules
