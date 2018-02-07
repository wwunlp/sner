from scripts import professions, utilities
import codecs
import csv
import re
import argparse
import random
from classes import Display


left_features =  []

right_features = []

spelling_features = []

known_symbols = []

x_index = 0

def writeSparse(out_features, word_left, word_middle, word_right, x_index):
    """
    Writes a single x vector of features in a one hot inspired representation
      to the out_features file.

    Args:
      out_features = output file to write features
      word_left = the word left of the word to be output
      word_middle = the word in question
      word_right = the right context of the word to be output
      x_index = the row id for the feature entry
      
    Returns:
      Nothing

    Raises:
      None
      
    """

    offset = 0
    for i in range(len(left_features)):
        left = left_features[i]
        if word_left == left:
            out_features.write("{} {} 1\n".format(x_index, i + offset))
            
    offset = len(left_features)
    for i in range(len(right_features)):
        right = right_features[i]
        
        if word_right == right:
            out_features.write("{} {} 1\n".format(x_index, i + offset))
            
    offset = len(left_features) + len(right_features)
    for i in range(len(spelling_features)):
        spelling = spelling_features[i]
        if spelling in word_middle:
            out_features.write("{} {} 1\n".format(x_index, i + offset))

    offset = len(left_features) + len(right_features) + len(spelling_features)
    symbols = word_middle.split('-')
    out_features.write("{} {} {}\n".format(x_index, offset, len(symbols)))
    offset += 1
    foundSym = []
    for sym in symbols:
        if sym in known_symbols and not sym in foundSym:
            foundSym.append(sym)
            out_features.write("{} {} 1\n".format(x_index, known_symbols.index(sym) + offset))



def main(config):
    """
    Finds all names in options.attestations file, and goes through each word 
      in the main options.corpus file to create a sparse matrix file to be used
      with scikit learn.

    Args:
        options.norm_num = True to normalize numbers
        options.norm_prof = True to normalize professions
        options.norm_geo = True to normalize geographical names

    Returns:
        .csv file with the format:
            TabletID, LineID, LocationInSentence, Word, Word Type
        Word Types: '-' for unknowns.
                    'PN' to identify personal names.
                    'GN' to identify geographical names.
                    'PF' to identify professions.

    Raises:
        None

    """

    path = config['path']
    corpus = config['corpus']

    features_file = open(path + 'features.KEY', 'r')
    features = features_file.read().splitlines()

    i = 0
    while i < len(features):
        while features[i][:3] == '[L]':
            left_features.append(features[i][3:])
            i += 1
        while features[i][:3] == '[R]':
            right_features.append(features[i][3:])
            i += 1
        while features[i][:3] == '[S]':
            spelling_features.append(features[i][3:])
            i += 1

        if features[i] != '-word length-':
            known_symbols.append(features[i])
            i += 1
        else:
            i += 1


    global x_index
    known_pn = {}
    known_gn = {}

    file2 = codecs.open(path + corpus, 'r', encoding = 'utf-8')

    lines = file2.read().splitlines()

    out_features = open(path + 'features_atf.sparseX', "w")
    out_target = open(path + 'target_atf.RT', "w")
    out_key = open(path + 'target_atf.KEY', "w")
    x_index = 0

    tags = [
        '&',
        '#',
        '@',
        '$',
        '>'
    ]

    display = Display()
    display.start('Writing sparse matrix')

    i = 0
    tablet_id = 0
    while i < len(lines):
        line = lines[i]
        if "@tablet" in line:
            tablet_id += 1
        if not (len(line) > 0 and line[0] in tags):
            j = 0
            while (j < len(line) and line[j].isdigit()):
                j += 1

            if line[j:j + 2] == ". " or line[j:j + 3] == "'. ":
                k = line.index(' ')
                line = line[k + 1:]
                
                writeLine(
                    config,
                    line,
                    i,
                    out_features,
                    out_target,
                    out_key,
                    known_pn,
                    known_gn,
                    tablet_id
                )
        i += 1
        display.update_progress_bar(i, len(lines))


    display.finish()
    out_features.close()
    out_target.close()
    

def writeLine(config, line, line_id, out_features, out_target, out_key, known_pn, known_gn, tablet_id):
    norm_date = config['norm']['date']
    norm_geo  = config['norm']['geo']
    norm_num  = config['norm']['num']
    norm_prof = config['norm']['prof']
    
    global x_index

    # Clean up the line and ensure that there are no extra spaces
    text = utilities.clean_line(line.rstrip(), norm_num, norm_prof)
    text = text.lower()
    text = " ".join(text.split())
    text = text.strip()

    newText = text;
    words = text.split(' ')
    # change to line_id
    last_word = ""
    last_word_2 = ""
    last_line_id = ""
    last_tablet = ""
    last_index = -1
    
    last_name = False
    last_geo = False
        
    for i in range(len(words)):            
        w = words[i]
        w_type = "-"
        # Set types if they are known and avoid
        # conflicts by using the line_id.            
        if norm_prof and professions.replaceProfessions(w) == 'profession':
            if (w_type != "-"):
                print ("Warning, replacing name with profession!")
            w_type = "PF"
                
        if norm_num and 'number' in w:
            if (w_type != "-"):
                print ("Warning, overwriting a known type with number: ", w, " - ", w_type)
            w_type = "N"
            w = 'number'
        if norm_date and last_word == "iti":
            if (w_type != "-"):
                print ("Warning, overwriting a known type with date: ", w, " - ", w_type)
            w_type = "D"
            if (norm_date):
                w = 'date'
                    
        if not (i == 0 and (w == "" or w == "-" or w == "...")):
            if (i > 0 and i < len(words) -1):
                # write last word
                out_key.write("{0}, {1}, {2}, {3}\n".format(tablet_id, last_line_id, last_index, last_word))
                writeSparse(out_features, last_word_2, last_word, w, x_index)
                x_index += 1
            elif i == len(words) -1:
                #write last word
                out_key.write("{0}, {1}, {2}, {3}\n".format(tablet_id, last_line_id, last_index, last_word))
                writeSparse(out_features, last_word_2, last_word, w, x_index)
                x_index += 1
                #write current word
                out_key.write("{0}, {1}, {2}, {3}\n".format(tablet_id, line_id, i, w))
                writeSparse(out_features, last_word, w, "", x_index)                    
                x_index += 1
                    
        last_word_2 = last_word
        last_word = w
        last_line_id = line_id
        last_index = i
