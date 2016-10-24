#will assign a strength rating to the rule provided as a paramter
#prospectiveNames refers to the tokens this rule identified as names
#it will check the annotations of these tokens to see if they are really names
#then it will use that to compute a strength rating

from ruleset import *
from tokenset import *


#rate the strength of the individual rule passed in,
#given all Tokens where the rule is true (identifiedNames)
def rateRulePerformance(identifiedNames, rule):
    alpha = 0.1
    k = 2
    
    namesFound = 0
    total = 0
    for token in identifiedNames:
        if token.annotation == TokenType.personal_name:
            namesFound += token.occurrences
            total += token.occurrences
        else:
            total += token.occurrences

    strength = (namesFound + alpha) / (total + k * alpha)

    rule.strength = strength


#find all tokens that match a given rule
#this is used to rate a rules performance, by totalling up the tokens that match the rule,
#and comparing that to how many of the tokens in that set are marked as a PN
def namesFromRule(corpus, rule):
    #how to handle a spelling rule
    def spelling(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if rule.contents in str(token):
                names.addToken(token)
        return names

    #how to handle a right context rule
    def leftContext(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if str(token.left_context) == rule.contents:
                names.addToken(token)
        return names
                
    #how to handle a right context rule
    def rightContext(corpus, rule):
        names = TokenSet()
        for token in corpus:
            if str(token.right_context) == rule.contents:
                names.addToken(token)
        return names
        
        
    names = TokenSet()
    #decide how to handle the passed-in rule
    if rule.rtype == RuleType.spelling:
        names = spelling(corpus, rule)
    elif rule.rtype == RuleType.left_context:
        names = leftContext(corpus, rule)
    elif rule.rtype == RuleType.right_context:
        names = rightContext(corpus, rule)
    elif rule.rytpe == RuleType.unset:
        tb = sys.exc_info()[2]
        raise TypeError("improperly initialized rule within ruleset: " + rule.contents + ", type unset").with_traceback(tb)
    else:
        print("unrecognized rule type found in nameFromRule: " + rule.content + ", of type: " + rule.rtype)

    return names

def run(corpus, rules):
    i = 1
    length = len(list(rules.rules))

    for rule in rules:
        names = namesFromRule(corpus, rule)
        rateRulePerformance(names, rule)
        
        #print progress information
        print("Rating rule performance, progress: " + str(i) + "/" + str(length) + 20 * ' ', end='\r')
        i += 1

    #erase the last progress report
    print(' ' * 50, end='\r')
