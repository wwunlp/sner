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
    file = codecs.open('Garshana Dataset/Attestations_PNs.csv',
                       'r', encoding='utf-16')
    for line in file:
        line = line.split(',')
        if line[9].rstrip() == 'PN':
            text = utilities.clean_line(line[4].rstrip())
            name = utilities.clean_line(line[5].rstrip())
            if name in names.personal:
                names.personal[name] += 1
            else:
                names.personal[name] = 1
            context.main(text, name)

    word_count, syll_count = utilities.get_counts()
    rules_collection = [
            [context.left_rules,  word_count, 'Left'],
            [context.right_rules, word_count, 'Right']]

    # Do spelling analysis
    spelling.main(syll_count)

    with open('results/context.csv', 'w', newline='',
              encoding='utf-16') as csvfile:
        fieldnames = [
                'Context',
                'Rule',
                'Occurrence',
                'Total Occurrence',
                'Percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for rules in rules_collection:
            for rule in rules[0]:
                if rule in rules[1]:
                    total = rules[1][rule]
                    percent = float(rules[0][rule]) / float(total)
                    writer.writerow({
                        'Context': rules[2],
                        'Rule': rule,
                        'Occurrence': str(rules[0][rule]),
                        'Total Occurrence': str(total),
                        'Percentage': str(percent)})

    with open('results/varients.csv', 'w', newline='',
              encoding='utf-16') as csvfile:
        fieldnames = [
                'Name',
                'Varients']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for name in context.varients.keys():
            writer.writerow({
                'Name': name,
                'Varients': str(context.varients[name])})

    with open('results/namesperrule.csv', 'w', newline='',
              encoding='utf-16') as csvfile:
        fieldnames = ['Rule', 'Name', 'Occurrences']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rule in context.rules:
            for name in context.rules[rule]:
                writer.writerow({
                    'Rule': rule,
                    'Name': name,
                    'Occurrences': str(context.rules[rule][name])})

if __name__ == '__main__':
    main()
