#this file is meant to recognize names in the corpus when given a set of rules

from ruleset import *
from tokenset import *

#takes the overall corpus as input, as well as a single Rule object (as defined in ruleset.py)
#will return a TokenSet of tokens satisfying the passed-in Rule, referred to in the code as 'names'
def namesFromRule(corpus, rule):
    names = TokenSet()

    
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

#this function is meant to use the provided ruleset to scan the corpus for names
#it will then return the names in quesiton, which will be used to generate more rules
def namesFromRules(corpus, rules):
    names = TokenSet()

    for rule in rules:
        results = namesFromRule(corpus, rule)
        
        #can probably write an extend function that doesn't enforce set properties
        #you can insert them without checking for redundancies because they already were checked
        names.extend(results)
        
    return names

#convenience function
def run(corpus, rules):
    return namesFromRules(corpus, rules)
