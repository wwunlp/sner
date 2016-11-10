from classes import Rule, Token
from scripts.ner import rulesperformance, rulefilter


def main(corpus, existingrules, names, maxrules):
    """This is meant to generate conextual rules from a set of identified
    name tokens. It needs the corpus as well as the name set in order to
    assess the performance of any rules it finds from the names

    Args:
        corpus (set): Set of Token objects.
        existingrules (set): Set of Rule objects.
        names (set): Set of Token objects.
        maxrules (int): int of max rules.

    Returns:
        rules (set): Set of Rule objects.

    Raises:
        None
    """

    newRules = set()

    for name in names:
        # New rules are assumed to have no strength until they are assessed
        #  later by scanning the whole corpus

        # Create left context rule
        leftContext = Rule(Rule.Types.left_context, str(name.left_context), -1)
        # Create right context rule
        rightContext = Rule(Rule.Types.right_context,
                            str(name.right_context), -1)

        # No redundant rules allowed!
        if leftContext not in existingrules:
            newRules.add(leftContext)

        if rightContext not in existingrules:
            newRules.add(rightContext)

    rulesperformance.main(corpus, newRules)

    rules = rulefilter.main(newRules, maxrules)

    return rules
