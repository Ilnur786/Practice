from pickle import load

with open("false_base/false_test_set_part2.pickle", 'rb') as f:
    var = load(f)

print(len(var))

with open("test_train/false_test_set.pickle", 'rb') as f:
    c = load(f)

print(type(c))