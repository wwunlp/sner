from classes import Rule, Token


def main(ruleset, maxrules):
    """
    #determine which rules will be accepted by an iteration of the algorithm

    #sorts rules into the top n rules, where n = maxrules
    #sorted by strength, ties broken by alphabetization

    #cut the rules down to only the ones that will be accepted in the next iteration

    """

    #sort the rules from best to worst (uses the __lt__ function defined in Rule class (in ruleset.py))
    sortedlist = sorted(list(ruleset), reverse=True)

    #trim the list down to only the rules that will go on to the next iteration
    sortedlist = sortedlist[:maxrules]

    rules = set()

    for rule in sortedlist:
        rules.add(rule)

    return rules
