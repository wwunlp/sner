import random
import codecs

def main(config):

    path = config['path']
    corpus = config['corpus']

    use_atf = config['flags']['use_atf']
    
    train_key = path + 'target_train.KEY'
    train_target = path + 'target_train.RT'
    dev_key = path + 'target_dev.KEY'
    dev_target = path + 'target_dev.RT'
    dev_pred = path + 'dev_prediction.RT'

    atf_key = path + 'target_atf.KEY'
    atf_pred = path + 'atf_prediction.RT'
    

    train_names = set()
    dev_names = set()
    pred_names = set()

    atf_names = set()

    atf_output = []
    
    total_train_names = addNames(train_key, train_target, train_names)
    total_dev_names = addNames(dev_key, dev_target, dev_names)
    total_pred_names = addNames(dev_key, dev_pred, pred_names)

    total_atf_names = None
    if use_atf:
        total_atf_names = addATFNames(atf_key, atf_pred, atf_names, train_names, atf_output)

    dev_unique_names = dev_names - train_names
    new_names = pred_names - train_names    
    atf_unique_names = None
    if use_atf:
         atf_unique_names = atf_names - train_names

    print ("Training found %d names. \nDev found %d names.\nUnique names in dev: %d" % (len(train_names), len(dev_names), len(new_names)))

    # Exit early when looking at ATF names.
    if use_atf:
        print("Names found in atf: %d\nUnique names found in atf: %d" % (len(atf_names), len(atf_unique_names)))
        outputATF(config, atf_output)
        return


        
    dev_key = open(dev_key, "r")
    dev_target = open(dev_target, "r")
    dev_pred = open(dev_pred, "r")

    correct = 0
    missed = 0
    mislabeled = 0
    correct_names = set()

    verbose = config['flags']['verbose']

    for x, y, z in zip(dev_key, dev_target, dev_pred):
        x = x.split(',')[3].strip()
        y = y.strip()
        z = z.strip()
        
        if int(y) == 1:
            if int(z) == 1:
                if x in new_names:
                    if verbose:
                        print("Found correct new name: %s" % x)
                    correct_names.add(x)
                    correct += 1
            else :
                if verbose:
                    print("Missed the correct name: %s" % x)
                missed += 1

        else:
            if int(z) == 1:
                if verbose:
                    print("Mislabeled name: %s" % x)
                mislabeled += 1


    
    print ()
    print ("Total names in train: %d\nTotal names in dev: %d\nTotal names in pred: %d\n" % (total_train_names, total_dev_names, total_pred_names))
    
    print ("Training has %d unique names.\nDev has %d unique names.\nUnique names to dev: %d\nUnique names found in pred: %d"
           % (len(train_names), len(dev_names), len(dev_unique_names), len(new_names)))
    print ("Correct unique names in pred: %d / %d [%.2f%%]\n" % (len(correct_names), len(dev_unique_names), 100 * len(correct_names) / len(dev_unique_names)))
    
    print ("Correct unique occurrences: %d" % (correct))
    print ("Missed names: %d / %d [%.2f%%]" % (missed, total_dev_names, 100 * missed / total_dev_names))
    print ("Mislabeled names: %d / %d [%.2f%%]" % (mislabeled, total_pred_names, 100 * mislabeled / total_pred_names))


def outputATF(config, output_list):
    path = config['path']
    count = 0
    unique_names = set()
    selected = []
    while count < 50:
        line = random.choice(output_list)
        name = line.split(',')[2].strip()
        if name not in unique_names:
            unique_names.add(name)
            selected.append(line.split(','))
            count += 1
    ordered = sorted(selected, key=lambda x: float(x[0]))

    corpus = codecs.open(path + config['corpus'], 'r', encoding = 'utf-8')

    lineid = -1
    nextname = 0
    
    for line in corpus:
        
        lineid += 1        

        if lineid == int(ordered[nextname][0]):
            print(ordered[nextname])
            print(line.strip())
            print()
            nextname += 1

        if nextname >= len(ordered):
            break


    print(lineid)
    print(nextname)
    print(len(ordered))


def numeric_compare(x, y):
    return int(x) - int(y)

def addATFNames(file_key, file_target, names, train_names, output_list):
    key = open(file_key, "r")
    target = open(file_target, "r")
    name_count = 0
    for x, y in zip(key, target):
        x = x.strip()
        y = y.strip()
        if int(y) == 1:
            name_count += 1
            name = x.split(',')[2].strip()
            if not name not in train_names:
                names.add(name)
                output_list.append(x)

    return name_count

    

def addNames(file_key, file_target, names):
    key = open(file_key, "r")
    target = open(file_target, "r")
    name_count = 0
    for x, y in zip(key, target):
        x = x.strip()
        y = y.strip()
        if int(y) == 1:
            name_count += 1
            name = x.split(',')[3].strip()
            names.add(name)

    return name_count



