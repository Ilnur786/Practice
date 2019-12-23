from pickle import load, dump
import logging


global_result = set()
NUMBER, NUMBER2, NUMBER3 = {0}, {0}, {0}
train, test, validation = set(), set(), set()
sig_train = set()
# logging.basicConfig(filename="ancient.log", level=logging.INFO)
logger = logging.getLogger("my test")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("train.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


for numeric in range(0, 10000):
    tuples = load(open('/home/nadia/data/True_pairs_new/{}.pickle'.format(numeric), 'rb'))
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        if TUPLE in global_result or (sig_b, sig_a, take_ml[2], take_ml[3]) in global_result:
            continue
        train.add(take_ml)
        sig_train.update((sig_a, sig_b))
        global_result.add(TUPLE)
        if len(train) == 8000:
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/data/train3/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            train.clear()
            logger.info(f" train : {max(NUMBER3)*8000}")


for numeric in range(10000, 43492):
    tuples = load(open('/home/nadia/data/True_pairs_new/{}.pickle'.format(numeric), 'rb'))
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        if TUPLE in global_result or (sig_b, sig_a, take_ml[2], take_ml[3]) in global_result:
            continue
        if (sig_a in sig_train) or (sig_b in sig_train):
            train.add(take_ml)
            sig_train.update((sig_a, sig_b))
        else:
            if len(validation) < len(test):
                validation.add(take_ml)
            else:
                test.add(take_ml)
        global_result.add(TUPLE)
        if len(validation) == 1000:
            NUMBER.add(max(NUMBER) + 1)
            with open('/home/nadia/data/validation3/{}validation.pickle'.format(max(NUMBER)), 'wb') as f:
                dump(validation, f)
            validation.clear()
            NUMBER2.add(max(NUMBER2) + 1)
            with open('/home/nadia/data/test3/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            test.clear()
            logger.info(f" train : {max(NUMBER3)*8000},  test : {max(NUMBER2)*1000},"
                        f" validation : {max(NUMBER)*1000}")
        if len(train) == 8000:
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/data/train3/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            train.clear()
            logger.info(f" train : {max(NUMBER3)*8000},  test : {max(NUMBER2)*1000},"
                        f" validation : {max(NUMBER)*1000}")
        if numeric == 43491 and take_ml == tuples[-1]:
            NUMBER3.add(max(NUMBER3) + 1)
            NUMBER2.add(max(NUMBER2) + 1)
            NUMBER.add(max(NUMBER) + 1)
            with open('/home/nadia/data/train3/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            with open('/home/nadia/data/test3/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            with open('/home/nadia/data/validation3/{}validation.pickle'.format(max(NUMBER)), 'wb') as f:
                dump(validation, f)
            logger.info(f" train : {(max(NUMBER3)-1)*8000 + len(train)},  test : {(max(NUMBER2)-1)*1000 + len(test)},"
                        f" validation : {(max(NUMBER)-1)*1000 + len(validation)}")
            train.clear()
            test.clear()
            validation.clear()
print('train files:', max(NUMBER3), ' test files:', max(NUMBER2),
      'validation files:', max(NUMBER))