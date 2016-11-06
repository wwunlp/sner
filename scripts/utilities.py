from scripts import professions
import codecs
import re


def get_counts(data):
    """
    Get the total occurrences of words and syllables in the original Unicode
    Garshana text.
    Remove annotations from the text portion of each line in the data file and
    then track the occurrence of each word and syllable.  For syllables, we are
    counting all unigrams, bigrams, and trigrams.

    Return a dictionary of the word occurrences and
     a dictionary of the syllable occurrences.
    """

    word_count = {}
    syll_count = {}

    # Hard coding this filename in so there is no ambiguity as to what we
    # consider the original text to be.
    infile = data.corpus
    try:

        open_file = codecs.open(infile, 'r', encoding='utf-16')
        for line in open_file:
            line = line.lower()
            # Remove tablet indexing info and line numbers. Grab only text data
            line = line.split(',')
            text = clean_line(line[7])

            # Update the occurrences of the words in the line
            for word in text.split():
                count = word_count.setdefault(word, 0)
                word_count[word] = count + 1

                # Track occurrences of syllables
                update_syllable_count(word, syll_count)

        open_file.close()
    except IOError:
        print("Cannot open: " + infile)

    return (word_count, syll_count)


def update_syllable_count(word, syll_count):
    """
    Update the total occurrence counts of each unigram, bigram, and trigram
    syllable that occurs in the word.  Note: syllables are separated by a
    dash ('-').
    """

    syllables = word.split('-')
    for i in range(1, 4):
        for j in range(len(syllables) - i + 1):
            gram = '-'.join(syllables[j: j + i])
            count = syll_count.setdefault(gram, 0)
            syll_count[gram] = count + 1


def clean_line(line, normNum=True, normProf=True):
    """
    Clean a line of data, removing all annotations from the line.

    NOTE: The line is expected to only be the TEXT portion of the data files.
    I.e. the ID and line number parts of the data files are expected to be
    previously removed.

    Return the cleaned line.

    """

    # Remove square brackets, ceiling characters, question marks, other
    # questionable characters, and line breaks
    line = re.sub(r'(\[|\])', '', line)
    line = re.sub(r'(⌈|⌉)', '', line)
    line = re.sub(r'( / )', ' ', line)
    line = re.sub(r'/', '', line)
    line = re.sub(r'\?', '', line)
    line = re.sub(r'([<]|[>])+', '', line)
    line = re.sub(r'!', '', line)
    line = re.sub(r'"', '', line)

    # Remove researcher's notes, and multiple dashes or '='s
    line = re.sub(r'(\(.*\))', '', line)
    line = re.sub(r'(#[.]*)', '', line)
    line = re.sub(r'[-]{2}', '', line)
    line = re.sub(r'[=]{2}', '', line)

    # Replace numbers with 'number'
    if normNum is True:
        line = re.sub(r'\b(?<!-)(\d+)(?![\w-])', 'number', line)

    # Replace professions with 'profession'
    if normProf is True:
        line = professions.replaceProfessions(line)

    # Remove blank character at end of line
    linelength = len(line)
    if (linelength > 0 and line[linelength-1] == ""):
        del line[0:linelength-2]

    return line


def main():
    # Testing
    word_count, syll_count = get_counts()
    print(word_count)
    print()
    print(syll_count)

if __name__ == '__main__':
    main()
