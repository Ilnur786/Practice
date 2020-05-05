from pickle import load

with open("test_train/intersection_dict.pickle", 'rb') as f:
    intersection_dict = load(f)

with open('test_train/false_test_molecules_ids.pickle', 'rb') as f:
    false_test_molecules_ids = load(f)

with open('test_train/false_train_molecules_ids.pickle', 'rb') as f:
    false_train_molecules_ids = load(f)

with open('test_train/true_train_molecules_ids.pickle', 'rb') as f:
    true_train_molecules_ids = load(f)

with open('test_train/true_test_molecules_ids.pickle', 'rb') as f:
    true_test_molecules_ids = load(f)

if false_train_molecules_ids & true_train_molecules_ids:
    print('a')
if false_test_molecules_ids & true_test_molecules_ids:
    print('b')
if false_test_molecules_ids & true_train_molecules_ids:
    print('c')
if false_test_molecules_ids & false_train_molecules_ids:
    print('d')
if false_train_molecules_ids & true_test_molecules_ids:
    print('e')
if false_train_molecules_ids & false_test_molecules_ids:
    print('f')

print(len(false_test_molecules_ids))
