"""Names from rule."""
from sner.classes import Rule


def main(corpus, rule):
    """
    Takes the overall corpus as input, as well as a single Rule object.
    Will return a Set of tokens satisfying the passed-in Rule, referred to in
    the code as 'names'.

    Args:
        corpus (set): Set of all Token objects in the corpus.
        rule (Rule): Rule object used to identify results.

    Returns:
        names (set): Set of Token objects that match the passed in Rule.

    Raises:
        TypeError

    """

    names = set()

    if rule.type == Rule.Type.left_context:
        for token in corpus:
            if rule.contents == token.left_context:
                names.add(token)
                token.rules.add(rule)

    elif rule.type == Rule.Type.right_context:
        for token in corpus:
            if rule.contents == token.right_context:
                names.add(token)
                token.rules.add(rule)

    elif rule.type == Rule.Type.spelling:
        for token in corpus:
            if rule.contents in token.word:
                names.add(token)
                token.rules.add(rule)

    elif rule.type == Rule.Type.unset:
        raise TypeError("improperly initialized rule within ruleset: " +
                        rule.contents + ", type unset")

    else:
        raise TypeError("unrecognized rule type found in nameFromRule: " +
                        rule.content + ", of type: " + rule.type)

    return names
