from pickle import load, dump

with open("test_train/false_test_set_part2.pickle", 'rb') as f:
    false_test_set_part2 = load(f)

with open("test_train/false_test_set.pickle", 'rb') as f:
    false_test_set = load(f)

false_test_set_full = set()
false_test_set_full.update(false_test_set)
false_test_set_full.update(false_test_set_part2)

with open('test_train/false_test_set_full.pickle', 'wb') as f:
    dump(false_test_set_full, f)

print(len(false_test_set_full))

#файлов в true_test_set_full = 567412