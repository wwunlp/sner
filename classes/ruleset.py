from enum import Enum


# Used to represent any name rules identified by the algorithm
class Rule:
    Types = Enum('Types', 'spelling left_context right_context')
    contents = str()
    strength = float()

    def __str__(self):
        return "Rule(type={}, rule={}, strength={})".format(
            self.type.name,
            self.contents,
            self.strength
        )

    def key(self):
        return self.contents + str(self.type.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.key() == other.key()

    #needed so that the rules can be sorted easily
    def __lt__(self, other):
        if self.strength == other.strength:
            return self.contents < other.contents
        else:
            return self.strength < other.strength

    def __hash__(self):
        return hash(self.contents + str(self.type))

    def __init__(self, ruletype, rule, strength):
        self.type = ruletype
        self.contents = str(rule)
        self.strength = float(strength)
        self.occurrence = 1
