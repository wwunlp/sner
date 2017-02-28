"""Token"""
from enum import Enum


class Token:
    """
    This represents a given 'token' in the corpus.
    It represents a combination of left context, right context, and the word itself.
    Any identical tokens will be combined into pre-existing ones.
	
	Attributes:
        left_context (str): contents of token to the left of this token
        word (str): this token as a string
        right_context (str): contents of token to the right of this token
		type (Enum): what kind of data does this token represent? (personal name, date, etc)
		rules (set): set of Rule objects that apply to this token
        name_probability (float): percent chance that this token represents a name
    """

    Type = Enum('Types', 'none personal_name geographic_name profession number date')

    def __init__(self, left_context, word, right_context, token_type):
        self.left_context = left_context
        self.word = str(word)
        self.right_context = right_context
        self.type = token_type
        self.rules = set()
        self.name_probability = 0.0

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.word == other.word

    def __nq__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Token(left_context={}, word={}, right_context={}, {})".format(
            self.left_context,
            self.word,
            self.right_context,
            self.type
        )

    @classmethod
    def find_type(cls, token_type):
        """Parse a string representation and return an equivalent Token.Type
		enumeration value.  A string representation is used in the input data
		files, however the enumeration allows for faster comparisons.  This
		function is a convenience to make it easier to scan the appropriate
		input files.
		
        Args:
            token_type (string): String representation of a type of token.

        Returns:
            type (Token.Type): Enumeration value representing the type of token.

        Raises:
            TypeError: If the string represents some unrecognized type of
					   token, then freak out.  You should probably respond to 
					   this by adding said rule to the enumeration above as 
					   well as to the code here.
        """

        if token_type == 'PN':
            return Token.Type.personal_name

        elif token_type == 'GN':
            return Token.Type.geographic_name

        elif token_type == 'PF':
            return Token.Type.profession

        elif token_type == 'N':
            return Token.Type.number

        elif token_type == 'D':
            return Token.Type.date

        elif token_type == '-':
            return Token.Type.none

        else:
            raise TypeError("Unrecognized Word Type: " + word_type)
