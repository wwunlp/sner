#!/usr/bin/python3

# Convert our current Garshana (Atte / Texts.csv) corpus to old corpus style for use in unsupervised learning program
# Andy Brown
# Authored     10/7/2016
# Last Updated 10/7/2016

import utilities
import codecs
import csv

knownNames = {}

def main():
    file = codecs.open('Garshana Dataset/Attestations_PNs.csv',
            'r', encoding = 'utf-16')
    # find all of the names
    for line in file:
        line = line.split(',')
        if line[9].rstrip() == 'PN':
            text = utilities.clean_line(line[4].rstrip())
            text = text.lower()
            name = utilities.clean_line(line[5].rstrip())
            name = name.lower()
            knownNames[name] = 1


    # replace concatenate all names with $PN$
    # and add in &P<Tablet ID number> before the start
    # of each tablet that is found
    file2 = codecs.open('Garshana Dataset/Texts.csv',
            'r', encoding = 'utf-16')
    out = open("convertedCorpusTexts", "w")
    prints = 0
    curTablet = -1
    for line in file2:
        line = line.split(',')
        curID = line[0]
        
        text = utilities.clean_line(line[7].rstrip())
        text = text.lower()

        # We should skip the first line that labels the csv
        if "text" in text:
            continue
        
        newText = text;
        words = text.split(' ')
        for w in words:
            if w in knownNames:
                newText = text.replace(w, w + "$PN$")
        newText = "<l> " + newText + " <\l>\n"

        # Indicate the start of a new tablet
        if curID != curTablet:
            curTablet = curID
            out.write("&P" + curID + "\n")
            
        # write the converted line
        out.write(newText)
        
main()
