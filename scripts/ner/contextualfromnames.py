# This file is meant to generate conextual rules from a set of identified
# name tokens. It needs the corpus as well as the name set in order to
# assess the performance of any rules it finds from the names

from classes import Rule, Token
from scripts.ner import rulesperformance, rulefilter


def genContextuals(names, existingrules):
    newRules = set()

    for name in names:
        # New rules are assumed to have no strength until they are assessed
        #  later by scanning the whole corpus

        # Create left context rule
        leftContext = Rule(Rule.Types.left_context, str(name.left_context), -1)
        # Create right context rule
        rightContext = Rule(Rule.Types.right_context,
                            str(name.right_context), -1)

        # No redundant rules allowed!
        if not leftContext in existingrules:
            newRules.add(leftContext)

        if not rightContext in existingrules:
            newRules.add(rightContext)

    return newRules


def run(corpus, existingrules, names, maxrules, cfg):
    rules = genContextuals(names, existingrules)

    rulesperformance.run(corpus, rules)

    rules = rulefilter.run(rules, maxrules)

    return rules
