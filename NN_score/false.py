from pickle import load, dump
import logging


global_result = set()
NUMBER, NUMBER2, NUMBER3 = {0}, {0}, {0}
train, test, doubles = set(), set(), set()
sig_train = load(open('/home/nadia/work/sig_train', 'wb'))
sig_test = load(open('/home/nadia/work/sig_test', 'wb'))
# logging.basicConfig(filename="false.log", level=logging.INFO)
logger = logging.getLogger("my test")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("false.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info(" Program start")
for numeric in range(1268, 13786):
    tuples = load(open('/home/nadia/adelia/False_pairs/{}.pickle'.format(numeric), 'rb'))
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        if TUPLE in global_result or (sig_b, sig_a, take_ml[2], take_ml[3]) in global_result:
            continue
        if (sig_a in sig_train) or (sig_b in sig_train):
            if (sig_a in sig_test) or (sig_b in sig_test):
                doubles.add(take_ml)
            else:
                train.add(take_ml)
                sig_train.update((sig_a, sig_b))
        else:
            test.add(take_ml)
            sig_test.update((sig_a, sig_b))
        global_result.add(TUPLE)
        if len(doubles) == 1000:
            NUMBER.add(max(NUMBER) + 1)
            with open('/home/nadia/work/doubles_false/{}doubles.pickle'.format(max(NUMBER)), 'wb') as f:
                dump(doubles, f)
            doubles.clear()
        if len(test) == 1000:
            NUMBER2.add(max(NUMBER2) + 1)
            with open('/home/nadia/work/test_false/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            test.clear()
            logger.info(f" train : {max(NUMBER3)*1000},  test : {max(NUMBER2)*1000},"
                        f" doubles : {max(NUMBER)*1000}")
        if len(train) == 1000:
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/work/train_false/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            train.clear()
            logger.info(f" train : {max(NUMBER3)*1000},  test : {max(NUMBER2)*1000},"
                        f" doubles : {max(NUMBER)*1000}")
            d = sig_train.intersection(sig_test)
            if d:
                logger.info("Doubles appeared :", len(d))
        if numeric == 13785 and take_ml == tuples[-1]:
            NUMBER3.add(max(NUMBER3) + 1)
            NUMBER2.add(max(NUMBER2) + 1)
            NUMBER.add(max(NUMBER) + 1)
            with open('/home/nadia/work/train_false/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            with open('/home/nadia/work/test_false/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            with open('/home/nadia/work/doubles_false/{}doubles.pickle'.format(max(NUMBER)), 'wb') as f:
                dump(doubles, f)
            logger.info(f" train false : {(max(NUMBER3)-1)*1000 + len(train)},  test false : {(max(NUMBER2)-1)*1000 + len(test)},"
                        f" doubles false : {(max(NUMBER)-1)*1000 + len(doubles)}")
            train.clear()
            test.clear()
            doubles.clear()
print('train false files:', max(NUMBER3), ' test false files:', max(NUMBER2),
      'doubles false files:', max(NUMBER))
f = sig_train.intersection(sig_test)
print('Doubles', len(f))

