from sner.classes import Display, Rule, Token
from sner.models import ner
from sner.scripts.ner import namesfromrule


def test_namesfromrule_main():
    """

    """

    corpus_file = 'tests/test_corpus.csv'
    seed_rules_file = 'tests/test_seed_rules.csv'

    display = Display()

    display.start()
    corpus = ner.import_corpus(corpus_file, display)
    display.finish()

    display.start()
    seed_rules = ner.import_seed_rules(seed_rules_file, display)
    display.finish()

    expected = Token('aa-aa', 'bb-bb', 'cc-cc', Token.Type.personal_name)
    for rule in seed_rules:
        results = namesfromrule.main(corpus, rule)
        for name in results:
            assert name == expected
