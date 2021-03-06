"""NER Model"""
from sner.classes import Display, Rule, Token
from sner.scripts.ner import contextualfromnames, namesfromrule
from sner.scripts.ner import spellingfromnames, updatetokenstrength
import matplotlib.pyplot as plt
import pandas as pd


def import_corpus(corpus_path, display):
    """
	Imports the corpus for the ner model, from a format of our own design.
	The format is a CSV containing individual words in the corpus, with columns
	containing the Tablet ID, the line number within that tablet, the word
	number within that line, the word itself, and any annotation associated
	with that word.

    Args:
        corpus_path (str): Path of the corpus file.
		display (Display): Utility object used to print the progress of scanning
						   the corpus file.

    Returns:
        corpus (set): Set of Token objects, properly initialized from the input
					  data.

    Raises:
        None

    """

    corpus = set()

    cols = ['Tablet ID', 'Line Number', 'Word Number', 'Word', 'Word Type']

    data = pd.read_csv(corpus_path, names=cols, header=0)
    for i in range(len(data) - 1):
        if data.loc[i, 'Word Number'] > 0:
            left_context = data.loc[i - 1, 'Word']
        else:
            left_context = None

        word = data.loc[i, 'Word']

        if data.loc[i, 'Line Number'] == data.loc[i + 1, 'Line Number']:
            right_context = data.loc[i + 1, 'Word']
        else:
            right_context = None

        word_type = Token.find_type(data.loc[i, 'Word Type'])

        token = Token(left_context, word, right_context, word_type)
        corpus.add(token)

        display.update_progress_bar(i + 1, len(data))

    return corpus


def import_seed_rules(seed_rules_path, display):
    """
    This function will read the seed rule file, and return the contents as
    a set.  The file is a CSV formatted with columns containing the rule type,
	the contents of the rule, and its strength rating (the probability that a
	token is a name if the rule applies to said token).

    Args:
        rulename (str): Location of seed rules file.

    Returns:
        rules (set): Set of Rule objects corresponding to the rules in the
            seed rules file.

    Raises:
		None

    """

    seed_rules = set()

    cols = ['Rule Type', 'Rule', 'Strength']

    data = pd.read_csv(seed_rules_path, names=cols, header=0)
    for i in range(len(data) - 1):
        rule_type = Rule.find_type(data.loc[i, 'Rule Type'])
        rule = data.loc[i, 'Rule']
        strength = data.loc[i, 'Strength']
        rule = Rule(rule_type, rule, strength)
        seed_rules.add(rule)

        display.update_progress_bar(i + 1, len(data))

    return seed_rules


def assess_strength(rules, corpus, config):
    """
	Evaluates the accuracy of the strength rating of the passed-in rules.  This
	is useful because the ner model will generate rules in an unsupervised
	fashion.  This function gets used to evaluate the performance of that
	process.

    Args:
        rules (set): A set of Rule objects to be evaluated
        corpus (set): A set of Token objects, representing the entire Garshana
					  corpus.

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

    est_false_positives = 0

    print("rule performance:")
    print("calculating...", end='\r')

    i = 0
    cols = {
        'Iteration'    : [],
        'Rule'         : [],
        'Type'         : [],
        'Strength'     : [],
        'True Strength': [],
        'Occurrences'  : []
    }
    output = pd.DataFrame(data=cols)

    x_vals = []
    y_vals = []
    rule_num = 1

    for rule in rules:
        names = namesfromrule.main(corpus, rule)
        real_names = 0
        total_names = len(names)

        for token in names:
            if token.type == Token.Type.personal_name:
                real_names += 1

        if total_names == 0:
            true_strength = 0
        else:
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

        i += 1
        output.loc[i, 'Iteration']     = rule.iteration
        output.loc[i, 'Rule']          = rule.contents
        output.loc[i, 'Type']          = rule.type.name
        output.loc[i, 'Strength']      = rule.strength
        output.loc[i, 'True Strength'] = true_strength
        output.loc[i, 'Occurrences']   = rule.occurrences

    output_path = config['path'].format(
        'ner',
        time.strftime('%Y%m%d_%H%M'),
        'output.csv'
    )
    output.to_csv(path_or_buf=output_path)

    print("               ", end='\r')
    print("percentage of bad rules:    {}%".format(
        100 * bad_rules / len(rules)
    ))
    print("percentage of bad context:  {}%".format(
        100 * bad_context / total_context
    ))
    print("percentage of bad spelling: {}%".format(
        100 * bad_spelling / total_spelling
    ))
    print("average delta value:        {}%".format(
        100 * total_delta / len(rules)
    ))

    plt.xlabel('Rules')
    plt.ylabel('Delta')
    plt.title('Plot of Delta per Rule')
    plt.plot(x_vals, y_vals, 'ro')
    plt.axis([min(x_vals), max(x_vals), min(y_vals), max(y_vals)])
    plt.show()

    sort_y = sorted(y_vals)
    plt.xlabel('')
    plt.ylabel('Delta')
    plt.title('Delta Sorted')
    plt.plot(x_vals, sort_y, 'ro')
    plt.axis([min(x_vals), max(x_vals), min(sort_y), max(sort_y)])
    plt.show()


def get_new_names(corpus, names, rules):
    """
    Meant to use the provided ruleset to scan the corpus for new names.
    It will then return the names in quesiton, which will be used
    to generate more rules.

	Basically, it grabs all tokens from the corpus matching the rules in
	question and then return them as a set.  The names parameter lets you
	specify tokens that are already recognized as names, allowing you to
	retrieve only new name results.

    Args:
        corpus (set): Set of Token objects representing the entire Garshana
					  corpus.
        names (set): Set of Tokens already recognized as names.
        rules (set): Set of Rule objects used to find new names

    Returns:
        new_names (set): Set of Token objects

    Raises:
        None

    """

    new_names = set()

    for rule in rules:
        results = namesfromrule.main(corpus, rule)
        for name in results:
            if name not in names:
                new_names.add(name)

    return new_names


def print_precision_and_recall(selected_elements, relevant_elements, i, log):
    """
	Prints the precision, recall, and F1 score of the algorithm.  Used by
	passing in tokens in the selected_elements parameter.  These tokens are
	the tokens considered to be names.  Relevant elements is just the total
	number of names in the corpus.

    Args:
        selected_elements (set): Set of Token objects representing names as
								 identified by the algorithm.
        relevant_elements (int): Total number of names that exist in the
								 corpus.
        i (int): Index of current log entry.
		log (pandas.DataFrame): Data structure containing logs

    Returns:
		None

    Raises:
        None

    """

    positives = 0.0
    true_positives = 0.0
    precision = 0.0
    recall = 0.0
    f1_score = 0.0

    for token in selected_elements:
        positives += 1.0
        if token.type == Token.Type.personal_name:
            true_positives += 1.0

    if positives == 0.0:
        precision = 0.0
    else:
        precision = true_positives / positives * 100

    if relevant_elements == 0.0:
        recall = 0.0
    else:
        recall = true_positives / relevant_elements * 100

    if precision + recall == 0.0:
        f1_score = 0.0
    else:
        f1_score = 2.0 * precision * recall / (precision + recall)

    print("Precision: {:06.4f}%".format(precision))
    print("Recall:    {:06.4f}%".format(recall))
    print("F1 Score:  {:06.4f}\n".format(f1_score))

    log.loc[i, 'Precision'] = precision
    log.loc[i, 'Recall'] = recall
    log.loc[i, 'F1 Score'] = f1_score


def main(config):
    """
    Rules and names will be lists of RuleSets or TokenSets.
    These sets will represent the results of various iterations of
    the algorithm. So index 0 of rules would be the first rule set
    (seed rules) and 1 would be the first rules generated and used by the
    algorithm itself. Index zero of names would be the names that came from
    the seed rules. Index one the rules that came from rule set 1. And so on.

    Args:
        config (dict): Dictionary containing confiruation information, such as
					   the location of the input files, as well as various
					   flags and runtime parameters.  (defined in sner.py)

    Returns:
        None

    Raises:
        None

    """

    path = config['path']
    corpus_path = path + config['corpus']
    seed_rules_path = path + config['seed-rules']
    iterations = config['iterations']
    max_rules = config['max_rules']

    log_cols = {
        'Iteration Type': [],
        'New Rules'     : [],
        'New Names'     : [],
        'Precision'     : [],
        'Recall'        : [],
        'F1 Score'      : []
    }
    log = pd.DataFrame(data=log_cols)

    display = Display()

    display.start("Importing Corpus: {}".format(corpus_path))
    corpus = import_corpus(corpus_path, display)
    display.finish()

    display.start("Importing Seed Rules: {}".format(seed_rules_path))
    seed_rules = import_seed_rules(seed_rules_path, display)
    display.finish()

    updatetokenstrength.main(corpus, seed_rules)

    rule_set = set()
    rule_set = rule_set.union(seed_rules)

    name_set = set()
    new_names = get_new_names(corpus, name_set, seed_rules)
    name_set = name_set.union(new_names)

    relevant_elements = 0.0
    for token in corpus:
        if token.type == Token.Type.personal_name:
            relevant_elements += 1.0

    display.start(
        "Starting Model:\n   {} iterations, {} max rules".format(
            iterations,
            max_rules
        )
    )
    for i in range(1, iterations + 1):
        if i % 2 == 0:
            iter_type = 'context'
            get_new_rules = contextualfromnames.main
        else:
            iter_type = 'spelling'
            get_new_rules = spellingfromnames.main

        print("Iteration {}: find {} rules".format(i, iter_type))

        new_rules = get_new_rules(
            corpus,
            rule_set,
            name_set,
            max_rules,
            i,
            config,
            display
        )

        print("Found {} new {} rules".format(len(new_rules), iter_type))

        rule_set = rule_set.union(new_rules)
        updatetokenstrength.main(corpus, rule_set)

        new_names = get_new_names(corpus, name_set, new_rules)
        name_set = name_set.union(new_names)

        print("top {} rules found {} new names".format(
            len(new_rules), len(new_names)))

        log.loc[i, 'Iteration Type'] = iter_type
        log.loc[i, 'New Rules'] = len(new_rules)
        log.loc[i, 'New Names'] = len(new_names)
        print_precision_and_recall(name_set, relevant_elements, i, log)

    display.finish()
    log.to_csv(path_or_buf=data.log)
    assess_strength(rule_set, corpus, data)
