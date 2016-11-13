from classes import Rule, Token, TokenSet
from scripts.ner import contextualfromnames, namesfromrule
from scripts.ner import spellingfromnames, updatetokenstrength
import matplotlib.pyplot as plt
from enum import Enum

def tokenize_corpus(corpus_loc):
    """
    Args:
        corpus_loc (str): Location of corpus file.

    Returns:
        corpus (TokenSet): Set of Token objects.

    Raises:
        None

    """
    
    try:
        corpus_file = open(corpus_loc, 'r')
    except:
        raise IOError("ERROR: Unable to open file: " + rulename)
    
    corpus_list = []
    
    next(corpus_file) # Skip headers
    for line in corpus_file:
        line = line.replace('\n', '')
        corpus_list.append(line.split(','))

    corpus_file.close()

    corpus = TokenSet()

    # Convert the line into the appropriate format
    # Each entry being a three element list, containing left context,
    # token, right context

    rawIter = iter(corpus_list)
    line = next(rawIter)
    tabletID = line[0]
    
    """
    This is the token constructor.
    Args:
        The left context for the token, the token, right context, and token type
        Right context assumed to be nothing, until set otherwise.

    Returns:
        The token adjacent to the current token. (?)

    Raises:
        None

    """
    prevToken = Token(None, line[3], None, Token.get_type(line[4]))

    for line in rawIter:
        if(line[0] == tabletID):
            token = Token(prevToken, line[3], None, Token.get_type(line[4]))

            prevToken.right_context = str(token)
            corpus.add(prevToken)

            prevToken = token

        else:
            corpus.add(prevToken)

            tabletID = line[0]
            token = Token(None, line[3], None, Token.get_type(line[4]))
            prevToken = token

    corpus.add(prevToken)

    return corpus


def tokenize_seed_rules(rulename):
    """
    This function will read the seed rule file, and return the contents as
    a set.
    Args:
        rulename (str): Location of seed rules file.

    Returns:
        rules (set): Set of Rule objects corresponding to the rules in the
            seed rules file.

    Raises:
        Error printed if unable to open rulename file.

    """
    rules = set()

    try:
        rulefile = open(rulename, "r")
    except:
        raise IOError("ERROR: Unable to open file: " + rulename)

    # Skip the first line since its column identifiers.
    next(rulefile)
    for line in rulefile:
        # Clean out the line returns as they will confuse the algorithm.
        line = line.replace('\n', '')
        ruledata = line.split(",")
        ruletype = Rule.Type.unset

        if ruledata[0] == "LEFT_CONTEXT":
            ruletype = Rule.Type.left_context
        elif ruledata[0] == "RIGHT_CONTEXT":
            ruletype = Rule.Type.right_context
        elif ruledata[0] == "SPELLING":
            ruletype = Rule.Type.spelling
        else:
            print("ERROR: rule parsing failed, invalid type: " + ruledata[0])
            sys.exit()

        rules.add(Rule(ruletype, ruledata[1], float(ruledata[2])))

    return rules


def assess_performance(corpus, options):
    """
    Find all names that pass a certain probability threshold, these will be
    considered our results
    Args:
        corpus (TokenSet): Set of Token objects
        options (Options): Options object with attributes of flags and
            variables.

    Returns:
        None

    Raises:
        None

    """

    name_threshold = options.accept_threshold
    names_found = TokenSet()

    print("performance so far:")

    for token in corpus:
        if token.name_probability > name_threshold:
            names_found.add(token)

    total_results = 0
    accurate_results = 0

    for token in names_found:
        total_results += token.occurrences
        if token.annotation == Token.Type.personal_name:
            accurate_results += token.occurrences

    total_names = 0

    for token in corpus:
        if token.annotation == Token.Type.personal_name:
            total_names += token.occurrences

    precision = accurate_results / total_results
    recall = accurate_results / total_names

    print("precision: {}%".format(100 * precision))
    print("recall: {}%".format(100 * recall))
    print("acceptance threshold: {}%".format(100 * name_threshold))
    #print("probability ratings off by {} ponts".format(100 * abs(name_threshold - precision)))


def assess_strength(rules, corpus, data):
    """
    Args:
        rules ():
        corpus ():

    Returns:
        None

    Raises:
        None

    """

    bad_rules = 0
    bad_context = 0
    bad_spelling = 0

    total_context = 0
    total_spelling = 0
    total_delta = 0

    print("rule performance:")
    print("calculating...", end='\r')

    f = open(data.output, 'wb')
    f.write("Iteration of Origin,Rule,Rule Type,Strength,Real Strength,Occurrences\n".encode('utf-8'))
    
    x_vals = []
    y_vals = []
    rule_num = 1

    for rule in rules:
        names = namesfromrule.main(corpus, rule)
        real_names = 0
        total_names = 0
        
        for token in names:
            if token.annotation == Token.Type.personal_name:
                real_names += rule.occurrences
            total_names += rule.occurrences

        true_strength = real_names / total_names
        delta = abs(true_strength - rule.strength)
        total_delta += delta

        x_vals.append(rule_num)
        rule_num += 1
        y_vals.append(delta)

        if rule.type == Rule.Type.spelling:
            total_spelling += 1
        else:
            total_context += 1

        #if a rule is more than 20% from its true value, it is 'bad'
        if delta > 0.2:
            bad_rules += 1
            if rule.type == Rule.Type.spelling:
                bad_spelling += 1
            else:
                bad_context += 1

        f.write("{0},{1},{2},{3},{4},{5}\n".format(str(rule.iteration), str(rule.contents), str(rule.type), str(rule.strength), str(true_strength), str(rule.occurrences)).encode('utf-8'))
        
    f.close()

    print("               ", end='\r')
    print("percentage of bad rules: {}%".format(
        100 * bad_rules / len(rules)
    ))
    print("percentage of bad context: {}%".format(
        100 * bad_context / total_context
    ))
    print("percentage of bad spelling: {}%".format(
        100 * bad_spelling / total_spelling
    ))
    print("average delta value: {}%".format(
        100 * total_delta / len(rules)
    ))

    plt.xlabel('Rules')
    plt.ylabel('Delta')
    plt.plot(x_vals, y_vals, 'ro')
    plt.axis([min(x_vals), max(x_vals), min(y_vals), max(y_vals)])
    plt.show()


def get_names(corpus, rules):
    """
    Meant to use the provided ruleset to scan the corpus for names.
    It will then return the names in quesiton, which will be used
    to generate more rules.

    Args:
        corpus (TokenSet): Set of Token objects
        rules (set): Set of Rule objects

    Returns:
        names (TokenSet): Set of Token objects

    Raises:
        None

    """

    names = TokenSet()

    for rule in rules:
        results = namesfromrule.main(corpus, rule)
        names.extend(results)

    return names


def main(data, options):
    """
    Rules and names will be lists of RuleSets or TokenSets.
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

    new_names = get_names(corpus, seed_rules)
    name_list = list(new_names)

    context_iter = False

    i = 0
    while i < iterations:
        if context_iter:
            print("iteration {}: find context rules".format(i + 1))
            new_rules = contextualfromnames.main(corpus, all_rules,
                                      name_list, max_rules, i, options)
            rules_found = len(new_rules)
            print("found {} new context rules!".format(rules_found))

        else:
            print("iteration {}: find spelling rules".format(i + 1))
            new_rules = spellingfromnames.main(corpus, all_rules,
                                      name_list, max_rules, i, options)
            rules_found = len(new_rules)
            print("found {} new spelling rules!".format(rules_found))

        updatetokenstrength.main(corpus, new_rules)

        rule_list.extend(list(new_rules))
        all_rules = all_rules.union(new_rules)

        new_names = get_names(corpus, new_rules)
        name_list.extend(list(new_names))

        print("top {} rules found {} new names".format(
            rules_found, len(new_names)))

        assess_performance(corpus, options)

        print("")

        context_iter = not context_iter
        i += 1

    assess_strength(all_rules, corpus, data)
