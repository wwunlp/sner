from ruleset import *
from tokenset import *
from sys import argv
import namesfromrules
import contextualfromnames
import spellingfromnames
import config


# Handles pulling things from config file
# Currently gets corpus file name and rule file name.
# Expects a "blank" configuration.txt to look like this:
# CORPUS_NAME=
# SEED_RULES=
# ITERATION_COUNT=
# RULES_PER_ITERATION=
# Otherwise prompts user for answers to everything, makes sure
#  iterations and maxrules are ints.
def init():
    corpusname = ""
    rulesname = ""
    iterations = -1
    maxrules = -1

    # Get from command line
    if len(sys.argv) == 5:
        corpusname = argv[1]
        rulesname = argv[2]
        if argv[3].isdigit():
            iterations = argv[3]
        if argv[4].isdigit():
            maxrules = argv[4]

    # Get from configuration file
    else:
        try:
            print("Pulling configuration options from: configuration.txt")
            configfile = open("configuration.txt", "r")
            nextline = configfile.readline().split('=')

            while(nextline[0] != ""):
                nextline[0] = nextline[0].rstrip('\n')
                nextline[1] = nextline[1].rstrip('\n')

                if nextline[0] == "CORPUS_NAME" and not corpusname:
                    corpusname = nextline[1]
                    if not corpusname:
                        corpusname = input("Please enter the name of the" +
                                           " corpus data file: ")

                elif nextline[0] == "SEED_RULES" and not rulesname:
                    rulesname = nextline[1]
                    if rulesname == "":
                        rulesname = input("Please enter the name of the" +
                                          " corpus data file: ")

                elif nextline[0] == "ITERATION_COUNT" and iterations < 0:
                    iterations = nextline[1]
                    if iterations == "":
                        iterations = input("Please enter the number of" +
                                           " iterations: ")
                        while(not iterations.isdigit()):
                            iterations = input("Please enter a valid integer" +
                                               " for number of iterations: ")

                elif nextline[0] == "RULES_PER_ITERATION" and maxrules < 0:
                    maxrules = nextline[1]
                    if maxrules == "":
                        maxrules = input("Please enter the maximum number of" +
                                         " new rules per iteration: ")
                        while(not maxrules.isdigit()):
                            maxrules = input("Please enter a valid integer" +
                                             " for maximum number of rules" +
                                             " per iteration: ")

                nextline = configfile.readline().split('=')

        except FileNotFoundError:
            print("Couldn't find a config file, getting input...")
            corpusname = input("Please enter the name of the corpus" +
                               " data file: ")
            rulesname = input("Please enter the name of the corpus" +
                              " data file: ")
            iterations = int(input("Please enter the number of iterations: "))
            while(not iterations.isdigit()):
                iterations = int(input("Please enter a valid integer for" +
                                       " number of iterations: "))
                maxrules = int(input("Please enter the maximum number of" +
                                     " new rules per iteration: "))
                while(not maxrules.isdigit()):
                    maxrules = int(input("Please enter a valid integer for" +
                                         " maximum number of rules per" +
                                         " iteration: "))
        except:
            print("ERROR: Unable to open configuration file")

    # Any missing values found here
    if corpusname == "":
        corpusname = input("Please enter the name of the corpus data file: ")
    if rulesname == "":
        rulesname = input("Please enter the name of the corpus data file: ")
    if int(iterations) <= 0:
        iterations = input("Please enter the number of iterations: ")
        while(not iterations.isdigit()):
            iterations = int(input("Please enter a valid integer for number" +
                                   " of iterations: "))
    if int(maxrules) <= 0:
        maxrules = int(input("Please enter the maximum number of new rules" +
                             " per iteration: "))
        while(not maxrules.isdigit()):
            maxrules = int(input("Please enter a valid integer for maximum" +
                                 " number of rules per iteration: "))

    return [corpusname, rulesname, iterations, maxrules]

# Reads the corpus file into memory by prompting the user for a file name.
# Returns the contents of the corpus as a TokenSet.
# Kind of a horribly bloody mess right now.


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

    corpus = TokenSet()

    # Convert the line into the appropriate format
    # Each entry being a three element list, containing left context, token,
    #  right context

    def interpretTokenType(wordType):
        if wordType == "PN":
            return TokenType.personal_name
        elif wordType == "GN":
            return TokenType.geographic_name
        elif wordType == "PF":
            return TokenType.profession
        elif wordType == "-":
            return TokenType.none
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
            corpus.addToken(prevToken)

            prevToken = token

        else:
            corpus.addToken(prevToken)

            tabletID = line[0]
            token = Token(None, line[3], None, interpretTokenType(line[4]))
            prevToken = token

    corpus.addToken(prevToken)

    return corpus


# This function will read the seed rule file, and return the contents as
# a RuleSet (defined in ruleset.py)
def loadSeedRules(rulename):
    rules = RuleSet()

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
        ruletype = RuleType.unset

        if ruledata[0] == "LEFT_CONTEXT":
            ruletype = RuleType.left_context
        elif ruledata[0] == "RIGHT_CONTEXT":
            ruletype = RuleType.right_context
        elif ruledata[0] == "SPELLING":
            ruletype = RuleType.spelling
        else:
            print("ERROR: rule parsing failed, invalid type: " + ruledata[0])
            sys.exit()

        rules.addRule(Rule(ruletype, ruledata[1], float(ruledata[2])))

    return rules


# Orchestrate the execution of the program
def main():
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
    allrules = RuleSet()

    # Pulls things from configuration file
    configs = init()
    corpusname = configs[0]
    rulename = configs[1]
    iterations = int(configs[2])
    maxrules = int(configs[3])

    # Load and prepare corpus data.
    # Corpus is a TokenSet, which is a container for many Token items.
    # Tokens represent individual words in the corpus, and contain left
    #  and right context as well as annotations
    corpus = loadCorpus(corpusname)

    # Get the seed rules
    seedrules = loadSeedRules(rulename)
    rulestack.append(seedrules)
    allrules.extend(seedrules)

    # Identify names via seed rules
    newNames = namesfromrules.run(corpus, seedrules)
    names.append(newNames)

    contextualIteration = False

    # Begin iterating.
    i = 0
    while i < iterations:
        if contextualIteration:
            print("iteration " + str(i + 1) + ": find contextual rules")
            newRules = contextualfromnames.run(corpus, allrules, names[i],
                                               maxrules)
            rulesFound = len(list(newRules.rules))
            print("found " + str(rulesFound) + " new contextual rules!")

            rulestack.append(newRules)
            allrules.extend(newRules)

            # Get the names for the next iteration.
            newNames = namesfromrules.run(corpus, newRules)
            print("top " + str(rulesFound) + " rules found " +
                  str(len(newNames.tokens)) + " new names")
            names.append(newNames)
        else:
            print("iteration " + str(i + 1) + ": find spelling")
            newRules = spellingfromnames.run(corpus, allrules, names[i],
                                             maxrules)
            rulesFound = len(list(newRules.rules))
            print("found " + str(rulesFound) + " new spelling rules!")

            rulestack.append(newRules)
            allrules.extend(newRules)

            # Get the names for the next iteration
            newNames = namesfromrules.run(corpus, newRules)
            print("top " + str(rulesFound) + " rules found " +
                  str(len(newNames.tokens)) + " new names")
            names.append(newNames)

        contextualIteration = not contextualIteration
        i += 1

    # Debug output
    # i = 0
    # for rule in allrules:
    #    print("rule " + str(i) + ": " + str(rule.rtype) + " " +
    #          str(rule.contents) + " " + str(rule.strength))
    #    i += 1

    # Really half assed output system, needs upgrading.
    
    f = open("output.csv", 'wb')

    f.write("Rule,Rule Type,Strength\n".encode('utf-8'))
    for rule in allrules:
        f.write("{0},{1},{2}\n".format(str(rule.contents), str(rule.rtype),
                str(rule.strength)).encode('utf-8'))

    f.close()

    #use the top rules (allrules variable) to get all names that apply to the rules we found
    namesfound = namesfromrules.run(corpus, allrules)

    totalresults = 0
    namecount = 0
    #sum the occurrences of all things in the nameset, add this to totalresults
    #also scan for occurrences annotated as names and add those occurences to namecount
    for token in namesfound:
        totalresults += token.occurrences
        if token.annotation == TokenType.personal_name:
            namecount += token.occurrences

    print("accuracy: " + str(100 * (namecount / totalresults)) + "%")

    totalnames = 0
    #scan for all tokens annotated as names and sum, to find all name occurence
    for token in corpus:
        if token.annotation == TokenType.personal_name:
            totalnames += token.occurrences

    print("recall: " + str(100 * (namecount / totalnames)) + "%")
    
# Begin execution
main()
