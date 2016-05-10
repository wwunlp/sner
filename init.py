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
        if name in names.personal.keys():
            names.personal[name] += 1
        else:
            names.personal[name] = 1
        context.main(text, name)

    word_count, syll_count = utilities.get_counts()

    with open('Results.csv', 'w', newline = '',
            encoding = 'utf-16') as csvfile:
        fieldnames = ['Context', 'Rule', 'Occurrence',
                'Total Occurrence', 'Percentage']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for rule in context.left_rules:
            if rule in word_count:
                total = word_count[rule]
                percent = float(context.left_rules[rule]) / float(total)
                writer.writerow({
                    'Context' : 'Left',
                    'Rule' : rule,
                    'Occurrence' : str(context.left_rules[rule]),
                    'Total Occurrence' : str(total),
                    'Percentage' : str(percent)})

        for rule in context.right_rules:
            if rule in word_count:
                total = word_count[rule]
                percent = float(context.right_rules[rule]) / float(total)
                writer.writerow({
                    'Context' : 'Right',
                    'Rule' : rule,
                    'Occurrence' : str(context.right_rules[rule]),
                    'Total Occurrence' : str(total),
                    'Percentage' : str(percent)})


if __name__ == '__main__':
    main()
