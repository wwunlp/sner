#!/usr/bin/python3

# Mike Canoy
# Authored     5/3/2016
# Last Updated 5/9/2016

import context
import names
import spelling
import utilities
import codecs
import csv


def main():
    file = codecs.open('Garshana Dataset/Attestations_PNs_GNs.csv',
            'r', encoding = 'utf-16')
    for line in file:
        line = line.split(',')
        text = utilities.clean_line(line[4].rstrip())
        name = line[5].rstrip()
        if name in names.personal:
            names.personal[name] += 1
        else:
            names.personal[name] = 1
        context.main(text, name)
        spelling.main(name)

    word_count, syll_count = utilities.get_counts()
    rules_collection = [
            [context.left_rules,  word_count, 'Left'],
            [context.right_rules, word_count, 'Right'],
            [spelling.rules,      syll_count, 'Spelling']]

    with open('Results.csv', 'w', newline = '',
            encoding = 'utf-16') as csvfile:
        fieldnames = [
                'Context',
                'Rule',
                'Occurrence',
                'Total Occurrence',
                'Percentage']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for rules in rules_collection:
            for rule in rules[0]:
                if rule in rules[1]:
                    total = rules[1][rule]
                    percent = float(rules[0][rule]) / float(total)
                    writer.writerow({
                        'Context'          : rules[2],
                        'Rule'             : rule,
                        'Occurrence'       : str(rules[0][rule]),
                        'Total Occurrence' : str(total),
                        'Percentage'       : str(percent)})


if __name__ == '__main__':
    main()
