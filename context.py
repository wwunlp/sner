#!/usr/bin/python3

# Mike Canoy
# Authored     5/3/2016
# Last updated 5/9/2016


left_rules = {}
right_rules = {}
skipped = {'lines' : 0}

def main(text, name):
    text = text.split(' ')
    if name in text:
        index = text.index(name)
        if index - 1 >= 0:
            left = text[index - 1]
            if left in left_rules.keys():
                left_rules[left] += 1
            else:
                left_rules[left] = 1
        if index + 1 <= len(text) - 1:
            right = text[index + 1]
            if right in right_rules.keys():
                right_rules[right] += 1
            else:
                right_rules[right] = 1
    else:
        skipped['lines'] += 1
