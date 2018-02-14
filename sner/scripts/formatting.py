from sner.scripts import professions, utilities
import codecs
import csv
import re
import argparse


def findKnown(data, options, knownPN, knownGN):
    """
    Iterates through the attenstations file for personal and geographical names
     and adds the lineIDs in a list to the knownPN and knownGN dictionaries.
    Args:
        data (?)
        options (?)
        knownPN = { Personal name : line ID }, to be filled in.
        knownGN = { Geographical name : line ID}, to be filled in.

    Returns:
        Updates knownPN and knownGN dictionaries with the lineIDs.

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
        lineID = line[1]
        lineID = re.sub("[L]", "", lineID)        

        if line[9].rstrip() == 'PN':
            if (name not in knownPN):
                knownPN[name] = [lineID]
            else :
                knownPN[name].append(lineID)
        if line[9].rstrip() == 'GN':
            if (name not in knownGN):
                knownGN[name] = [lineID]
                if (name in knownPN):
                    print ("Note: ", name, " is both a PN and GN.")
            else :
                knownGN[name].append(lineID)                

def main(data, options):
    """
    Finds all names in options.attestations file, and goes through each word 
      in the main options.corpus file to fill a new output file specified by
      options.output
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
    
    knownPN = {}
    knownGN = {}
    findKnown(data, options, knownPN, knownGN)
    
    # iterate each line in Garshana Text and output to specified file
    file2 = codecs.open(data.corpus, 'r', encoding = 'utf-8')
    out = open(data.output, "w")
        
    out.write("Tablet ID,Line Number,Word Number,Word,Word Type\n")
    
    for line in file2:
        line = line.split(',')
        tabletID = line[0]

        # Clean up the line and ensure that there are no extra spaces
        text = utilities.clean_line(line[7].rstrip(), options.norm_num, options.norm_prof)
        text = text.lower()
        text = " ".join(text.split())
        text = text.strip()

        # We should skip the first line that labels the csv
        if "text" in text:
            continue
        
        newText = text;
        words = text.split(' ')
        lineID = line[6]
        # skip description lines
        if lineID == "":
            continue
        # change to lineID
        lineID = line[4]
        lineID = re.sub("[L]", "", lineID)
        lastWord = ""
        if "'" in lineID:
            lineID = re.sub("[']", "", lineID)
            lineID = "'" + lineID
        for i in range(len(words)):
            w = words[i]
            wType = "-"
            # Set types if they are known and avoid
            # conflicts by using the lineID.
            if w in knownPN:
                if (lineID in knownPN[w]):
                    wType = "PN"
            if w in knownGN:
                if (lineID in knownGN[w]):
                    if (w in knownPN and wType != "-"):
                        print("Warning, replacing PN with GN!")
                    wType = "GN"
                    if (options.norm_geo):
                        w = "geoname"
            if professions.replaceProfessions(w) == 'profession':
                if (wType != "-"):
                    print ("Warning, replacing name with profession!")
                wType = "PF"
                
            if 'number' in w:
                if (wType != "-"):
                    print ("Warning, overwriting a known type with number: ", w, " - ", wType)
                wType = "N"
                w = 'number'
            if lastWord == "iti":
                if (wType != "-"):
                    print ("Warning, overwriting a known type with date: ", w, " - ", wType)
                wType = "D"
                if (options.norm_date):
                    w = 'date'
                
            lastWord = w            
            if not (i == 0 and (w == "" or w == "-" or w == "...")):
                out.write("{},{},{},{},{}\n".format(tabletID, lineID, i, w, wType))  
