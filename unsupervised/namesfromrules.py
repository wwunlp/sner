# This file is meant to recognize names in the corpus when given a set of rules

from ruleset import *
from tokenset import *

# Takes the overall corpus as input, as well as a single Rule object,
#  as defined in ruleset.py.
# Will return a TokenSet of tokens satisfying the passed-in Rule,
#  referred to in the code as 'names'.


def namesFromRule(corpus, rule):
    names = TokenSet()

    # How to handle a spelling rule
    def spelling(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if rule.contents in str(token):
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


# This function is meant to use the provided ruleset to scan
#  the corpus for names.
# It will then return the names in quesiton, which will be used
# to generate more rules.
def namesFromRules(corpus, rules):
    names = TokenSet()

    for rule in rules:
        results = namesFromRule(corpus, rule)

        # Can probably write an extend function that doesn't enforce
        #  set properties.
        # You can insert them without checking for redundancies because
        # they already were checked.
        names.extend(results)

    return names


# Convenience function
def run(corpus, rules):
    return namesFromRules(corpus, rules)
