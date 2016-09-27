#!/usr/bin/python3

# Mike Canoy
# Authored     5/3/2016
# Last updated 5/9/2016

import editdistance

left_rules = {}
right_rules = {}
varients = {}

def main(text, name):
    text = text.split(' ')
    edit_distance = []
    for word in text:
        edit_distance.append(editdistance.eval(name, word))

    index = edit_distance.index(min(edit_distance))    
    varient = text[index]
    if name != varient:
        if name in varients.keys():
            if varient not in varients[name]:
                varients[name].append(varient)
        else:
            varients[name] = [varient]

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

