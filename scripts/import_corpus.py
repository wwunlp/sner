"""Import Corpus"""
import math
import pandas as pd
from classes import Display


def main(config):
    """
    main
    Args:
        corpus = file to pull data from
        path = where to find the corpus

    Returns:
        corpus = corpus in an array format

    Raises:
        None

    """

    file_name = config['corpus']
    path = config['path']

    if file_name[-3:] == 'atf':
        sep = 'READ_AS_ONE_COLUMN'
        header = None
        engine = 'python'
    elif file_name[-3:] == 'csv':
        sep = ','
        header = 0
        engine = 'c'

    reader = pd.read_table(
        filepath_or_buffer=path + file_name,
        sep=sep,
        header=header,
        engine=engine
    )

    cols = {
        'BDTNS ID'   : [],
        'Line ID'    : [],
        'CDLI ID'    : [],
        'Designation': [],
        'Q ID'       : [],
        'Q Line'     : [],
        'Language'   : [],
        'Object'     : [],
        'Surface'    : [],
        'Discourse'  : [],
        'Line'       : [],
        'Text'       : [],
        'Translation': []
    }

    corpus = pd.DataFrame(data=cols)

    objects = [
        'tablet',
        'envelope',
        'prism',
        'bulla',
        'fragment'
    ]

    discourse = [
        'catchline',
        'colophon',
        'date'
        'signatures',
        'signature',
        'summary',
        'witness'
    ]

    def read_csv(corpus, reader):
        """
        read csv
        """

        bdtns_id = ''
        line_id = ''
        cdli_id = ''
        name = ''
        q_id = ''
        q_line = ''
        lang = ''
        obj = ''
        surf = ''
        disc = ''
        line = ''
        text = ''
        tran = ''

        i = 0
        for index, row in reader.iterrows():
            if row['Text'] != 'NaN':
                i += 1
                bdtns_id = row['Id BDTNS']
                line_id = row['Id Line']
                line = row['Line']
                text = row['Text']
                corpus.loc[i, 'BDTNS ID'] = bdtns_id
                corpus.loc[i, 'Line ID'] = line_id
                corpus.loc[i, 'CDLI ID'] = cdli_id
                corpus.loc[i, 'Designation'] = name
                corpus.loc[i, 'Q ID'] = q_id
                corpus.loc[i, 'Q Line'] = q_line
                corpus.loc[i, 'Language'] = lang
                corpus.loc[i, 'Object'] = obj
                corpus.loc[i, 'Surface'] = surf
                corpus.loc[i, 'Discourse'] = disc
                corpus.loc[i, 'Line'] = line
                corpus.loc[i, 'Text'] = text
                corpus.loc[i, 'Translation'] = tran

        return corpus


    def read_atf(corpus, reader):
        """
        read atf
        """

        bdtns_id = ''
        line_id = ''
        cdli_id = ''
        name = ''
        q_id = ''
        q_line = ''
        lang = ''
        obj = ''
        surf = ''
        disc = ''
        line = ''
        text = ''
        tran = ''

        display = Display()
        display.start('Importing corpus')

        i = 0
        for index, row in reader.iterrows():
            display.update_progress_bar(index + 1, len(reader))
            if row[0][0] == '&':
                cdli_id = row[0][:8]
                name = row[0][11:]
                q_id = ''
                q_line = ''
                lang = ''
                obj = ''
                surf = ''
                disc = ''
                line = ''
                text = ''
                tran = ''
            elif row[0][0] == '#':
                if row[0][1:10] == 'atf: lang':
                    lang = row[0][11:]
                if row[0][1:4] == 'tr.':
                    tran = row[0][4:]
                else:
                    # Ignore Comments
                    pass
            elif row[0][0] == '@':
                if row[0][1:] in objects:
                    obj = row[0][1:]
                elif row[0][1:7] == 'object':
                    obj = row[0][8:]
                elif row[0][1:] in discourse:
                    disc = row[0][1:]
                else:
                    surf = row[0][1:]
            elif row[0][0] == '$':
                # Ignore States
                pass
            elif row[0][:3] == '>>Q':
                q_id = row[0][2:9]
                q_line = row[0][10:]
            else:
                if row[0][0].isdigit():
                    i += 1
                    period = row[0].index('.')
                    line = row[0][:period]
                    text = row[0][period + 2:]
                else:
                    text += row[0]

                corpus.loc[i, 'BDTNS ID'] = bdtns_id
                corpus.loc[i, 'Line ID'] = line_id
                corpus.loc[i, 'CDLI ID'] = cdli_id
                corpus.loc[i, 'Designation'] = name
                corpus.loc[i, 'Q ID'] = q_id
                corpus.loc[i, 'Q Line'] = q_line
                corpus.loc[i, 'Language'] = lang
                corpus.loc[i, 'Object'] = obj
                corpus.loc[i, 'Surface'] = surf
                corpus.loc[i, 'Discourse'] = disc
                corpus.loc[i, 'Line'] = line
                corpus.loc[i, 'Text'] = text
                corpus.loc[i, 'Translation'] = tran

        display.finish()
        return corpus


    if file_name[-3:] == 'atf':
        corpus = read_atf(corpus, reader)
    elif file_name[-3:] == 'csv':
        corpus = read_csv(corpus, reader)

    return corpus
