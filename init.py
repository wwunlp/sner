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

        '''
        for word in text:
            if word is name:
                isName = 1
            else:
                isName = 0
            if '-' in word:
                word = word.split('-')
                for gram in word:
                    spelling.addMonogram(gram, isName)
        '''

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

        for rule in spelling.rules:
            if rule in syll_count:
                total = syll_count[rule]
                percent = float(spelling.rules[rule]) / float(total)
                writer.writerow({
                    'Context' : 'Spelling',
                    'Rule' : rule,
                    'Occurrence' : str(spelling.rules[rule]),
                    'Total Occurrence' : str(total),
                    'Percentage' : str(percent)})

        '''
        for gram in spelling.monograms:
            # if gram in syll_count:
                total = spelling.monograms[gram][0] # syll_count[gram]
                percent = float(spelling.monograms[gram][1]) / float(total)
                writer.writerow({
                    'Context' : 'Spelling',
                    'Rule' : gram,
                    'Occurrence' : str(spelling.monograms[gram]),
                    'Total Occurrence' : str(total),
                    'Percentage' : str(percent)})

        for gram in spelling.bigrams:
            if gram in syll_count:
                total = syll_count[gram]
                percent = float(spelling.bigrams[gram][1]) / float(total)
                writer.writerow({
                    'Context' : 'Spelling',
                    'Rule' : gram,
                    'Occurrence' : str(spelling.bigrams[gram]),
                    'Total Occurrence' : str(total),
                    'Percentage' : str(percent)})

        for gram in spelling.trigrams:
            if gram in syll_count:
                total = syll_count[gram]
                percent = float(spelling.trigrams[gram][1]) / float(total)
                writer.writerow({
                    'Context' : 'Spelling',
                    'Rule' : gram,
                    'Occurrence' : str(spelling.trigrams[gram]),
                    'Total Occurrence' : str(total),
                    'Percentage' : str(percent)})
        '''


if __name__ == '__main__':
    main()
