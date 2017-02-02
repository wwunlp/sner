#from itertools import izip

def main(config):
    train_key = 'data/target_train.KEY'
    train_target = 'data/target_train.RT'
    atf_key = 'data/target_atf.KEY'
    atf_pred = 'data/atf_prediction.RT'

    train_names = set()
    pred_names = set()
    
    total_train_names = addNames(train_key, train_target, train_names, 3)
    total_pred_names = addNames(atf_key, atf_pred, pred_names, 2)
    

    new_names = pred_names - train_names

    print ("Training found %d names. \nUnique names in atf: %d" % (len(train_names), len(new_names)))

    print ()
    print ("Total names in train: %d\nTotal names in pred: %d\n" % (total_train_names, total_pred_names))
    
    print ("Training has %d unique names.\nUnique names found in pred: %d"
           % (len(train_names), len(new_names)))
    

def addNames(file_key, file_target, names, index):
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

    return name_count


