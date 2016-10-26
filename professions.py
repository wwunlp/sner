
import re

professions = ["aga'us",
               "arad",
               "aszgab",
               "azlag",
               "ama-gal",
               "bahar",
               "bisajdubak",
               "damgar",
               "dikud",
               "dubsar",
               "en",
               "er2",
               "ereszdijir",
               "ensik",
               "engar",
               "enkud",
               "gaba'asz",
               "galamah",
               "gala",
               "geme",
               "gudug",
               "guzala"
               "ha-za-num2",
               "idu",
               "iszib",
               "kaguruk",
               "kasz",
               "lu2-kasz",
               "ka-us2-sa",
               "kijgia",
               "kinkin",
               "kur-gara",
               "kuruszda",
               "kusz",
               "lu2-mar-sa-me",
               "lu2-ur3-ra",
               "lugal",
               "lukur",
               "lungak",
               "malah",
               "maszkim",
               "muhaldim",
               "muszendu",
               "nagada",
               "nagar",
               "nar",
               "nin",
               "nubanda",
               "nukirik",
               "sajDUN",
               "sajja",
               "simug",
               "sipad",
               "sukkal",
               "szabra",
               "szagia",
               "szakkanak",
               "ša-ra-ab-du",
               "szej",
               "szesz",
               "szidim",
               "szu'i",
               "szukud",
               "szusz3",
               "tibira",
               "ugula",
               "ugula geš2-da",
               "unud",
               "urin",
               "ujjaja",
               "uszbar",
               "zabardab",
               "zadim"]

prof_re = re.compile(r'\b(?<!-)' + r'(?![\w-])|\b(?<!-)'.join(professions) +
                     r'(?![\w-])')


def replaceProfessions(line):
    """
    Replaces known professions with 'profession'
    """
    line, numReplaces = re.subn(prof_re, 'profession', line)
    return line


def main():
    """
    Testing function
    """
    line = 'testing 1234 zadim abc df3urin33  unud 3223aa ne33ds33 345'
    line = re.sub(r'\b(?<!-)(\d+)(?![\w-])', 'number', line)
    line = replaceProfessions(line)
    print(line)

if __name__ == '__main__':
    main()
