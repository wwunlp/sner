"""
Sumerian Named Entity Recognition: sner.py

This file bootstraps the program, parsing arguments and configuration file.
Also offers interface for our analysis and formatting tools and test functions.
"""
import argparse
import json
import os
import pytest
from models import ner, sklearn_launcher
from scripts import export, export_atf, overfit_check # analysis, export, formatting


def bool_check(arg, config, default):
    """Return bool from `arg` or `config` str, or `default` bool.

    Arguments from the parser and configuration file are represented as strings.
    Arguments that represent boolean values need string compares, and then
    return the actual boolean object.

    Args:
        arg (str):
        config (str):
        default (bool):

    Returns:
        True, False, or default (bool):

    Raises:
        TypeError
    """

    if arg:
        if arg == 'True':
            return True
        elif arg == 'False':
            return False
        else:
            raise TypeError
    elif config:
        if config == 'True':
            return True
        elif config == 'False':
            return False
        else:
            raise TypeError
    else:
        return default



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
        help='Run one of the following models: '
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
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-ng',
        '--norm-geo',
        help='Enable geographical name normalization',
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-nn',
        '--norm-num',
        help='Enable number normalization',
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-np',
        '--norm-prof',
        help='Enable profession normalization',
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-dn',
        '--disjoint-names',
        help='Export train / dev with disjoint unique name sets',
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-el',
        '--export-left-rules',
        help='Export uses hardcoded left context rules',
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-er',
        '--export-right-rules',
        help='Export uses hardcoded right context rules',
        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-es',
        '--export-spelling-rules',
        help='Export uses hardcoded spelling rules',

        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-ef',
        '--export-found',
        help='Export creates features out of found syllables',
        required=False,
        choices=['True', 'False']
        
    )
    parser.add_argument(
        '-atf',
        '--use-atf',
        help='Enables use of the atf files for the scikit models',

        required=False,
        choices=['True', 'False']
    )
    parser.add_argument(
        '-ds',
        '--dev-size',
        help='Percentage for exporter to use for dev set. 0 > size >= 1',
        type=float,
        required=False
    )
    parser.add_argument(
        '-ts',
        '--train-size',
        help='Percentage for exporter to use for train set. 0 > size >= 1',
        type=float,
        required=False
    )
    parser.add_argument(
        '-vb',
        '--verbose',
        help='Verbose output.',
        required=False,
        choices=['True', 'False']
        
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
            },
            'params': {
                'alpha': '',
                'C': '',
                'criterion': '',
                'degree': '',
                'kernel': '',
                'loss': '',
                'max_features': '',
                'max_depth': '',
                'min_samples_split': '',
                'max_leaf_nodes': '',
                'min_samples_leaf': '',
                'n_estimators': '',
                'penalty': '',
                'splitter': ''
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
        'train_size': args.train_size or \
             0.7,
        'dev_size': args.dev_size or \
             0.3,
        'flags': {
            'disjoint_names': bool_check(
                args.disjoint_names,
                None,
                False
            ),
            'use_left_context': bool_check(
                 args.export_left_rules,
                None,
                False
            ),            
            'use_right_context': bool_check(
                args.export_right_rules,
                None,
                False
            ),
            'use_spelling': bool_check(
                args.export_spelling_rules,
                None,
                False
            ),
            'use_syllables': bool_check(
                 args.export_found,
                None,
                True
            ),
            'verbose': bool_check(
                 args.verbose,
                None,
                False
            ),
            'use_atf': bool_check(
                 args.use_atf,
                None,
                False
            )
        },
        'norm': {
            'date': bool_check(
                args.norm_date,
                config_file['norm']['date'],
                False
            ),
            'geo': bool_check(
                args.norm_geo,
                config_file['norm']['geo'],
                False
            ),
            'num': bool_check(
                args.norm_num,
                config_file['norm']['num'],
                True
            ),
            'prof': bool_check(
                args.norm_prof,
                config_file['norm']['prof'],
                True
            )
        },
        'params': {
            'alpha': config_file['params']['alpha'] or \
                     0.503706954708716,
            'C': config_file['params']['C'] or \
                 1.67640892878145,
            'criterion': config_file['params']['criterion'] or \
                         'gini',
            'degree': config_file['params']['degree'] or \
                      4,
            'kernel': config_file['params']['kernel'] or \
                      'linear',
            'loss': config_file['params']['loss'] or \
                    'squared_hinge',
            'max_features': config_file['params']['max_features'] or \
                            None,
            'max_depth': config_file['params']['max_depth'] or \
                         None,
            'min_samples_split': config_file['params']['min_samples_split'] or \
                                 2,
            'max_leaf_nodes': config_file['params']['max_leaf_nodes'] or \
                              None,
            'min_samples_leaf': config_file['params']['min_samples_leaf'] or \
                                1,
            'n_estimators': config_file['params']['n_estimators'] or \
                            480,
            'penalty': config_file['params']['penalty'] or \
                       'elasticnet',
            'splitter': config_file['params']['splitter'] or \
                        'best'
        }
    }

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
    # Models
    else:
        sklearn_launcher.main(config)


if __name__ == '__main__':
    main()
