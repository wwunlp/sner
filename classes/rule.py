""" Rule """
from enum import Enum


class Rule:
    """Object representing a rule that is used to identify names within the 
	corpus.  This object is used in the ner model, rather than the sner model.

    Attributes:
        type (Enum): What variety of rule is this (spelling, context, etc)
        contents (str): Data that defines the rule
        strength (float): Percent chance that any token this rule applies to 
					      is a name
        occurrences (int): Number of tokens this rule applies to
		iteration (int): The iteration in which this rule was generated
    """

	#enumeration representing the various rule types, these are used to speed
	#comparisons between rules
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
        """Define what constitutes an identifying key for a Rule type object.
		The Rule's type as a string concatenated with the Rule's contents was
		considered to be uniquely identifying.
		
        Args:
            None

        Returns:
            key (string): Uniquely identifying key for this Rule object.

        Raises:
            None
        """

        return "{}:{}".format(self.type.value, self.contents)

    @classmethod
    def find_type(cls, rule_type):
        """Parse a string representation and return an equivalent Rule.Type
		enumeration value.  A string representation is used in the input data
		files, however the enumeration allows for faster comparisons.  This
		function is a convenience to make it easier to scan the appropriate
		input files.
		
        Args:
            rule_type (string): String representation of a type of rule.

        Returns:
            type (Rule.Type): Enumeration value representing the type of rule.

        Raises:
            TypeError: If the string represents some unrecognized type of rule,
					   then freak out.  You should probably respond to this by
					   adding said rule to the enumeration above as well as to
					   the code here.
        """

        if rule_type == 'LEFT_CONTEXT':
            return Rule.Type.left_context
        elif rule_type == 'RIGHT_CONTEXT':
            return Rule.Type.right_context
        elif rule_type == 'SPELLING':
            return Rule.Type.spelling
        else:
            raise TypeError
