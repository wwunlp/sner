from scripts import professions, utilities
import codecs
import csv
import re
import argparse
import random

# To run: 
# python3 sner.py -r export -nn True -np True 


def findKnown(data, options, known_pn, known_gn):
    """
    Iterates through the attenstations file for personal and geographical names
     and adds the lineIDs in a list to the known_pn and known_gn dictionaries.
    Args:
        data (?)
        options (?)
        known_pn = { Personal name : line ID }, to be filled in.
        known_gn = { Geographical name : line ID}, to be filled in.

    Returns:
        Updates known_pn and known_gn dictionaries with the lineIDs.

    Raises:
        None

    """

    file = codecs.open(data.attestations, 'r', encoding = 'utf-8')
    # find all of the names
    for line in file:
        line = line.split(',')        
        text = utilities.clean_line(line[4].rstrip(), options.norm_num, options.norm_prof)
        text = text.lower()
        name = utilities.clean_line(line[5].rstrip(), options.norm_num, options.norm_prof)
        name = name.lower()
        line_id = line[1]
        line_id = re.sub("[L]", "", line_id)        

        if line[9].rstrip() == 'PN':
            if (name not in known_pn):
                known_pn[name] = [line_id]
            else :
                known_pn[name].append(line_id)
        if line[9].rstrip() == 'GN':
            if (name not in known_gn):
                known_gn[name] = [line_id]
                if (name in known_pn):
                    print ("Note: ", name, " is both a PN and GN.")
            else :
                known_gn[name].append(line_id)
            


left_features =  ['dumu','giri3', 'iti']
right_features = ['lugal-e','nubanda3']
spelling_features = ['ba-ni', 'a-da', 'a-na']
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
        if sym not in known_symbols:
            known_symbols.append(sym)
        if sym not in foundSym:
            foundSym.append(sym)
            out_features.write("{} {} 1\n".format(x_index, known_symbols.index(sym) + offset))



def main(data, options):
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
    global x_index
    known_pn = {}
    known_gn = {}
    findKnown(data, options, known_pn, known_gn)
    
    # iterate each line in Garshana Text and output to specified file
    file2 = codecs.open(data.corpus, 'r', encoding = 'utf-8')

    out_features = open('data/features_train.sparseX', "w")
    out_target = open('data/target_train.RT', "w")

    lines = file2.read().splitlines()
    end_train =  len(lines) * 0.3
    end_dev = len(lines) * 0.0
    x_index = 0
    
    while len(lines) > end_train:
        line = random.choice(lines)
        writeLine(options, line, out_features, out_target, known_pn, known_gn)
        lines.remove(line)

    out_features.close()
    out_target.close()
    out_features = open('data/features_dev.sparseX', "w")
    out_target = open('data/target_dev.RT', "w")
    x_index = 0
    
    while len(lines) > end_dev:
        line = random.choice(lines)
        writeLine(options, line, out_features, out_target, known_pn, known_gn)
        lines.remove(line)

    out_features.close()
    out_target.close()
    out_features = open('data/features_test.sparseX', "w")
    out_target = open('data/target_test.RT', "w")
    x_index = 0
    
    while len(lines) > 0:
        line = random.choice(lines)
        writeLine(options, line, out_features, out_target, known_pn, known_gn)
        lines.remove(line)
    
    writeKey()


def writeLine(options, line, out_features, out_target, known_pn, known_gn):
    global x_index
    line = line.split(',')
    if len(line) < 8:
        return
    tablet_id = line[0]

    # Clean up the line and ensure that there are no extra spaces
    text = utilities.clean_line(line[7].rstrip(), options.norm_num, options.norm_prof)
    text = text.lower()
    text = " ".join(text.split())
    text = text.strip()

    # We should skip the first line that labels the csv
    if "text" in text:
        return
        
    newText = text;
    words = text.split(' ')
    line_id = line[6]
    # skip description lines
    if line_id == "":
        return
    # change to line_id
    line_id = line[4]
    line_id = re.sub("[L]", "", line_id)
    last_word = ""
    last_word_2 = ""
    last_name = False
    last_geo = False
        
    if "'" in line_id:
        line_id = re.sub("[']", "", line_id)
        line_id = "'" + line_id
    for i in range(len(words)):            
        w = words[i]
        w_type = "-"
        # Set types if they are known and avoid
        # conflicts by using the line_id.            
        if w in known_pn:
            if (line_id in known_pn[w]):
                w_type = "PN"
        if w in known_gn:
            if (line_id in known_gn[w]):
                if (w in known_pn and w_type != "-"):
                    print("Warning, replacing PN with GN!")
                w_type = "GN"
                if (options.norm_geo):
                    w = "geoname"
        if professions.replaceProfessions(w) == 'profession':
            if (w_type != "-"):
                print ("Warning, replacing name with profession!")
            w_type = "PF"
                
        if 'number' in w:
            if (w_type != "-"):
                print ("Warning, overwriting a known type with number: ", w, " - ", w_type)
            w_type = "N"
            w = 'number'
        if last_word == "iti":
            if (w_type != "-"):
                print ("Warning, overwriting a known type with date: ", w, " - ", w_type)
            w_type = "D"
            if (options.norm_date):
                w = 'date'
                    
        if not (i == 0 and (w == "" or w == "-" or w == "...")):
            if (i > 0 and i < len(words) -1):
                # write last word
                writeSparse(out_features, last_word_2, last_word, w, x_index)
                writeTarget(out_target, last_name, last_geo)
                x_index += 1
            elif i == len(words) -1:
                #write last word
                writeSparse(out_features, last_word_2, last_word, w, x_index)
                writeTarget(out_target, last_name, last_geo)
                x_index += 1
                #write current word
                writeSparse(out_features, last_word, w, "", x_index)                    
                writeTarget(out_target, w_type == "PN", w_type == "GN")
                x_index += 1
                    
        last_word_2 = last_word
        last_word = w
        if w_type == "PN":
            last_name = True
        else:
            last_name = False
        if w_type == "GN":
            last_geo = True
        else:
            last_geo = False 

def writeTarget(out_target, isName, isGN):
    if isName:
        out_target.write("1\n")
    elif isGN:
        out_target.write("2\n")
    else:
        out_target.write("0\n")
        
def writeKey():
    out = open('data/features.KEY', "w")

    offset = 0
    
    for i in range(len(left_features)):
        out.write(left_features[i])
        out.write("\n")
    for i in range(len(right_features)):
        out.write(right_features[i])
        out.write("\n")
    for i in range(len(spelling_features)):
        out.write(spelling_features[i])
        out.write("\n")

    out.write("-word length-\n")

    for i in range(len(known_symbols)):
        out.write(known_symbols[i])
        out.write("\n")
                

if __name__ == '__main__':    
    main()
