from classes import Rule, Token, TokenSet


def main(corpus, rule):
    """
    Takes the overall corpus as input, as well as a single Rule object.
    Will return a Set of tokens satisfying the passed-in Rule, referred to in
    the code as 'names'.

    Args:
        courpus (TokenSet): Set of Token objects.
        rule (Rule): Rule object.

    Returns:
        names (TokenSet): Set of Token objects.

    Raises:
        TypeError

    """

    names = TokenSet()

    # How to handle a spelling rule
    def spelling(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if rule.contents in str(token):
                names.add(token)
                
        return names

    # How to handle a right context rule
    def leftContext(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if str(token.left_context) == rule.contents:
                names.add(token)
 
        return names

    # How to handle a right context rule
    def rightContext(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if str(token.right_context) == rule.contents:
                names.add(token)
 
        return names

    # Decide how to handle the passed-in rule
    if rule.type == Rule.Type.spelling:
        names = spelling(corpus, rule)
    elif rule.type == Rule.Type.left_context:
        names = leftContext(corpus, rule)
    elif rule.type == Rule.Type.right_context:
        names = rightContext(corpus, rule)
    elif rule.rytpe == Rule.Type.unset:
        tb = sys.exc_info()[2]
        raise TypeError("improperly initialized rule within ruleset: " +
                        rule.contents + ", type unset").with_traceback(tb)
    else:
        print("unrecognized rule type found in nameFromRule: " +
              rule.content + ", of type: " + rule.type)

    return names
