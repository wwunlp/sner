#determine which rules will be accepted by an iteration of the algorithm

#relatively elaborate algorithm used to cut the rule list down to size
#it will take at least 20 rules, unless not that many rules are available
#
def fancyCull:


def run():
    #sort the rules from best to worst (uses the __lt__ function defined in Rule class (in ruleset.py))
    sortedlist = sorted(list(rules.rules), reverse=True)

    rulecount = len(sortedlist)
    
    #trim the list down to only the rules that will go on to the next iteration
    if rulecount
    sortedlist = sortedlist[:maxrules]

    rules = RuleSet()

    for rule in sortedlist:
        rules.addRule(rule)
