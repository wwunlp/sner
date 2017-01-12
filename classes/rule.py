""" Rule """
from enum import Enum


class Rule:
    """
    Rule
    """

    Type = Enum('Types', 'unset spelling left_context right_context')

    def __init__(self, ruletype, rule, strength):
        self.type = ruletype
        self.contents = str(rule)
        self.strength = float(strength)
        self.occurrences = 1
        self.iteration = -1

    def __eq__(self, other):
        return self.key() == other.key()

    def __gt__(self, other):
        return self.strength > other.strength

    def __nq__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.key())

    def __lt__(self, other):
        return self.strength < other.strength

    def __str__(self):
        return "Rule(type={}, rule={}, strength={})".format(
            self.type.name,
            self.contents,
            self.strength
        )

    def key(self):
        """
        key
        """

        return "{}:{}".format(self.type.value, self.contents)

    @classmethod
    def find_type(cls, rule_type):
        """
        find rule type
        """

        if rule_type == 'LEFT_CONTEXT':
            return Rule.Type.left_context
        elif rule_type == 'RIGHT_CONTEXT':
            return Rule.Type.right_context
        elif rule_type == 'SPELLING':
            return Rule.Type.spelling
        else:
            raise TypeError
