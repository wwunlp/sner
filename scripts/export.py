from scripts import professions, utilities
import codecs
import csv
import re
import argparse
import random


uniqueNames = True

# To run: 
# python3 sner.py -r export -nn True -np True 


def findKnown(config, known_pn, known_gn):
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
    path = config['path']
    norm_num = config['norm']['num']
    norm_prof = config['norm']['prof']

    file = codecs.open(path + 'attestations.csv', 'r', encoding = 'utf-8')
    # find all of the names
    for line in file:
        line = line.split(',')        
        text = utilities.clean_line(line[4].rstrip(), norm_num, norm_prof)
        text = text.lower()
        name = utilities.clean_line(line[5].rstrip(), norm_num, norm_prof)
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
            

left_features = []
left_features_phase1 =  ['dumu','giri3', 'iti',
                  'u3',
                  'arad2',
                  'gurum2',
                  'en-nu',
                  'zi-ga',
                  'igi',
                  'im-sumur',
                  'in-u',
                  'du-u2-um',
                  'i7',
                  'gu2-gal',
                  'a2-bi',
                  'a-ga2-ri-na',
                  'puzur4-a-ku-um',
                  'tu7',
                  'nig2-gu2-na',
                  '{giš}garigx',
                  'nig2-lam2',
                  'sag',
                  'ki-a-nag',
                  '{tug2}nig2-lam2-ab',
                  '{na4}profession',
                  '{gi}dur-gazi',
                  'nig2-kas7',
                  'bara2',
                  'i3-giš-bara2',
                  'kaskal',
                  'gar3-da-hi-še3',
                  'kab2',
                  'tug2-ba',
                  '{giš}u3-suh5-sig',
                  '{gi}ma-an-sim',
                  'nig2-ar3-ra',
                  '{gi}gur5',
                  'udug',
                  '{tug2}bar-dul5-ab']
right_features = []
right_features_phase1 = ['lugal-e','nubanda3',
                  'dub-sar',
                  'arad2-zu',
                  'ašgab',
                  'nu-banda3',
                  'a-zu',
                  'e2-šim×gar',
                  'al-tar',
                  'a2-ag2-ga2',
                  'geme2-arad2',
                  'al-nag4-ga2',
                  '{d}nin-{d}si4-an-na',
                  '1-kam',
                  '2-kam',
                  'a-ra2',
                  'e2-uš-bar',
                  'lu2-kin-gi4-a',
                  'e2-da-na{ki}-še3',
                  '3-kam',
                  'ba-ra-šeg6',
                  '{dug}utul2',
                  'e2-kišib-ba-še3',
                  'ša3-du',
                  'hun-ga2-e-ne',
                  'ka',
                  'ga2-nun-še3',
                  'ki-a-nag',
                  'ki-mu-ra',
                  'si-ga',
                  'e2-uš-bar-še3',
                  '4-kam',
                  'diri-ga',
                  'kurušda',
                  'alan',
                  '1-sila3',
                  'ma-ma-šar-ra-at',
                  'za3-gu2-la2',
                  'du11-ga',
                  '{d}šu-{d}suen-e-te-el2-ka-{d}en-lil2',
                  'lu2-kas4',
                  'šuš3']

spelling_features = []
spelling_features_phase1 = ['i3-li',
                     'i3-li2',
                     'kab-ta',
                     'kab-ta2',
                     'a-ra',
                     'ra-a',
                     'a-bi',
                     '{d}nin-kar',
                     'ra-am',
                     'kar3',
                     'ta2-kar3',
                     'am-i3',
                     'ra-am-i3',
                     'na-ah',
                     'sig5',
                     'ah-i3-li2',
                     'na-ah-i3',
                     'ah-i3',
                     'na-ra',
                     'na-ra-am',
                     'li2-a',
                     'bi2-a',
                     'a-li2',
                     'li2-i3',
                     'a-me',
                     'ar3-ra',
                     'nig2-ar3',
                     'nig2-ar3-ra',
                     'ra-sig5',
                     'ar3-ra-sig5',
                     'ba-ba',
                     'li2-bi',
                     'la-ni',
                     'sa2-a',
                     'bi-la',
                     'ra-ni',
                     'bi-la-ni',
                     'li2-bi-la',
                     'at-i3',
                     'ki-sa2',
                     'ta2-ki',
                     'si-ru',
                     'si-ru-um',
                     'li2-um',
                     'li2-an.dul3',
                     'duru5-sig5',
                     'li2-aš-ra',
                     'aš-ra-ni',
                     'aš-ra',
                     'li2-aš',
                     'ki-ru',
                     'ta2-ki-ru',
                     'ki-ru-um',
                     'ba-ra',
                     'gašam-e',
                     'gašam-e-ne',
                     'ba-ak',
                     'duru5-kab-bi',
                     'kab-bi',
                     'duru5-kab',
                     'li2-um{ki}',
                     'ur2-i3',
                     'uz-ra-ni',
                     'za-gar3',
                     'sa2-ab',
                     'li2-uz-ra',
                     'li2-uz',
                     'uz-ra',
                     'ši-ru',
                     'bi2-za',
                     'gur11',
                     'u4-11',
                     'li2-tu',
                     'ga-li2']

known_symbols = []

test_names = set()
dev_names = set()

def writeSparse(config, out_features, word_left, word_middle, word_right, x_index):
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

    # write number of syllables
    offset = len(left_features) + len(right_features) + len(spelling_features)
    symbols = word_middle.split('-')
    out_features.write("{} {} {}\n".format(x_index, offset, len(symbols)))
    offset += 1
    
    if config['flags']['use_syllables'] == False:
        return
    
    foundSym = []
    for sym in symbols:
        if sym not in known_symbols:
            known_symbols.append(sym)
        if sym not in foundSym:
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
    global left_features
    global right_features
    global spelling_features
    global uniqueNames
    path = config['path']
    corpus = config['corpus']

    if config['norm']['date']:
        print("Normalizing dates!")
    if config['norm']['geo']:
        print("Normalizing geo names!")
    if config['norm']['num']:
        print("Normalizing numbers.")
    if config['norm']['prof']:
        print("Normalizing professions.")
        
    flags = config['flags']
    if flags['disjoint_names'] == True:
        uniqueNames = True
        print("Using disjoint name sets for train / dev.")
    else:
        uniqueNames = False

    if flags['use_left_context'] == True:
        left_features = left_features_phase1
        print("Using left context from phase 1.")        
    else:
        left_features = []
        
    if flags['use_right_context'] == True:
        print("Using right context from phase 1.")
        right_features = right_features_phase1
    else:
        right_features = []
        
    if flags['use_spelling'] == True:
        print("Using spelling rules from phase 1.")
        spelling_features = spelling_features_phase1
    else:
        spelling_features = []

    if flags['use_syllables'] == True:
        print("Using unique syllables as features.")
    

    known_pn = {}
    known_gn = {}
    findKnown(config, known_pn, known_gn)
    
    # iterate each line in Garshana Text and output to specified file
    file2 = codecs.open(path + corpus, 'r', encoding = 'utf-8')


    dev_size = config['dev_size']
    train_size = config['train_size']

    if dev_size + train_size > 1.001 or dev_size < 0 or train_size < 0:
        print(dev_size, train_size)
        print("Invalid dev or train size! Expecting both to be 0-1 and dev+train <= 1.")
        return

    
    test_size = 1 - (dev_size + train_size)
        
    lines = file2.read().splitlines()
    end_train =  len(lines) * train_size
    end_dev = len(lines) * dev_size
    end_test = len(lines) * test_size

    
    print ("Train size: %.2f%% %d lines" % (train_size,end_train))
    print ("Dev size: %.2f%% %d lines" % (dev_size,end_dev))
    print ("Test size: %.2f%% %d lines" % (test_size,end_test))

    out_features = open('data/features_train.sparseX', "w")
    out_target = open('data/target_train.RT', "w")
    out_key = open('data/target_train.KEY', "w")

    out_features2 = open('data/features_dev.sparseX', "w")
    out_target2 = open('data/target_dev.RT', "w")
    out_key2 = open('data/target_dev.KEY', "w")

    out_features3 = open('data/features_test.sparseX', "w")
    out_target3 = open('data/target_test.RT', "w")
    out_key3 = open('data/target_test.KEY', "w")


    x_index = 0
    x_index2 = 0
    x_index3 = 0

    train_lines = 0
    dev_lines = 0
    test_lines = 0

    
    while len(lines) > 0:
        if (train_lines < end_train or (dev_lines >= end_dev and test_lines >= end_test)):
            line = random.choice(lines)
            x_index = writeLine(x_index, config, line, out_features, out_target, out_key, known_pn, known_gn, True)
            lines.remove(line)
            train_lines += 1
        if (dev_lines < end_dev and len(lines) > 0):
            line = random.choice(lines)
            x_index2 = writeLine(x_index2, config, line, out_features2, out_target2, out_key2, known_pn, known_gn, False)
            lines.remove(line)
            dev_lines += 1
        if (test_lines < end_test and len(lines) > 0):
            line = random.choice(lines)
            writeLine(x_index3, config, line, out_features3, out_target3, out_key3, known_pn, known_gn, False)
            lines.remove(line)
            test_lines += 1

    
    writeKey(path)


def writeLine(x_index, config, line, out_features, out_target, out_key, known_pn, known_gn, test_run):

    norm_date = config['norm']['date']
    norm_geo  = config['norm']['geo']
    norm_num  = config['norm']['num']
    norm_prof = config['norm']['prof']


    line = line.split(',')
    if len(line) < 8:
        return x_index
    tablet_id = line[0]

    # Clean up the line and ensure that there are no extra spaces
    text = utilities.clean_line(line[7].rstrip(), norm_num, norm_prof)
    text = text.lower()
    text = " ".join(text.split())
    text = text.strip()

    # We should skip the first line that labels the csv
    if "text" in text:
        return x_index
        
    newText = text;
    words = text.split(' ')
    line_id = line[6]
    # skip description lines
    if line_id == "":
        return x_index
    # change to line_id
    line_id = line[4]
    line_id = re.sub("[L]", "", line_id)
    last_word = ""
    last_word_2 = ""
    last_line_id = ""
    last_tablet = ""
    last_index = -1
    
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
                if (norm_geo):
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
        if last_word == "iti" and norm_date:
            if (w_type != "-"):
                print ("Warning, overwriting a known type with date: ", w, " - ", w_type)
            w_type = "D"            
            w = 'date'
                    
        if not (i == 0 and (w == "" or w == "-" or w == "...")):
            if (i > 0 and i < len(words) -1):
                # write last word
                x_index += writeWord(last_tablet, last_line_id, last_index, last_word_2,
                           last_word, w, x_index, out_key, out_features, out_target,
                                     last_name, last_geo, test_run, config)
            elif i == len(words) -1:
                #write last word
                x_index += writeWord(last_tablet, last_line_id, last_index, last_word_2,
                           last_word, w, x_index, out_key, out_features, out_target,
                                     last_name, last_geo, test_run, config)
                #write current word
                x_index += writeWord(tablet_id, line_id, i, last_word, w, "", x_index,
                           out_key, out_features, out_target,
                                     w_type == "PN", w_type == "GN", test_run, config)
                    
        last_word_2 = last_word
        last_word = w
        last_line_id = line_id
        last_tablet = tablet_id
        last_index = i
        
        if w_type == "PN":
            last_name = True
        else:
            last_name = False
        if w_type == "GN":
            last_geo = True
        else:
            last_geo = False
    # Return the final index.
    return x_index


def writeWord(tablet_id, line_id, i, last_word, word, next_word, x_index,
              out_key, out_features, out_target, PN, GN, test_run, config):
    if len(word) < 1:
        return 0

    if uniqueNames:
        if not test_run and PN and word in test_names:
            return 0
        if test_run and PN and word in dev_names:
            return 0
        if test_run and PN and word:
            test_names.add(word)
        else:
            dev_names.add(word)
    
    out_key.write("{0}, {1}, {2}, {3}\n".format(tablet_id, line_id, i, word))
    writeSparse(config, out_features, last_word, word, next_word, x_index)                    
    writeTarget(out_target, PN, GN)
    return 1


def writeTarget(out_target, isName, isGN):
    if isName:
        out_target.write("1\n")
    elif isGN:
        out_target.write("2\n")
    else:
        out_target.write("0\n")
        
def writeKey(path):
    out = open(path + 'features.KEY', "w")

    offset = 0
    
    for i in range(len(left_features)):
        out.write("[L]")
        out.write(left_features[i])
        out.write("\n")
    for i in range(len(right_features)):
        out.write("[R]")
        out.write(right_features[i])
        out.write("\n")
    for i in range(len(spelling_features)):
        out.write("[S]")
        out.write(spelling_features[i])
        out.write("\n")

    out.write("-word length-\n")

    for i in range(len(known_symbols)):
        out.write(known_symbols[i])
        out.write("\n")
