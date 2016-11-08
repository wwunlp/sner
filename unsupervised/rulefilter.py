
from ruleset import *
from tokenset import *

#determine which rules will be accepted by an iteration of the algorithm

#relatively elaborate algorithm used to cut the rule list down to size
#it will take at least 20 rules, or if less than 20 are available, it will take what it can
#it will take as many rules as are available if they are rated past a certain threshold
def fancyCull(ruleset, minrules):
    acceptanceThreshold = 0.9
    
    rulelist = list(ruleset.rules)
    
    rulecount = 0

    resultset = RuleSet()

    for rule in ruleset:
        if rule.strength >= acceptanceThreshold:
            resultset.addRule(rule)
            rulecount += 1

    if rulecount < 20:
        sortedlist = sorted(list(ruleset.rules), reverse=True)

        while (rulecount < 20) and (len(sortedlist) > 0):
            resultset.addRule(sortedlist.pop(0))
            rulecount += 1

    return resultset

#sorts rules into the top n rules, where n = maxrules
#sorted by strength, ties broken by alphabetization
def truncateCull(ruleset, maxrules):
    #sort the rules from best to worst (uses the __lt__ function defined in Rule class (in ruleset.py))
    sortedlist = sorted(list(ruleset.rules), reverse=True)
    
    #trim the list down to only the rules that will go on to the next iteration
    sortedlist = sortedlist[:maxrules]
    
    rules = RuleSet()

    for rule in sortedlist:
        rules.addRule(rule)

    return rules
    

def run(ruleset, maxrules):
    #cut the rules down to only the ones that will be accepted in the next iteration
    rules = truncateCull(ruleset, maxrules)
    return rules
