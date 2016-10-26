from ruleset import *
from tokenset import *
import namesfromrules
import contextualfromnames
import spellingfromnames

#reads the corpus file into memory by prompting the user for a file name
#returns the contents of the corpus as a TokenSet
#kindof a horribly bloody mess right now
def loadCorpus():
    rawcorpus = list()

    #prompt for the name of the corpus file
    corpusname = input("please enter the name of the corpus data file: ")

    try:
        corpusfile = open(corpusname, "r")
    except:
        print("ERROR: Unable to open file: " + corpusname)
        
    #skip the first line since its column identifiers
    next(corpusfile)
    #read the corpus from the user-specified file
    for line in corpusfile:
        #clean out the line returns as they will confuse the algorithm
        line = line.replace('\n','')
        rawcorpus.append(line.split(','))
        
    corpusfile.close()
    
    corpus = TokenSet()
    
    #convert the line into the appropriate format
    #each entry being a three element list, containing left context, token, right context

    def interpretTokenType(wordType):
        if wordType == "PN":
            return TokenType.personal_name
        elif wordType == "-":
            return TokenType.none
        else:
            tb = sys.exc_info()[2]
            raise TypeError("Unrecognized Word Type in corpus file!").with_traceback(tb)
            

    #here you see loop unrolling
    rawIter = iter(rawcorpus)
    line = next(rawIter)
    tabletID = line[0]
    #inputs here are, the left context for the token, the token itself, the right context, and then the type of the token (for instance if its annotated as a PN)
    #right context is assumed to be nothing, and will be set later if otherwise
    prevToken = Token(None, line[3], None, interpretTokenType(line[4]))
    
    for line in rawIter:
        if(line[0] == tabletID):
            token = Token(prevToken, line[3], None, interpretTokenType(line[4]))
            
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

#this function will read the seed rule file, and return the contents as a RuleSet (defined in ruleset.py)
def loadSeedRules():
    rules = RuleSet()

    #prompt for the name of the seed rule file 
    rulename = input("please enter the name of the seed rule file: ")
    
    try:
        rulefile = open(rulename, "r")
    except:
        print("ERROR: Unable to open file: " + rulename)


    #read the corpus from the user-specified file

    #skip the first line since its column identifiers
    next(rulefile)
    for line in rulefile:
        #clean out the line returns as they will confuse the algorithm
        line = line.replace('\n','')
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

#orchestrate the execution of the program
def main():
    #rules and names will be lists of RuleSets or TokenSets
    #these sets will represent the results of various iterations of the algorithm
    #so index 0 of rules would be the first rule set (seed rules) and 1 would be
    #the first rules generated and used by the algorithm itself
    #index zero of names would be the names that came from the seed rules
    #index one the rules that came from rule set 1
    #et cetera
    rulestack = list()
    names = list()

    #meant to store all rules that are ultimately used by the algorithm
    allrules = RuleSet()

    #load and prepare corpus data
    #corpus is a TokenSet, which is a container for many Token items
    #Tokens represent individual words in the corpus, and contain left and right context as well as annotations
    corpus = loadCorpus()
    
    #get the seed rules
    seedrules = loadSeedRules()
    rulestack.append(seedrules)
    allrules.extend(seedrules)
        
    #identify names via seed rules
    newNames = namesfromrules.run(corpus, seedrules)
    names.append(newNames)

    contextualIteration = False

    iterations = int(input("please enter the number of iterations: "))
    maxrules = int(input("please enter the number of rules to keep between iterations: "))
    
    #begin iterating
    i = 0;
    while i < iterations:
        if contextualIteration:
            print("iteration " + str(i + 1) + ": find contextual rules")
            newRules = contextualfromnames.run(corpus, allrules, names[i], maxrules)
            rulesFound = len(list(newRules.rules))
            print("found " + str(rulesFound) + " new contextual rules!")

            rulestack.append(newRules)
            allrules.extend(newRules)

            #get the names for the next iteration
            newNames = namesfromrules.run(corpus,newRules)
            print("top " + str(rulesFound) + " rules found " + str(len(newNames.tokens)) + " new names")
            names.append(newNames)
        else:
            print("iteration " + str(i + 1) + ": spelling")
            newRules = spellingfromnames.run(corpus, allrules, names[i], maxrules)
            rulesFound = len(list(newRules.rules))
            print("found " + str(rulesFound) + " new spelling rules!")

            rulestack.append(newRules)
            allrules.extend(newRules)
            
            #get the names for the next iteration
            newNames = namesfromrules.run(corpus,newRules)
            print("top " + str(rulesFound) + " rules found " + str(len(newNames.tokens)) + " new names")
            names.append(newNames)

        contextualIteration = not contextualIteration
        i += 1

    #debug output
    #i = 0
    #for rule in allrules:
    #    print("rule " + str(i) + ": " + str(rule.rtype) + " " + str(rule.contents) + " " + str(rule.strength))
    #    i += 1

    #really half assed output system, needs upgrading

    f = open("output.csv", 'wb')
    
    f.write("Rule,Rule Type,Strength\n".encode('utf-8'))
    for rule in allrules:
        f.write("{0},{1},{2}\n".format(str(rule.contents), str(rule.rtype), str(rule.strength)).encode('utf-8'))

    f.close()

#begin execution
main()