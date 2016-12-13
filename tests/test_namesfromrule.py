from classes import Rule, Token
from models import ner
from scripts.ner import namesfromrule


def test_namesfromrule_main():
    """

    """

    corpus_file = 'tests/test_corpus.csv'
    seed_rules_file = 'tests/test_seed_rules.csv'

    corpus = ner.tokenize_corpus(corpus_file)
    seed_rules = ner.tokenize_seed_rules(seed_rules_file)

    expected = Token('aa-aa', 'bb-bb', 'cc-cc', Token.Type.personal_name)
    for rule in seed_rules:
        results = namesfromrule.main(corpus, rule)
        for name in results:
            assert name == expected
