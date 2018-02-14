import numpy as np
from sner.classes import Rule
from sner.scripts.ner import rulefilter


def test_rulefilter_main():
    """

    """

    rule_set = set()
    expected = set()
    values = np.linspace(0.1, 0.8, num=8)

    for strength in values:
        rule = Rule(Rule.Type.unset, "test-{}".format(strength), strength)
        rule_set.add(rule)

    for strength in values[3:]:
        rule = Rule(Rule.Type.unset, "test-{}".format(strength), strength)
        expected.add(rule)

    expected = sorted(expected, reverse=True)
    results = sorted(rulefilter.main(rule_set, 5), reverse=True)
    assert results == expected
