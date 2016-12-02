# Will assign a strength rating to the rule provided as a paramter.
# ProspectiveNames refers to the tokens this rule identified as names.
# It will check the annotations of these tokens to see if they are really names
# then it will use that to compute a strength rating

from classes import Rule, Token
from scripts.ner import namesfromrule


# Rate the strength of the individual rule passed in,
# given all Tokens where the rule is true (identifiedNames)
def rateRulePerformance(identifiedNames, rule, alpha, k):
    namesFound = 0
    total = 0
    for token in identifiedNames:
        namesFound += token.name_probability * token.occurrences
        total += token.occurrences

    strength = (namesFound + alpha) / (total + k * alpha)

    rule.strength = strength
    rule.occurrences = len(identifiedNames)


# Find all tokens that match a given rule
# This is used to rate a rules performance, by totalling up the
# tokens that match the rule,
# and comparing that to how many of the tokens in that set are marked as a PN


def main(corpus, rules, options):
    """
    Finds all tokens that match a given rule, using that to rate the rules
    performance. Rates rule performance by totalling up the tokens that 
    match the rule, and comparing that to how many of the tokens in that set
    are marked as a PN.
    Args:
        corpus = Set of all lines from the corpus.
        rules = RuleSet object of all currently used rules.
        options = values pulled from the configuration file.

    Returns:
        None

    Raises:
        None

    """
    
    alpha = options.alpha
    k = options.k
    i = 1
    length = len(rules)

    for rule in rules:
        names = namesfromrule.main(corpus, rule)
        rateRulePerformance(names, rule, alpha, k)

        # Print progress information
        print("Rating rule performance, progress: " + str(i) + "/" +
              str(length) + 20 * ' ', end='\r')
        i += 1

    # Erase the last progress report
    print(' ' * 50, end='\r')
