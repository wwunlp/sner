from classes import Data, Options
from models import ner
from scripts import analysis, formatting
import argparse
import json
import os
import subprocess


def add_args(parser):
    """
    Args:
        parser

    Returns:
        None

    Raises:
        None
    """
    
    parser.add_argument('-r', '--run', help='Run [analysis], [formatting], '
                        '[unsupervised-old], or [ner] routines',
                        required=False, choices=['analysis', 'formatting', 
                        'unsupervised-old', 'ner'])
    parser.add_argument('-c', '--corpus', help='Location of corpus file',
                        required=False)
    parser.add_argument('-a', '--attestations', help='Location of attestations '
                        'file', required=False)
    parser.add_argument('-sr', '--seed-rules', help='Location of seed rules '
                        'file', required=False)
    parser.add_argument('-o', '--output', help='Location of output file',
                        required=False)
    
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

    parser.add_argument('-nn', '--norm-num', help='Enable the nomralization '
                        'of numbers', type=bool, required=False)
    parser.add_argument('-np', '--norm-prof', help='Enable the normalization '
                        'of professions', type=bool, required=False)
    parser.add_argument('-ng', '--norm-geo', help='Enable the normalization '
                        'of geographic names', type=bool, required=False)


def main():
    """
    
    """

    config_loc = os.environ.get('SNER_CONF') or 'sner.conf'
    config_file = open(config_loc)
    config = json.load(config_file)

    parser = argparse.ArgumentParser()
    add_args(parser)
    args = parser.parse_args()

    run = args.run or config['run'] or 'ner'
    corpus = args.corpus or config['corpus'] or 'data/corpus.csv'
    attestations = args.attestations or config['attestations'] or \
        'data/attestations.csv'
    seed_rules = args.seed_rules or config['seed-rules'] or \
        'data/seed_rules.csv'
    output = args.output or config['output'] or 'data/output.csv'
    
    iterations = args.iterations or config['iterations'] or 5
    max_rules = args.max_rules or config['max-rules'] or 5
    mod_freq = args.mod_freq or config['mod-freq'] or 0.0
    mod_str = args.mod_str or config['mod-str'] or 1.0
    accept_threshold = args.accept_threshold or config['accept-threshold'] or \
        0.9
    
    norm_num = args.norm_num or config['norm-num'] or False
    norm_prof = args.norm_prof or config['norm-prof'] or False
    norm_geo = args.norm_geo or config['norm-geo'] or False

    
    data = Data(corpus, attestations, seed_rules, output)

    options = Options(iterations, max_rules, mod_freq, mod_str,
                      accept_threshold, norm_num, norm_prof,
                      norm_geo)

    if run== 'analysis':
        analysis.main(data, options)
    elif run == 'formatting':
        formatting.main(data, options)
    elif run == 'unsupervised-old':
        os.chdir('models/unsupervised-old/')
        subprocess.run('./run.sh')
    elif run == 'ner':
        ner.main(data, options)

if __name__ == '__main__':
    main()
