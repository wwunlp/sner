#this is meant to test the correct functioning of the supporting modules

from classes import Rule, RuleSet, RuleType, Token, TokenSet, TokenType
from scripts.ner import contextualfromnames, namesfromrules, rulefilter, \
rulesperformance, spellingfromnames
import unittest


class RuleTests(unittest.TestCase):
    def runTest(self):
        #test that the rule gets initialized properly
        rule1 = Rule(RuleType.spelling, "jewawa", 0.7)
        assert hash("jewawaRuleType.spelling") == rule1.__hash__()
        assert rule1.strength == 0.7
        assert rule1 == rule1
        assert not (rule1 < rule1)

        #test the rules __lt__ function (for sorting) as well as __eq__ (for hashing)
        rule2 = Rule(RuleType.left_context, "abcd", 0.7)
        assert rule2 < rule1
        assert not (rule1 == rule2)
        rule2.strength = 0.8
        assert rule2 > rule1
        rule2.strength = 6000
        rule2.rtype = RuleType.spelling
        rule2.contents = "jewawa"
        assert rule2 == rule1

class TokenTests(unittest.TestCase):
    def runTest(self):
        token1 = Token("lerp", "derp", "rerp", TokenType.personal_name)
        token2 = Token("lerp", "aerp", "rerp", TokenType.profession)

        assert not (token1 == token2)

class TokenSetTests(unittest.TestCase):
    def runTest(self):
        token1 = Token("lerp", "derp", "rerp", TokenType.personal_name)
        token2 = Token("lerp", "aerp", "rerp", TokenType.profession)
        tokset1 = TokenSet()
        tokset.addToken(token1)
        tokset.addToken(token2)

        

class RuleSetTests(unittest.TestCase):
    def runTest(self):

class TokenSetTests(unittest.TestCase):
    def runTest(self):

        
def main():
    suite = unittest.TestSuite()

    suite.addTest(RuleTests())
    suite.addTest(TokenTests())
    
    runner = unittest.TextTestRunner()

    runner.run(suite)

main()
