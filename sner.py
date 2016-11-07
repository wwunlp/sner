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
                        '[unsupervised], or [supervised] routines',
                        required=False, choices=['analysis', 'formatting', 
                        'unsupervised', 'supervised'], default='supervised')
    parser.add_argument('-c', '--corpus', help='Location of corpus file',
                        required=False)
    parser.add_argument('-a', '--attestations', help='Location of attestations '
                        'file', required=False)
    parser.add_argument('-sr', '--seed-rules', help='Location of seed rules '
                        'file', required=False)
    parser.add_argument('-o', '--output', help='Location of output file',
                        required=False)
    parser.add_argument('-i', '--iterations', help='Number of iterations',
                        required=False)
    parser.add_argument('-mr', '--max-rules', help='Max number of rules per '
                        'iterations', required=False)
    
    parser.add_argument('-nt', '--name-tag', help='The formating for names, '
                        'default is $PN$', required=False)
    parser.add_argument('-nn', '--norm-num', help='Enable the nomralization '
                        'of numbers', required=False)
    parser.add_argument('-np', '--norm-prof', help='Enable the normalization '
                        'of professions', required=False)
    parser.add_argument('-lt', '--left-tag', help='Left tag of a sentence, '
                        'default blank', required=False)
    parser.add_argument('-rt', '--right-tag', help='Right tag of a sentence, '
                        'default newline', required=False)
    parser.add_argument('-t', '--tablet', help='Add start of tablet line, '
                        'default False', required=False)
    parser.add_argument('-m', '--mode', help='Switch between [csv] and '
                        '[multiline] modes, default csv', required=False, 
                        choices=['csv', 'multiline'])


def main():
    """
    
    """

    config_loc = os.environ.get('SNER_CONF') or 'sner.conf'
    config_file = open(config_loc)
    config = json.load(config_file)

    parser = argparse.ArgumentParser()
    add_args(parser)
    args = parser.parse_args()

    run = args.run or config['run'] or 'supervised'
    corpus = args.corpus or config['corpus'] or 'data/corpus.csv'
    attestations = args.attestations or config['attestations'] or \
        'data/attestations.csv'
    seed_rules = args.seed_rules or config['seed-rules'] or \
        'data/seed_rules.csv'
    output = args.output or config['output'] or 'data/output.csv'
    
    iterations = args.iterations or config['iterations'] or 5
    max_rules = args.max_rules or config['max-rules'] or 5
    name_tag = args.name_tag or config['name-tag'] or '$PN$'
    norm_num = args.norm_num or config['norm-num'] or False
    norm_prof = args.norm_prof or config['norm-prof'] or False
    left_tag = args.left_tag or config['left-tag'] or ''
    right_tag = args.right_tag or config['right-tag'] or '\n'
    tablet = args.tablet or config['tablet'] or False
    mode = args.mode or config['mode'] or 'csv'
    
    data = Data(corpus, attestations, seed_rules, output)

    options = Options(iterations, max_rules, name_tag, norm_num,
                      norm_prof, left_tag, right_tag, tablet, mode)

    if run== 'analysis':
        analysis.main(data, options)
    elif run == 'formatting':
        formatting.main(data, options)
    elif run == 'unsupervised':
        os.chdir('unsupervised-old/')
        subprocess.run('./run.sh')
    elif run == 'supervised':
        ner.main(data, options)

if __name__ == '__main__':
    main()
