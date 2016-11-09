from enum import Enum


# This represents a given 'token' in the corpus.
# It represents a combination of left context, right context, and the word
#  itself.
# Any identical tokens will be combined into pre-existing ones.
# This is meant to be used in conjunction with the TokenSet implemented below.
class Token:
    Types = Enum('Types', 'none personal_name geographic_name profession')
    applicable_rules = list() #list of Rule objects that are associated with this token

    def key(self):
        return ((self.token + str(self.left_context) +
                str(self.right_context)), self.annotation.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.key() == other.key()

        return False

    def __hash__(self):
        return hash(self.token + str(self.left_context) +
                    str(self.right_context) + str(self.annotation.value))

    def __init__(self, left, token, right, annotation):
        self.left_context = str(left)
        self.token = str(token)
        self.rightContext = str(right)
        self.annotation = annotation
        self.occurrences = 1

        self.applicable_rules = list()
        self.name_probability = 0

    def __str__(self):
        return self.token

    def add(set, token, rule):
        set.add(token)
        token.occurrences += 1
        if rule:
            rule.occurrences +=1
