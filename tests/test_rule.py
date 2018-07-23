from sner.classes import Rule


def test_rule_init():
    """

    """

    rule = Rule(Rule.Type.left_context, 'ki', 0.989010989)
    assert rule.type == Rule.Type.left_context
    assert rule.contents == 'ki'
    assert rule.strength == 0.989010989
    assert rule.occurrences == 1
    assert rule.iteration == -1


def test_rule_eq():
    """

    """

    rule1 = Rule(Rule.Type.left_context, 'ki', 0.989010989)
    rule2 = Rule(Rule.Type.left_context, 'ki', 0.989010989)
    assert rule1 == rule2


def test_rule_nq():
    """

    """

    rule1 = Rule(Rule.Type.left_context, 'ki', 0.989010989)
    rule2 = Rule(Rule.Type.left_context, 'giri3', 0.9887640449)
    assert rule1 != rule2


def test_rule_str():
    """

    """

    rule = Rule(Rule.Type.left_context, 'ki', 0.989010989)
    expected_result = 'Rule(type=left_context, rule=ki, strength=0.989010989)'
    assert str(rule) == expected_result
