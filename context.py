#!/usr/bin/python3

# Mike Canoy
# Authored     5/3/2016
# Last updated 5/9/2016

import editdistance

left_rules = {}
right_rules = {}
skipped = {'lines' : 0}

def main(text, name):
    skip = True
    text = text.split(' ')
    for word in text:
        if editdistance.eval(name, word) < 5:
            skip = False
            index = text.index(word)
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
    
    if skip:
        skipped['lines'] += 1
        if name in skipped.keys():
            skipped[name] += 1
        else:
            skipped[name] = 1
