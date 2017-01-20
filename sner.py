"""
Sumerian Named Entity Recognition: sner.py

This file bootstraps the program, parsing arguments and configuration file.
Also offers interface for our analysis and formatting tools and test functions.
"""
import argparse
import json
import os
import pytest
from classes import Data, Options
from models import ner, random_forest
from scripts import analysis, export, formatting


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

    parser.add_argument('-r', '--run', help='Run either the [ner] or [rdf] '
                        'model, or one of the following routines: '
                        '[analysis], [export], [formatting], or [testing].',
                        required=False, choices=['ner', 'rdf',
                                                 'analysis', 'export',
                                                 'formatting', 'testing'])


    parser.add_argument('-c', '--corpus', help='Path to corpus file',
                        required=False)
    parser.add_argument('-a', '--attestations', help='Path to attestations '
                        'file', required=False)
    parser.add_argument('-sr', '--seed-rules', help='Path to seed rules file',
                        required=False)
    parser.add_argument('-o', '--output', help='Path to output file',
                        required=False)
    parser.add_argument('-l', '--log', help='Path to log file', required=False)


    parser.add_argument('-i', '--iterations', help='Number of iterations',
                        type=int, required=False)
    parser.add_argument('-mr', '--max-rules', help='Max number of rules per '
                        'iterations', type=int, required=False)
    parser.add_argument('-mf', '--mod-freq', help='Modifier of rule frequency',
                        type=float, required=False)
    parser.add_argument('-ms', '--mod-str', help='Modifier of rule strength',
                        type=float, required=False)
    parser.add_argument('-at', '--accept-threshold', help='Name acceptance '
                        'threshold', type=float, required=False)
    parser.add_argument('-al', '--alpha', help='Alpha value', type=float,
                        required=False)
    parser.add_argument('-k', '--k', help='K value', type=float, required=False)


    parser.add_argument('-nn', '--norm-num', help='Enable the normalization '
                        'of numbers', type=bool, required=False)
    parser.add_argument('-np', '--norm-prof', help='Enable the normalization '
                        'of professions', type=bool, required=False)
    parser.add_argument('-ng', '--norm-geo', help='Enable the normalization '
                        'of geographic names', type=bool, required=False)
    parser.add_argument('-nd', '--norm-date', help='Enable the normalization '
                        'of dates', type=bool, required=False)
    parser.add_argument('-na', '--norm-all', help='Enable the normalization '
                        'of everything', type=bool, required=False)


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

    config_path = os.environ.get('SNER_CONF') or 'sner.conf'
    config_file = open(config_path)
    config = json.load(config_file)

    parser = argparse.ArgumentParser()
    add_args(parser)
    args = parser.parse_args()

    run = args.run or config['run'] or 'ner'

    data = Data(
        corpus=args.corpus or \
               config['corpus'] or \
               'data/corpus.csv',
        attestations=args.attestations or \
                     config['attestations'] or \
                     'data/attestations.csv',
        seed_rules=args.seed_rules or \
                   config['seed-rules'] or \
                   'data/seed_rules.csv',
        train='data/train.RT',
        dev='data/dev.RT',
        test='data/test.RT',
        output=args.output or \
               config['output'] or \
               'data/output.csv',
        log=args.log or \
            config['log'] or \
            'data/log.csv'
    )

    options = Options(
        iterations=args.iterations or \
                   config['iterations'] or \
                   5,
        max_rules=args.max_rules or \
                  config['max-rules'] or \
                  5,
        mod_freq=args.mod_freq or \
                 config['mod-freq'] or \
                 0.0,
        mod_str=args.mod_str or \
                config['mod-str'] or \
                1.0,
        accept_threshold=args.accept_threshold or \
                         config['accept-threshold'] or \
                         0.9,
        alpha=args.alpha or \
              config['alpha'] or \
              0.1,
        k=args.k or \
          config['k'] or \
          2.0,
        norm_num=args.norm_num or \
                 args.norm_all or \
                 config['norm-num'] or \
                 False,
        norm_prof=args.norm_prof or \
                  args.norm_all or \
                  config['norm-prof'] or \
                  False,
        norm_geo=args.norm_geo or \
                 args.norm_all or \
                 config['norm-geo'] or \
                 False,
        norm_date=args.norm_date or \
                  args.norm_all or \
                  config['norm-date'] or \
                  False
    )

    if run == 'ner':
        ner.main(data, options)
    elif run == 'rdf':
        random_forest.main(data, options)
    elif run == 'analysis':
        analysis.main(data, options)
    elif run == 'export':
        export.main(data, options)
    elif run == 'formatting':
        formatting.main(data, options)
    elif run == 'testing':
        pytest.main(['tests/'])

if __name__ == '__main__':
    main()
