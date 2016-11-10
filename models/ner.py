from classes import Rule, Token
from scripts.ner import contextualfromnames, namesfromrule
from scripts.ner import spellingfromnames, updatetokenstrength


def tokenize_corpus(corpus_loc):
    """
    Args:
        corpus_loc (str): Location of corpus file.

    Returns:
        corpus (set): Set of Token objects.

    Raises:
        TypeError
    """

    corpus_list = []

    corpus_file = open(corpus_loc, 'r')

    next(corpus_file) # Skip headers
    for line in corpus_file:
        line = line.replace('\n', '')
        corpus_list.append(line.split(','))

    corpus_file.close()

    corpus = set()

    # Convert the line into the appropriate format
    # Each entry being a three element list, containing left context,
    # token, right context

    def interpretTokenType(wordType):
        if wordType == "PN":
            return Token.Types.personal_name
        elif wordType == "GN":
            return Token.Types.geographic_name
        elif wordType == "PF":
            return Token.Types.profession
        elif wordType == "-":
            return Token.Types.none
        else:
            tb = sys.exc_info()[2]
            raise TypeError("Unrecognized Word Type in corpus" +
                            " file!").with_traceback(tb)

    rawIter = iter(corpus_list)
    line = next(rawIter)
    tabletID = line[0]
    # Inputs here are: the left context for the token, the token itself,
    # the right context, and then the type of the token
    #  (for instance if its annotated as a PN)
    # right context is assumed to be nothing,
    # and will be set later if otherwise
    prevToken = Token(None, line[3], None, interpretTokenType(line[4]))

    for line in rawIter:
        if(line[0] == tabletID):
            token = Token(prevToken, line[3], None,
                          interpretTokenType(line[4]))

            prevToken.right_context = str(token)
            Token.add(corpus, prevToken, None)

            prevToken = token

        else:
            Token.add(corpus, prevToken, None)

            tabletID = line[0]
            token = Token(None, line[3], None, interpretTokenType(line[4]))
            prevToken = token

    Token.add(corpus, prevToken, None)

    return corpus


def tokenize_seed_rules(rulename):
    """This function will read the seed rule file, and return the contents as
    a set.
    Args:
        rulename (str): Location of seed rules file.

    Returns:
        rules (set): Set of Rule objects corresponding to the rules in the
            seed rules file.

    Raises:
        None
    """
    rules = set()

    try:
        rulefile = open(rulename, "r")
    except:
        print("ERROR: Unable to open file: " + rulename)

    # Skip the first line since its column identifiers.
    next(rulefile)
    for line in rulefile:
        # Clean out the line returns as they will confuse the algorithm.
        line = line.replace('\n', '')
        ruledata = line.split(",")
        ruletype = Rule.Types.unset

        if ruledata[0] == "LEFT_CONTEXT":
            ruletype = Rule.Types.left_context
        elif ruledata[0] == "RIGHT_CONTEXT":
            ruletype = Rule.Types.right_context
        elif ruledata[0] == "SPELLING":
            ruletype = Rule.Types.spelling
        else:
            print("ERROR: rule parsing failed, invalid type: " + ruledata[0])
            sys.exit()

        rules.add(Rule(ruletype, ruledata[1], float(ruledata[2])))

    return rules

def performanceAssessment(corpus, options):
    """Find all names that pass a certain probability threshold, these will be
    considered our results
    Args:
        courpus ():
        options ():

    Returns:
        None

    Raises:
        None
    """

    namethreshold = options.accept_threshold
    namesfound = set()
    for token in corpus:
        if token.name_probability > namethreshold:
            Token.add(namesfound, token, None)

    totalresults = 0
    accurateresults = 0
    #sum the occurrences of all things in the nameset, add this to totalresults
    #also scan for occurrences annotated as names and add those occurences to namecount
    for token in namesfound:
        totalresults += token.occurrences
        if token.annotation == Token.Types.personal_name:
            accurateresults += token.occurrences

    totalnames = 0
    #scan for all tokens annotated as names and sum, to find all name occurence
    for token in corpus:
        if token.annotation == Token.Types.personal_name:
            totalnames += token.occurrences

    accuracy = accurateresults / totalresults
    recall = accurateresults / totalnames
    print("accuracy: " + str(100 * accuracy) + "%")
    print("recall: " + str(100 * recall) + "%")
    print("acceptance threshold: " + str(100 * namethreshold) + "%")
    print("probability ratings off by " + str(100 * abs(namethreshold - accuracy)) + " points")

def rulesStrengthAssessment(rules, corpus):
    """
    Args:
        rules ():
        corpus ():
        cfg ():

    Returns:
        None

    Raises:
        None
    """

    badrules = 0
    totalspelling = 0
    badspelling = 0
    totalcontext = 0
    badcontext = 0

    totaldelta = 0

    print("calculating...", end='\r')

    for rule in rules:
        names = namesfromrule.main(corpus, rule)
        realnames = 0
        total = 0
        for token in names:
            if token.annotation == Token.Types.personal_name:
                realnames += 1
                total += 1
            else:
                total += 1

        truestrength = realnames/total
        delta = abs(truestrength - rule.strength)
        totaldelta += delta

        if rule.type == Rule.Types.spelling:
            totalspelling += 1
        else:
            totalcontext += 1

        if delta > 0.2:
            badrules += 1
            if rule.type == Rule.Types.spelling:
                badspelling += 1
            else:
                badcontext += 1

    print("               ", end='\r')

    print("percentage of bad rules: " + str(100 * badrules/len(rules)) + "%")
    print("percentage of bad context: " + str(100 * badcontext/totalcontext) + "%")
    print("percentage of bad spelling: " + str(100 * badspelling/totalspelling) + "%")
    print("average delta value: " + str(100 * totaldelta / len(rules)) + "%")


def namesFromRules(corpus, rules):
    """Meant to use the provided ruleset to scan the corpus for names.
    It will then return the names in quesiton, which will be used
    to generate more rules.

    """

    names = set()

    for rule in rules:
        results = namesfromrule.main(corpus, rule)

        # Can probably write an extend function that doesn't enforce
        #  set properties.
        # You can insert them without checking for redundancies because
        # they already were checked.
        names = names.union(results)

    return names


def main(data, options):
    """Rules and names will be lists of RuleSets or TokenSets.
    These sets will represent the results of various iterations of
    the algorithm. So index 0 of rules would be the first rule set
    (seed rules) and 1 would be the first rules generated and used by the
    algorithm itself. Index zero of names would be the names that came from
    the seed rules. Index one the rules that came from rule set 1. And so on.

    Args:
        data (Data): Data object with atrributes of locations for data files.
        options (Options): Options object with attributes of flags and
            variables.

    Returns:
        None

    Raises:
        None
    """

    corpus_file = data.corpus
    seed_rules_file = data.seed_rules
    iterations = options.iterations
    max_rules = options.max_rules

    corpus = tokenize_corpus(corpus_file)
    seed_rules = tokenize_seed_rules(seed_rules_file)

    updatetokenstrength.main(corpus, seed_rules)

    rule_list = list(seed_rules)
    all_rules = seed_rules

    new_names = namesFromRules(corpus, seed_rules)
    name_list = list(new_names)

    context_iter = False

    i = 0
    while i < iterations:
        if context_iter:
            print("iteration {}: find context rules".format(i + 1))
            new_rules = contextualfromnames.main(corpus, all_rules,
                                      name_list, max_rules)
            rules_found = len(new_rules)
            print("found {} new context rules!".format(rules_found))
        
        else:
            print("iteration {}: find spelling rules".format(i + 1))
            new_rules = spellingfromnames.main(corpus, all_rules,
                                      name_list, max_rules)
            rules_found = len(new_rules)
            print("found {} new spelling rules!".format(rules_found))

        updatetokenstrength.main(corpus, new_rules)

        rule_list.extend(list(new_rules))
        all_rules = all_rules.union(new_rules)

        new_names = namesFromRules(corpus, new_rules)
        name_list.extend(list(new_names))

        print("top {} rules found {} new names".format(
            rules_found, len(new_names)))

        print("performance so far:")
        performanceAssessment(corpus, options)

        print("")

        context_iter = not context_iter
        i += 1

    print("rule performance:")
    rulesStrengthAssessment(all_rules, corpus)

    f = open(data.output, 'wb')

    f.write("Rule,Rule Type,Strength\n".encode('utf-8'))
    for rule in all_rules:
        f.write("{0},{1},{2}\n".format(str(rule.contents), str(rule.type),
                str(rule.strength)).encode('utf-8'))

    f.close()
