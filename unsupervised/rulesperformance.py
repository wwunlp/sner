# Will assign a strength rating to the rule provided as a paramter.
# ProspectiveNames refers to the tokens this rule identified as names.
# It will check the annotations of these tokens to see if they are really names
# then it will use that to compute a strength rating

from ruleset import *
from tokenset import *


# Rate the strength of the individual rule passed in,
# given all Tokens where the rule is true (identifiedNames)
def rateRulePerformance(identifiedNames, rule):
    alpha = 0.1
    k = 2

    namesFound = 0
    total = 0
    for token in identifiedNames:
        namesFound += token.name_probability * token.occurrences
        total += token.occurrences

    strength = (namesFound + alpha) / (total + k * alpha)

    rule.strength = strength


# Find all tokens that match a given rule
# This is used to rate a rules performance, by totalling up the
# tokens that match the rule,
# and comparing that to how many of the tokens in that set are marked as a PN
def namesFromRule(corpus, rule):
    # How to handle a spelling rule
    def spelling(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if rule.contents in token.token:
                names.addToken(token)
        return names

    # How to handle a right context rule
    def leftContext(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if str(token.left_context) == rule.contents:
                names.addToken(token)
        return names

    # How to handle a right context rule
    def rightContext(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if str(token.right_context) == rule.contents:
                names.addToken(token)
        return names

    names = TokenSet()
    # Decide how to handle the passed-in rule
    if rule.rtype == RuleType.spelling:
        names = spelling(corpus, rule)
    elif rule.rtype == RuleType.left_context:
        names = leftContext(corpus, rule)
    elif rule.rtype == RuleType.right_context:
        names = rightContext(corpus, rule)
    elif rule.rytpe == RuleType.unset:
        tb = sys.exc_info()[2]
        raise TypeError("improperly initialized rule within ruleset: " +
                        rule.contents + ", type unset").with_traceback(tb)
    else:
        print("unrecognized rule type found in nameFromRule: " +
              rule.content + ", of type: " + rule.rtype)

    return names


def run(corpus, rules):
    i = 1
    length = len(list(rules.rules))

    for rule in rules:
        names = namesFromRule(corpus, rule)
        rateRulePerformance(names, rule)

        # Print progress information
        print("Rating rule performance, progress: " + str(i) + "/" +
              str(length) + 20 * ' ', end='\r')
        i += 1

    # Erase the last progress report
    print(' ' * 50, end='\r')
