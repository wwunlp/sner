
from enum import Enum
import sys


class TokenType(Enum):
    unset = -1
    none = 0
    personal_name = 1


# This represents a given 'token' in the corpus.
# It represents a combination of left context, right context, and the word
#  itself.
# Any identical tokens will be combined into pre-existing ones.
# This is meant to be used in conjunction with the TokenSet implemented below.
class Token:
    token = None
    annotation = TokenType.unset
    left_context = None
    right_context = None
    occurrences = 1

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

    def __str__(self):
        return self.token


# This acts as an effecient container for Token objects, take my word for it.
# It will enforce 'Set' style behavior on the tokens in that no two identical
# token objects will be allowed.
class TokenSet:
    tokens = dict()

    def __iter__(self):
        return iter(self.tokens)

    def addToken(self, token, rule):
        if(type(token) is not Token):
            tb = sys.exc_info()[2]
            raise TypeError("Tried to push something other than a token" +
                            " into a TokenSet").with_traceback(tb)

        try:
            existingtoken = self.tokens[token]
        except KeyError:
            existingtoken = None

        if(existingtoken is None):
            self.tokens[token] = token
        else:
            existingtoken.occurrences += 1
            if rule:
                rule.occurrence += 1

    def extend(self, setOfTokens):
        if(type(setOfTokens) is not TokenSet):
            tb = sys.exc_info()[2]
            raise TypeError("Attempted to add contents of TokenSet to" +
                            " another TokenSet, was given something other" +
                            " than a TokenSet to add").with_traceback(tb)

        for token in setOfTokens:
            self.addToken(token, None)

    def __init__(self):
        self.tokens = dict()
