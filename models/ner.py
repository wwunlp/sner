from classes import Rule, Token
from scripts.ner import contextualfromnames, namesfromrules, \
spellingfromnames, updatetokenstrength


def loadCorpus(corpusname):

    rawcorpus = list()

    try:
        corpusfile = open(corpusname, "r")
    except:
        print("ERROR: Unable to open file: " + corpusname)

    # Skip the first line since its column identifiers
    next(corpusfile)
    # Read the corpus from the user-specified file
    for line in corpusfile:
        # Clean out the line returns as they will confuse the algorithm
        line = line.replace('\n', '')
        rawcorpus.append(line.split(','))

    corpusfile.close()

    corpus = set()

    # Convert the line into the appropriate format
    # Each entry being a three element list, containing left context, token,
    #  right context

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

    # Here you see loop unrolling
    rawIter = iter(rawcorpus)
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


# This function will read the seed rule file, and return the contents as
# a RuleSet (defined in ruleset.py)
def loadSeedRules(rulename):
    rules = set()

    try:
        rulefile = open(rulename, "r")
    except:
        print("ERROR: Unable to open file: " + rulename)

    # Read the corpus from the user-specified file.
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
    #find all names that pass a certain probability threshold, these will be considered our results
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

def rulesStrengthAssessment(rules, corpus, cfg):

    badrules = 0
    totalspelling = 0
    badspelling = 0
    totalcontext = 0
    badcontext = 0

    totaldelta = 0

    print("calculating...", end='\r')

    for rule in rules:
        names = namesfromrules.namesFromRule(corpus, rule)
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

# Orchestrate the execution of the program
def main(data, options):
    # Rules and names will be lists of RuleSets or TokenSets.
    # These sets will represent the results of various iterations of
    # the algorithm. So index 0 of rules would be the first rule set
    # (seed rules) and 1 would be the first rules generated and used by the
    # algorithm itself.
    # Index zero of names would be the names that came from the seed rules.
    # Index one the rules that came from rule set 1.
    # And so on.
    rulestack = list()
    names = list()

    # Meant to store all rules that are ultimately used by the algorithm
    allrules = set()

    # Pulls things from configuration file
    corpusname = data.corpus
    rulesname = data.seed_rules
    iterations = options.iterations
    maxrules = options.max_rules

    # Load and prepare corpus data.
    # Corpus is a TokenSet, which is a container for many Token items.
    # Tokens represent individual words in the corpus, and contain left
    #  and right context as well as annotations
    corpus = loadCorpus(corpusname)

    # Get the seed rules
    seedrules = loadSeedRules(rulesname)

    #apply them to the tokens in the corpus
    updatetokenstrength.run(corpus, seedrules, options)

    #add them as the first generation of rules, and add them to the 'all rules' set
    rulestack.append(seedrules)
    allrules.union(seedrules)

    # Identify names via the seed rules
    newNames = namesfromrules.run(corpus, seedrules, options)
    names.append(newNames)

    contextualIteration = False

    # Begin iterating.
    i = 0
    while i < iterations:

        #detect the new rules
        newRules = set()
        rulesFound = 0
        if contextualIteration:
            print("iteration " + str(i + 1) + ": find contextual rules")
            newRules = contextualfromnames.run(corpus, allrules, names[i],
                                               maxrules, options)
            rulesFound = len(list(newRules))
            print("found " + str(rulesFound) + " new contextual rules!")
        else:
            print("iteration " + str(i + 1) + ": find spelling")
            newRules = spellingfromnames.run(corpus, allrules, names[i],
                                             maxrules)
            rulesFound = len(list(newRules))
            print("found " + str(rulesFound) + " new spelling rules!")

        #at this point in execution the new rules have had their strength ratings assigned (unless something broke)

        #update the name_probability ratings of all of the tokens using the new rules
        #so, in light of the new rules, how does that effect all tokens chances of being a name?
        updatetokenstrength.run(corpus, newRules, options)

        #record the rules found in this iteration of the algorithm
        rulestack.append(newRules)

        #update the list of all rules found
        allrules.union(newRules)


        # Get the names for the next iteration
        newNames = namesfromrules.run(corpus, newRules, options)
        names.append(newNames)

        print("top " + str(rulesFound) + " rules found " +
              str(len(newNames.tokens)) + " new names")


        print("performance so far:")
        performanceAssessment(corpus, options)

        print("")


        contextualIteration = not contextualIteration
        i += 1

    print("rule performance:")
    rulesStrengthAssessment(allrules, corpus, options)

    # Really half assed output system, needs upgrading.

    f = open("output.csv", 'wb')

    f.write("Rule,Rule Type,Strength\n".encode('utf-8'))
    for rule in allrules:
        f.write("{0},{1},{2}\n".format(str(rule.contents), str(rule.type),
                str(rule.strength)).encode('utf-8'))

    f.close()
