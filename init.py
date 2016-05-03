#!/usr/bin/python3

# Mike Canoy
# Authored 5/3/2016

import context
import rules
import spelling
import utilities
import codecs

personal_names = {}


def main():
    file = codecs.open('Garshana Dataset/Texts.csv',
            'r', encoding = 'utf-16')
    for line in file:
        line = line.split(',')
        line = line[7].rstrip()
        context.init(line, personal_names)
    # Testing
    word_count, syll_count = utilities.get_counts()
    for name in personal_names:
        print(name + ' : ' + str(personal_names[name]))
    for rule in rules.left_context:
        print(rule + ' : ' + str(rules.left_context[rule]))
        print(str(rules.left_context[rule] / word_count[rule]))
    for rule in rules.right_context:
        print(rule + ' : ' + str(rules.right_context[rule]))
        print(str(rules.right_context[rule] / word_count[rule]))

if __name__ == '__main__':
    main()
