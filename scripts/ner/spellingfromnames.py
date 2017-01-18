# This file is meant to generate spelling rules from a list of identified name
# tokens.

from classes import Rule, Token
from scripts.ner import rulefilter, rulesperformance


# Produces a list of monograms on up to k-grams
def getKgrams(names, k):
    """
    Produces lists of grams, from monograms up to k-grams.
    Duplicate found in /scripts/readnames.py
    Example use to get monograms, birgams, and trigrams:
    getKgrams(getPNs(), 3)
    Args:
        names (dict) = dictionary of the form { Names : Occurrences }
        k (int) = Max k-gram you want to retrieve.
            Special values of k = -1 returning dictionary of monograms.
                          and k = -2 returning dictionary of monograms,
                                  followed by a dictionary of bigrams.

    Returns:
        A dictionary of all grams up to order k

    Raises:
        None

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


def gramsToRules(kgrams, allrules, iteration):
    rules = set()

    for gram in kgrams:
        rule = Rule(Rule.Type.spelling, gram, -1)
        if not rule in allrules:
            rules.add(rule)
            rule.iteration = iteration

    return rules


def main(corpus, allrules, names, maxrules, iteration, options):
    """
    Produces lists of grams, from monograms up to k-grams.
    Duplicate found in /scripts/readnames.py
    Example use to get monograms, birgams, and trigrams:
    getKgrams(getPNs(), 3)
    Args:
        corpus (set) = set of all tokens in the corpus
        allrules (set) = set of all rules in the corpus
		names (set) = set of tokens that will be used to generate new spelling rules
        maxrules (int) = maximum number of rules to be accepted with each iteration
        iteration (int) = what iteration are we currently on?
        options (Options) = collection of configuration data

    Returns:
        Set of spelling rules generated from names

    Raises:
        None

    """
    # Uses up to trigrams currently
    maxGram = 3

    # Get all possible spelling rules from the names passed in
    kgrams = getKgrams(names, maxGram)
    rules = gramsToRules(kgrams, allrules, iteration)

    rulesperformance.main(corpus, rules, options)

    rules = rulefilter.main(rules, maxrules)

    return rules
