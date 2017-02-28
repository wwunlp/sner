#!/usr/bin/python3

# Mike Canoy
# Authored     5/3/2016
# Last updated 2/25/2017

import editdistance

left_rules = {}
right_rules = {}
varients = {}
rules = {}               # {rules : {namesperrule : occurrence}}


def main(text, name):
    """
    Args:
        text = line from corpus split into array split on ' '
        name = the PN found in this line

    Returns:
        None (?)
        Probably fills left_rules and right_rules dicts

    Raises:
        None

    """

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

        if left not in rules:
            rules[left] = {name: 1}
        elif left in rules and name not in rules[left].keys():
            rules[left].update({name: 1})
        elif left in rules and name in rules[left].keys():
            rules[left][name] += 1

    if index + 1 <= len(text) - 1:
        right = text[index + 1]
        if right in right_rules.keys():
            right_rules[right] += 1
        else:
            right_rules[right] = 1

        if right not in rules:
            rules[right] = {name: 1}
        elif right in rules and name not in rules[right].keys():
            rules[right].update({name: 1})
        elif right in rules and name in rules[right].keys():
            rules[right][name] += 1
