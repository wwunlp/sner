from classes import Rule, Token
from scripts.ner import namesfromrule


def main(tokens, rules):
    """
    This will update the strength of all tokens it is given, using
        the rules it is given.
    Args:
        tokens (TokenSet): Set object of Token objects.
        rules (set): Set object of Rule objects.

    Returns:
        None

    Raises:
        ValueError

    """

    for rule in rules:
        applicableTokens = namesfromrule.main(tokens, rule)

        for token in applicableTokens:
            if rule not in token.applicable_rules:
                # Raise ValueError("attempted to apply same rule to a token twice!")

                token.applicable_rules.append(rule)

                # Use statistical rules to calculate the new probability
                # In other words, the probability that all other applicable rules in addition
                #  to the current one are wrong
                initialprob = token.name_probability
                addedprob = rule.strength

                newprob = 1 - ((1 - initialprob) * (1 - addedprob))

                token.name_probability = newprob
