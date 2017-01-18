from classes import Rule, Token
from scripts.ner import namesfromrule


def main(tokens, rules):
    """
    This will update the strength of all tokens it is given, using
        the rules it is given.
    Args:
        tokens (set): Set object of Token objects.
        rules (set): Set object of Rule objects.

    Returns:
        None

    Raises:
        ValueError

    """

    for rule in rules:
        names = namesfromrule.main(tokens, rule)

        for name in names:
            # Raise ValueError("attempted to apply same rule to a token twice!")

            # Use statistical rules to calculate the new probability
            # In other words, the probability that all other applicable rules in addition
            #  to the current one are wrong
            initialprob = name.name_probability
            
            if ((initialprob < 0) and (initialprob > 1)):
                raise ValueError("Token \"" + str(name) + "\" has impossible name probability (v < 0 or v > 1): " + str(initialprob))
            
            addedprob = rule.strength
            
            if ((addedprob < 0) and (addedprob > 1)):
                raise ValueError("Rule \"" + str(rule) + "\" has impossible strength rating (str < 0 or str > 1): " + str(addedprob))

            newprob = 1 - ((1 - initialprob) * (1 - addedprob))
            
            if ((newprob < 0) and (newprob > 1)):
                raise ValueError("Generated impossible name probability: " + str(newprob))

            name.name_probability = newprob
