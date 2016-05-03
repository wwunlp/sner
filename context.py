#!/usr/bin/python3

# Mike Canoy
# Authored 5/3/2016

import rules


def init(line, personal_names):
    line = line.split(' ')
    index = 0
    for word in line:
        context('left', line, index - 1, personal_names)
        context('right', line, index + 1, personal_names)
        index += 1

def context(case, line, index, personal_names):
    if index < 0 or index > len(line) - 1:
        pass
    else:
        if case is 'left':
            context_rules = rules.left_context
        elif case is 'right':
            context_rules = rules.right_context 
        if line[index] in context_rules:
            context_rules[line[index]] += 1
            if case is 'left':
                index += 1
            elif case is 'right':
                index -= 1
            if line[index] in personal_names.keys():
                personal_names[line[index]] += 1
            else:
                personal_names[line[index]] = 1
