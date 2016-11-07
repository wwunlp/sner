
from enum import Enum
import sys


class RuleSet:
    rules = set()

    def __iter__(self):
        return iter(self.rules)

    def addRule(self, rule):
        if(type(rule) is not Rule):
            tb = sys.exc_info()[2]
            raise TypeError("Tried to push something other than a rule into" +
                            " a RuleSet").with_traceback(tb)

        self.rules.add(rule)

    def extend(self, setOfRules):
        if(type(setOfRules) is not RuleSet):
            tb = sys.exc_info()[2]
            raise TypeError("Attempted to add contents of RuleSet to another" +
                            " ruleset, was given something other than a" +
                            " RuleSet to add").with_traceback(tb)

        self.rules = self.rules.union(setOfRules.rules)

    def containsRule(self, rule):
        if(rule in self.rules):
            return True
        return False

    def __init__(self):
        self.rules = set()


class RuleType(Enum):
    unset = -1
    spelling = 0
    left_context = 1
    right_context = 2


# Used to represent any name rules identified by the algorithm
class Rule:
    rtype = RuleType.unset
    contents = str()
    strength = float()

    def key(self):
        return self.contents + str(self.rtype.value)

    #needed for the hashing to work in the RuleSet above
    def __eq__(self, other):
        return self.key() == other.key()

    #needed so that the rules can be sorted easily
    def __lt__(self, other):
        if self.strength == other.strength:
            return self.contents < other.contents
        else:
            return self.strength < other.strength

    def __hash__(self):
        return hash(self.contents + str(self.rtype))

    def __init__(self, ruletype, rule, strength):
        self.rtype = ruletype
        self.contents = str(rule)
        self.strength = float(strength)
