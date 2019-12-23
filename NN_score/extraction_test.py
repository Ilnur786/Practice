from pickle import load, dump
import logging


global_result = set()
test, train, doubles = set(), set(), set()
sig_test, sig_train = set(), set()
NUMBER2, NUMBER3 = {0}, {0}
# logging.basicConfig(filename="log.log", level=logging.INFO)
logger = logging.getLogger("my test")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("log.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


for numeric in range(0, 4000):
    tuples = load(open('/home/nadia/data/True_pairs_new/{}.pickle'.format(numeric), 'rb'))  # открываю файл
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        if TUPLE in global_result or (sig_b, sig_a, take_ml[2], take_ml[3]) in global_result:
            continue
        sig_test.update((sig_a, sig_b))
        test.add(take_ml)
        global_result.add(TUPLE)
        if len(test) == 1000:
            NUMBER2.add(max(NUMBER2) + 1)
            with open('/home/nadia/data/test/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            logger.info(f" test : {(len(NUMBER2)+1)*1000}")
            test.clear()
        if numeric == 4000 and take_ml == tuples[-1]:
            NUMBER2.add(max(NUMBER2) + 1)
            with open('/home/nadia/data/test/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
                test.clear()
with open('/home/nadia/data/sig_test/sig_test.pickle', 'wb') as f:
    dump(sig_test, f)
logger.info(f"All test unloaded. Number of files test : {len(NUMBER2)+1}")


for numeric in range(4000, 43492):
    tuples = load(open('/home/nadia/data/True_pairs_new/{}.pickle'.format(numeric), 'rb'))
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        if TUPLE in global_result or (sig_b, sig_a, take_ml[2], take_ml[3]) in global_result:
            continue
        if sig_a in sig_test or sig_b in sig_test:
            doubles.add(TUPLE)
        else:
            train.add(take_ml)
        global_result.add(TUPLE)
        if len(train) == 8000:
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/data/train/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            logger.info(f" train : {(len(NUMBER3)+1)*8000}")
            train.clear()
        if numeric == 43491 and take_ml == tuples[-1]:
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/data/train/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            train.clear()
with open('/home/nadia/data/test/doubles.pickle', 'wb') as f:
    dump(doubles, f)
logger.info(f"Number of train files for 8000 tuples : {len(NUMBER3)+1}. Number of test files for 1000 molecules : {len(NUMBER2)+1}. Number of doubles : {len(doubles)}")
print('10000 pickles processed')