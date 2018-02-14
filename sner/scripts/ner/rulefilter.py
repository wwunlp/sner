from sner.classes import Rule, Token


def main(ruleset, maxrules):
    """
    Determine which rules will be accepted by an iteration of the algorithm

    Sorts rules into the top n rules, where n = maxrules
    Sorted by strength, ties broken by alphabetization

    Args:
        ruleset = set of all rules known
        maxrules = integer value of maximum number of rules we can accept
    Returns:
        The set of rules that are to be accepted by the next iteration.

    Raises:
        None

    """
    
    #sort the rules from best to worst (uses the __lt__ function defined in Rule class (in ruleset.py))
    sortedlist = sorted(ruleset, reverse=True)

    #trim the list down to only the rules that will go on to the next iteration
    sortedlist = sortedlist[:maxrules]

    rules = set()

    for rule in sortedlist:
        rules.add(rule)

    return rules
