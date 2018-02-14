from sner.classes import Rule, Token
from sner.scripts.ner import rulesperformance, rulefilter


def main(corpus, rules, names, max_rules, iteration, options, display):
    """
    This is meant to generate conextual rules from a set of identified
    name tokens. It needs the corpus as well as the name set in order to
    assess the performance of any rules it finds from the names

    Args:
        corpus (set): Set of all Token objects in the corpus.
        rules (set): Set of all Rule objects that have been found so far.
        names (set): Set of Token objects to derive new context rules from.
        max_rules (int): maximum number of rules to be accepted each iteration.
        iteration (int): what iteration is the algorithm currently on?
        options (Options): collection of configuration options

    Returns:
        new_rules (set): Set of Rule objects.

    Raises:
        None

    """

    new_rules = set()

    for name in names:
        # New rules are assumed to have no strength until they are assessed
        #  later by scanning the whole corpus

        # Create left context rule
        left_context = Rule(Rule.Type.left_context, str(name.left_context), -1)
        # Create right context rule
        right_context = Rule(Rule.Type.right_context, str(name.right_context), -1)

        # No redundant rules allowed!
        if left_context not in rules:
            left_context.iteration = iteration
            new_rules.add(left_context)

        if right_context not in rules:
            right_context.iteration = iteration
            new_rules.add(right_context)

    rulesperformance.main(corpus, new_rules, options, iteration, display)

    new_rules = rulefilter.main(new_rules, max_rules)

    return new_rules
