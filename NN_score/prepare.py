# -*- coding: utf-8 -*-
from CGRtools.files import SDFwrite
from pickle import load


global_result = set()
pairs = set()
molecules = {}
NUMBER = set()
SIG = set()
train = set()
test = set()
validation = set()


def get_set(path, number):
    for num in range(number):
        tuples = load(open('{}/{}.pickle'.format(path, num), 'rb'))
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
            if sig_a in check_a or sig_b in check_b or sig_a in check_b or sig_b in check_a:
                train.add(take_ml)
            else:
                if len(test) <= len(validation):
                    test.add(take_ml)
                else:
                    validation.add(take_ml)
            global_result.add(TUPLE)


for number in range(4, 7):
    get_set('/home/nadia/data/True_pairs_new', number)
