from classes import Rule, Token
from scripts.ner import rulesperformance


def test_rulesperformance_rateRulePerformance():
    """

    """

    alpha = 0.1
    k = 2.0
    accept_threshold = 0.9

    rule = Rule(Rule.Type.spelling, 'bb', 1.0)
    name = Token('aa-aa', 'bb-bb', 'cc-cc', Token.Type.personal_name)
    name.name_probability = 1.0
    names = set()
    names.add(name)

    rulesperformance.rateRulePerformance(names, rule, alpha, k, accept_threshold)

    expected_strength = (1.0 + alpha) / (1.0 + k * alpha)
    expected_occurrences = 1.0

    assert rule.strength == expected_strength
    assert rule.occurrences == expected_occurrences
