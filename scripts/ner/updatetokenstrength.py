from classes import Rule, Token


#this system will update the strength of all tokens it is given, using the rules it is


#borrowed from namesfromrules, used to find all names a given rule applies to
def namesFromRule(corpus, rule):
    names = set()

    # How to handle a spelling rule
    def spelling(corpus, ruleset
        names = set()
        for token in corpus:
            if rule.contents in str(token):
                Token.add(names, token, rule)
        return names

    # How to handle a right context rule
    def leftContext(corpus, rule):
        names = set()
        for token in corpus:
            if str(token.left_context) == rule.contents:
                Token.add(names, token, rule)
        return names

    # How to handle a right context rule
    def rightContext(corpus, rule):
        names = set()
        for token in corpus:
            if str(token.right_context) == rule.contents:
                Token.add(names, token, rule)
        return names

    # Decide how to handle the passed-in rule
    if rule.type == Rule.Types.spelling:
        names = spelling(corpus, rule)
    elif rule.type == Rule.Types.left_context:
        names = leftContext(corpus, rule)
    elif rule.type == Rule.Types.right_context:
        names = rightContext(corpus, rule)
    elif rule.rytpe == Rule.Types.unset:
        tb = sys.exc_info()[2]
        raise TypeError("improperly initialized rule within ruleset: " +
                        rule.contents + ", type unset").with_traceback(tb)
    else:
        print("unrecognized rule type found in nameFromRule: " +
              rule.content + ", of type: " + rule.type)

    return names

def updateWithRule(rule, tokens):
    applicableTokens = namesFromRule(tokens, rule)

    for token in applicableTokens:
        if rule in token.applicable_rules:
            raise ValueError("attempted to apply same rule to a token twice!")

        token.applicable_rules.append(rule)

        #use statistical rules to calculate the new probability
        #in other words, the probability that all other applicable rules in addition to the current one are wrong
        initialprob = token.name_probability
        addedprob = rule.strength

        newprob = 1 - ((1 - initialprob) * (1 - addedprob))

        token.name_probability = newprob



def run(tokens, rules, cfg):
    for rule in rules:
        updateWithRule(rule, tokens)
