#!/usr/bin/python3

# Convert our current Garshana (Atte / Texts.csv) corpus to old corpus style for use in unsupervised learning program
# Andy Brown
# Authored     10/7/2016
# Last Updated 10/7/2016

import utilities
import codecs
import csv
import re
import argparse

knownNames = {}

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("-nameTag", "-nt",  help="The formating for names, default is $PN$", required=False, default="$PN$")
parser.add_argument("--normNum", "--n", help="Enable the nomralization  of numbers", required=False, dest='normNum', action='store_true')
parser.add_argument("--normProf", "--p", help="Enable the normalization of professions", required=False, dest='normProf', action='store_true')
parser.add_argument("-lt",  help="Left tag of a sentence, default blank", required=False, default="")
parser.add_argument("-rt",  help="Right tag of a sentence, default newline", required=False, default="\n")
parser.add_argument("--tablet", "--t", help="Add start of tablet line, default False", required=False, dest='tablet', action='store_true')
parser.add_argument("-output", "-o",  help="Name of the output file, default convertedCorpuseText", required=False, default="convertedCorpusText")
parser.add_argument("-mode", "-m", help="Switch between [csv] and [multiline] modes, default csv", required=False, choices=["csv", "multiline"], default="csv")
parser.set_defaults(normNum = False, normProf = False, tablet = False)
args = parser.parse_args()


def main():
    """
    Find all names in Attestations file, and goes through each in in the main Texts file
    to fill a new output file (default convertedCorpusText, can specify with -o arg)
    The default mode is a CSV file with the format:
      TabletID, LineID, LocationInSentence, Word, Word Type
    Word Type is either '-' or 'PN' to identify personal names. 

    If you specify -mode to be 'multiline' then you can generate an ouput similiar to the
    corpus used in the old unsupervised model.
    
    You can use --normProf [-p] to normalize professions in the output
    You can use --normNum [-n] to normalize the numbers in the output

    There are additional args for multiline mode which can be seen by running the
    program with the -h tag. 
    """
    
    file = codecs.open('Garshana Dataset/Attestations_PNs.csv', 'r', encoding = 'utf-16')
    # find all of the names
    for line in file:
        line = line.split(',')
        if line[9].rstrip() == 'PN':
            text = utilities.clean_line(line[4].rstrip(), args.normNum, args.normProf)
            text = text.lower()
            name = utilities.clean_line(line[5].rstrip(), args.normNum, args.normProf)
            name = name.lower()
            knownNames[name] = 1


    # iterate each line in Garshana Text and output to specified file
    file2 = codecs.open('Garshana Dataset/Texts.csv', 'r', encoding = 'utf-16')
    out = open(args.output, "w")

    
    if args.mode == "csv":
        out.write("Tablet ID,Line Number,Word Number,Word,Word Type\n")
    
    curTablet = -1
    for line in file2:
        line = line.split(',')
        tabletID = line[0]

        # Clean up the line and ensure that there are no extra spaces
        text = utilities.clean_line(line[7].rstrip(), args.normNum, args.normProf)
        text = text.lower()
        text = " ".join(text.split())
        text = text.strip()

        # We should skip the first line that labels the csv
        if "text" in text:
            continue
        
        newText = text;
        words = text.split(' ')

        # multi mode
        if args.mode == "multiline":
            newWords = text.split(' ')
            for i in range(len(words)):
                w = words[i]
                if w in knownNames:
                    newWords[i] = w + args.nameTag
            newText = args.lt + ' '.join(newWords) + args.rt
            # Indicate the start of a new tablet
            if tabletID != curTablet:
                curTablet = tabletID
                if args.tablet == True:
                    out.write("&P" + tabletID + "\n")
            # write the converted line
            out.write(newText)

        # csv Mode
        if args.mode == "csv":
            lineID = line[6]
            for i in range(len(words)):
                w = words[i]
                wType = "-"
                if w in knownNames:
                    wType = "PN"
                out.write("{},{},{},{},{}\n".format(tabletID, lineID, i, w, wType))  

if __name__ == '__main__':
    print ("Starting conversion...")
    main()
    print ("Converted and saved as " + args.output + "!")
