from enum import Enum


class Token:
    """
    This represents a given 'token' in the corpus.
    It represents a combination of left context, right context, and the word itself.
    Any identical tokens will be combined into pre-existing ones.
    This is meant to be used in conjunction with the TokenSet implemented below.
    """

    Type = Enum('Types', 'unset none personal_name geographic_name profession')
    
    def __init__(self, left_context, token, right_context, annotation):
        self.left_context = left_context
        self.token = token       
        self.right_context = right_context
        self.annotation = annotation
        self.applicable_rules = []       
        self.occurrences = 1
        self.name_probability = 0

    def __eq__(self, other):
        if type(self) is type(other):
            return self.key() == other.key()
        else:
            return False

    def __nq__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.token + str(self.left_context) +
                    str(self.right_context) + str(self.annotation.value))

    def __str__(self):
        return self.token

    def key(self):
        return ((self.token + str(self.left_context) +
                str(self.right_context)), self.annotation.value)
    
    def get_type(word_type):
        """
        Args:
            word_type (str): Word type from corpus

        Returns:
            Token.Type the correlates to word_type

        Raises:
            TypeError
        """

        if word_type == 'PN':
            return Token.Type.personal_name

        elif word_type == 'GN':
            return Token.Type.geographic_name

        elif word_type == 'PF':
            return Token.Type.profession

        elif word_type == '-':
            return Token.Type.none

        else:
            TypeError
