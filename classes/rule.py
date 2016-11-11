from enum import Enum


class Rule:
    """

    """

    Type = Enum('Types', 'unset spelling left_context right_context')

    def __init__(self, ruletype, rule, strength):
        self.type = ruletype
        self.contents = str(rule)
        self.strength = float(strength)
        self.occurrences = 1

    def __eq__(self, other):
        if type(other) == type(self):
            return self.key() == other.key()
        else:
            return False

    def __nq__(slef, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.contents + str(self.type))

    def __lt__(self, other):
        if self.strength == other.strength:
            return self.contents < other.contents
        else:
            return self.strength < other.strength

    def __str__(self):
        return "Rule(type={}, rule={}, strength={})".format(
            self.type.name,
            self.contents,
            self.strength
        )

    def key(self):
        return self.contents + str(self.type.value)

