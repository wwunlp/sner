#from itertools import izip

def main(data, options):
    train_key = 'data/target_train.KEY'
    train_target = 'data/target_train.RT'
    dev_key = 'data/target_dev.KEY'
    dev_target = 'data/target_dev.RT'
    dev_pred = 'data/dev_prediction.RT'

    train_names = set()
    dev_names = set()
    pred_names = set()
    
    total_train_names = addNames(train_key, train_target, train_names)
    total_dev_names = addNames(dev_key, dev_target, dev_names)
    total_pred_names = addNames(dev_key, dev_pred, pred_names)
    

    dev_unique_names = dev_names - train_names
    new_names = pred_names - train_names

    print ("Training found %d names. \nDev found %d names.\nUnique names in dev: %d" % (len(train_names), len(dev_names), len(new_names)))

    #for name in new_names:
    #    print(name)

    dev_key = open('data/target_dev.KEY', "r")
    dev_target = open('data/target_dev.RT', "r")
    dev_pred = open('data/dev_prediction.RT', "r")

    correct = 0
    missed = 0
    mislabeled = 0
    correct_names = set()

    for x, y, z in zip(dev_key, dev_target, dev_pred):
        x = x.split(',')[3].strip()
        y = y.strip()
        z = z.strip()
        
        if int(y) == 1:
            if int(z) == 1:
                if x in new_names:
                    print("Found correct new name: %s" % x)
                    correct_names.add(x)
                    correct += 1
            else :
                print("Missed the correct name: %s" % x)
                missed += 1

        else:
            if int(z) == 1:
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


main(None, None)
