from sner.scripts import professions
import codecs
import re


def get_counts(data):
    """
    This function gets the total occurrences of words and syllables in the
    original Unicode Garshana corpus.  To do this, it opens a .csv file with
    utf-16 encoding, and splits on commans, expecting the line of sumerian text
    to be in the 8th column. Filters annotations from each line, and tracks the
    occurrence of each word and syllable. All combinations of unigrams, bigrams,
    and trigrams are treated as individual syllables.

    Args:
        data = filename of the corpus .csv file, consistent with the formatting
			   of the .csv files provided with the Garshana corpus.

    Returns:
        Returns dictionary of the number of times any unique word occurs, as
        well as a dictionary of occurrences for syllables.

    Raises:
        IOError

    """

    word_count = {}
    syll_count = {}

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

    Args:
        line (str): Line of just the text section of a tablet
    Returns:
        line (str): The line, with all annotations removed

    Raises:
        None
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
        line = re.sub(r'[-+]?\b\d+\b', 'number', line)

        #line = re.sub(r'\b([\-\.0-9]+)(?![\w-])', 'number', line)

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
