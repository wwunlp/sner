import random
import codecs
import operator

unique_names = False


def main(config):
    global unique_names    
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

    flags = config['flags']
    if flags['disjoint_names'] == True:
        uniqueNames = True
        print("Using disjoint name sets for train / dev.")
    else:
        uniqueNames = False

    

    train_names = set()
    dev_names = set()
    pred_names = set()
    dev_output = []
    
    atf_names = set()
    atf_output = []
    
    
    total_train_names = addNames(train_key, train_target, train_names)
    total_dev_names = add_names_and_unique(dev_key, dev_target, dev_names, train_names, dev_output)
    total_pred_names = addNames(dev_key, dev_pred, pred_names)

    total_atf_names = None
    if use_atf:
        total_atf_names = add_names_and_unique(atf_key, atf_pred,
                                               atf_names, train_names, atf_output, 2)

    dev_unique_names = dev_names - train_names
    new_names = pred_names - train_names    
    atf_unique_names = None
    if use_atf:
         atf_unique_names = atf_names - train_names

    print ("Training found %d names." % len(train_names))

    if not use_atf:
        print("dev found %d names." % len(dev_names))
        print("Unique names in dev: %d" % (len(new_names)))
        print("dev name occurrences: %d" % total_dev_names)
        print("dev unique name occurrences: %d - %.3f%%" % (len(dev_output), 100 * len(dev_output) / total_dev_names))
        
    # Exit early when looking at ATF names.             
    if use_atf:
        print("Names found in atf: %d" % len(atf_names))
        print("Unique names found in atf: %d" % len(atf_unique_names))
        print("Total name occurrences in ATF: %d" % total_atf_names)
        print("Unique name occurrences in ATF: %d - %.3f%%" % (len(atf_output), 100 * len(atf_output) /
                                                               total_atf_names ))
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
    print ("Correct unique names in pred: %d / %d [%.2f%%]\n" %
           (len(correct_names), len(dev_unique_names), 100 * len(correct_names) / len(dev_unique_names)))
    
    print ("Correct unique occurrences: %d" % (correct))
    print ("Missed names: %d / %d [%.2f%%]" % (missed, total_dev_names, 100 * missed / total_dev_names))
    print ("Mislabeled names: %d / %d [%.2f%%]" %
           (mislabeled, total_pred_names, 100 * mislabeled / total_pred_names))


def outputATF(config, output_list):
    path = config['path']
    count = 0
    unique_names = set()
    selected = []

    name_counts = {}
    name_line = {}

    for x in output_list:
        name = x.split(',')[2].strip()
        if name not in name_counts.keys():
            name_counts[name] = 0
        name_counts[name] = name_counts[name] + 1
        name_line[name] = x

    sorted_names = sorted(name_counts.items(), key=operator.itemgetter(1), reverse=True)

    while count < 100:
        #print(sorted_names[count])        
        line = name_line[sorted_names[count][0]]
        #print(line)
        #print()
        result = line.split(',')
        if len(result) > 3:
            combo = ','.join(result[2:])
            result[2:] = []
            result.append(combo)
        result.append(sorted_names[count][1])
        selected.append(result)
        count += 1
    
    #while count < 3:
    #    line = random.choice(output_list)
    #    name = line.split(',')[2].strip()
    #    if name not in unique_names:
    #        unique_names.add(name)
    #        selected.append(line.split(','))
    #        count += 1

    print("----------------------")
    ordered = sorted(selected, key=lambda x: float(x[0]))

    corpus = codecs.open(path + config['corpus'], 'r', encoding = 'utf-8')

    lineid = -1
    nextname = 0
    
    for line in corpus:
        
        lineid += 1        

        if lineid == int(ordered[nextname][0]):
            nn = ordered[nextname]
            print("%s, %s, %s, %s" % (nn[0].strip(), nn[1].strip(), nn[3], nn[2].strip()))
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

def add_names_and_unique(file_key, file_target, names, train_names, output_list, index=3):
    global unique_names
    key = open(file_key, "r")
    target = open(file_target, "r")
    name_count = 0
    for x, y in zip(key, target):
        x = x.strip()
        y = y.strip()
        if int(y) == 1:
            name_count += 1
            name = x.split(',')[index].strip()
            names.add(name)
            if name not in train_names:              
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



