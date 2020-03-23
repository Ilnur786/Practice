from pickle import load, dump
import random
from CGRtools.files import SDFwrite
from CGRtools.files import SDFread


global_result = set()
pairs = set()
NUMBER, NUMBER2, NUMBER3 = set(), set(), set()
SIG = set()
train = set()
test = set()
validation = set()

end = False
for numeric in range(43000, 43050):
    tuples = load(open('/home/nadia/data/True_pairs_new/{}.pickle'.format(numeric), 'rb'))
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        if (sig_b, sig_a) in pairs or (sig_a, sig_b) in pairs:
            continue
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        pairs.add((sig_a, sig_b))
        check_a = ([t[0] for t in global_result])
        check_b = ([t[1] for t in global_result])
        if sig_b in check_b or sig_b in check_a:
            train.add(take_ml)
        else:
            if len(test)*8 > len(train):
                train.add(take_ml)
            elif len(validation) < len(test):
                validation.add(take_ml)
            else:
                test.add(take_ml)
        global_result.add(TUPLE)
        if numeric == 43050:
            end = True
        if len(validation) == 1000 or end:
            number = max(NUMBER)+1
            NUMBER.add(number)
            with open('/home/nadia/data/validation/{}validation.pickle'.format(number)) as f:
                dump(validation, f)
            validation.clear()
            number = max(NUMBER2)
            NUMBER2.add(number)
            with open('/home/nadia/data/test/{}test.pickle'.format(number)) as f:
                dump(test, f)
            test.clear()
            number = max(NUMBER3)
            NUMBER3.add(number)
            with open('/home/nadia/data/train/{}train.pickle'.format(number)) as f:
                dump(train, f)
            train.clear()
print(len(train))
print(len(test))
print(len(validation))


