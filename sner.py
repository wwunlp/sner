"""
Sumerian Named Entity Recognition: sner.py

This file bootstraps the program, parsing arguments and configuration file.
Also offers interface for our analysis and formatting tools and test functions.
"""
import argparse
import json
import os
import pytest
from models import decision, random_forest # naive, ner, random_forest, sgd, svc
from scripts import export, export_atf, overfit_check # analysis, export, formatting


def add_args(parser):
    """
    Adds arguments from the command line and interprets them as appropriate.

    Args:
        parser

    Returns:
        None

    Raises:
        None

    """

    parser.add_argument(
        '-r',
        '--run',
        help='Run one the following models: '
        '[dec], '
        '[nbc], '
        '[ner], '
        '[rdf], '
        '[sgd], '
        'or [svc]. '
        'Or one of the following routines: '
        '[analysis], '
        '[export], '
        '[export-atf], '
        '[formatting], '
        '[over-fit], '
        'or [testing].',
        required=False,
        choices=[
            'dec',
            'nbc',
            'ner',
            'rdf',
            'sgd',
            'svc',
            'analysis',
            'export',
            'export-atf',
            'formatting',
            'testing',
            'over-fit'
        ]
    )
    parser.add_argument(
        '-cf',
        '--config',
        help='Configuration file to use',
        required=False
    )
    parser.add_argument(
        '-p',
        '--path',
        help='Path to data directory',
        required=False
    )
    parser.add_argument(
        '-c',
        '--corpus',
        help='File name of the corpus',
        required=False
    )
    parser.add_argument(
        '-a',
        '--attestations',
        help='File name of the attestations',
        required=False
    )
    parser.add_argument(
        '-sr',
        '--seed-rules',
        help='File name of the seed rules',
        required=False
    )
    parser.add_argument(
        '-i',
        '--iterations',
        help='Number of iterations',
        type=int,
        required=False
    )
    parser.add_argument(
        '-mr',
        '--max-rules',
        help='Max number of rules per iterations',
        type=int,
        required=False
    )
    parser.add_argument(
        '-al',
        '--alpha',
        help='Alpha value',
        type=float,
        required=False
    )
    parser.add_argument(
        '-k',
        '--k',
        help='K value',
        type=float,
        required=False
    )
    parser.add_argument(
        '-nd',
        '--norm-date',
        help='Enable date normalization',
        type=bool,
        required=False
    )
    parser.add_argument(
        '-ng',
        '--norm-geo',
        help='Enable geographical name normalization',
        type=bool,
        required=False
    )
    parser.add_argument(
        '-nn',
        '--norm-num',
        help='Enable number normalization',
        type=bool,
        required=False
    )
    parser.add_argument(
        '-np',
        '--norm-prof',
        help='Enable profession normalization',
        type=bool,
        required=False
    )


def main():
    """
    Collects arguments and configurations, or sets defaults.
    Calls either the NER, analysis, formatting, or testing routines.

    Args:
        None

    Returns:
        None

    Raises:
        None

    """

    parser = argparse.ArgumentParser()
    add_args(parser)
    args = parser.parse_args()

    config_path = args.config or \
                  os.environ.get('SNER_CONF') or \
                  'sner.conf'

    if os.path.exists(config_path):
        config_file = json.load(open(config_path))
    else:
        config_file = {
            'run': '',
            'path': '',
            'corpus': '',
            'attestations': '',
            'seed-rules': '',
            'iterations': '',
            'max-rules': '',
            'alpha': '',
            'k': '',
            'norm': {
                'date': '',
                'geo': '',
                'num': '',
                'prof': ''
            }
        }

    config = {
        'run': args.run or \
               config_file['run'] or \
               'ner',
        'path': args.path or \
                config_file['path'] or \
                'data/',
        'corpus': args.corpus or \
                  config_file['corpus'] or \
                  'corpus.csv',
        'attestations': args.attestations or \
                        config_file['attestations'] or \
                        'attestations.csv',
        'seed-rules': args.seed_rules or \
                      config_file['seed-rules'] or \
                      'seed_rules.csv',
        'iterations': args.iterations or \
                      config_file['iterations'] or \
                      5,
        'max-rules': args.max_rules or \
                     config_file['max-rules'] or \
                     5,
        'alpha': args.alpha or \
                 config_file['alpha'] or \
                 0.1,
        'k': args.k or \
             config_file['k'] or \
             2.0,
        'norm': {
            'date': args.norm_date or \
                    config_file['norm']['date'] or \
                    True,
            'geo': args.norm_geo or \
                   config_file['norm']['geo'] or \
                   False,
            'num': args.norm_num or \
                   config_file['norm']['num'] or \
                   True,
            'prof': args.norm_prof or \
                    config_file['norm']['prof'] or \
                    True
        }
    }

    # corpus = import_corpus.main(config)
    # print(corpus)
    # return

    # Models
    if config['run'] == 'dec':
        decision.main(config)
    elif config['run'] == 'naive':
        # naive.main(config)
        pass
    elif config['run'] == 'ner':
        # ner.main(config)
        pass
    elif config['run'] == 'rdf':
        random_forest.main(config)
    elif config['run'] == 'sgd':
        # sgd.main(config)
        pass
    elif config['run'] == 'svc':
        # svc.main(config)
        pass
    # Routines
    if config['run'] == 'analysis':
        # analysis.main(config)
        pass
    elif config['run'] == 'export':
        export.main(config)
    elif config['run'] == 'export-atf':
        export_atf.main(config)
    elif config['run'] == 'formatting':
        # formatting.main(config)
        pass
    elif config['run'] == 'testing':
        pytest.main(['tests/'])
    elif config['run'] == 'over-fit':
        overfit_check.main(config)


if __name__ == '__main__':
    main()
