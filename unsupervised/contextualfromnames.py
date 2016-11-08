# This file is meant to generate conextual rules from a set of identified
# name tokens. It needs the corpus as well as the name set in order to
# assess the performance of any rules it finds from the names

from ruleset import *
from tokenset import *
import rulesperformance
import rulefilter


def genContextuals(names, existingrules):
    newRules = RuleSet()

    for name in names:
        # New rules are assumed to have no strength until they are assessed
        #  later by scanning the whole corpus

        # Create left context rule
        leftContext = Rule(RuleType.left_context, str(name.left_context), -1)
        # Create right context rule
        rightContext = Rule(RuleType.right_context,
                            str(name.right_context), -1)

        # No redundant rules allowed!
        if not existingrules.containsRule(leftContext):
            newRules.addRule(leftContext)

        if not existingrules.containsRule(rightContext):
            newRules.addRule(rightContext)

    return newRules


def run(corpus, existingrules, names, maxrules, cfg):
    rules = genContextuals(names, existingrules)

    rulesperformance.run(corpus, rules)

    rules = rulefilter.run(rules, maxrules)

    return rules
