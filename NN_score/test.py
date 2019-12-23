from pickle import load, dump
import logging


global_result, doubles = set(), set()
NUMBER, NUMBER2, NUMBER3 = {0}, {0}, {0}
train, test, validation = [], [], []
sig_train, sig_test = set(), set()
# logging.basicConfig(filename="ancient.log", level=logging.INFO)
logger = logging.getLogger("my test")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("new.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


for numeric in range(0, 43492):
    tuples = load(open('/home/nadia/data/True_pairs_new/{}.pickle'.format(numeric), 'rb'))  # открываю файл
    for take_ml in tuples:
        a = take_ml[0]
        b = take_ml[1]
        sig_a = bytes(a)
        sig_b = bytes(b)
        TUPLE = (sig_a, sig_b, take_ml[2], take_ml[3])
        # проверяю, были ли такие же тюплы ранее или тюплы с помененными положениями А и Б
        if TUPLE in global_result or (sig_b, sig_a, take_ml[2], take_ml[3]) in global_result:
            continue
        # проверяю были ли такие же либо а, либо б ранее трайн, если были то добавляю также в трайн
        if (sig_a in sig_train) or (sig_b in sig_train):
            if (sig_a in sig_test) or (sig_b in sig_test):
                doubles.add(TUPLE)
            else:
                train.append(take_ml)
                sig_train.update((sig_a, sig_b))
        # если же а и б не встречались ранее в трайн, то добавляю в тест, вал или трайн
        # (если ранее мы не добовляли в тест) в зависимости от их колличества
        else:
            if (sig_a in sig_test or sig_b in sig_test) or len(test)*8 < len(train):
                if len(validation) < len(test):
                    validation.append(take_ml)
                    sig_test.update((sig_a, sig_b))
                else:
                    test.append(take_ml)
                    sig_test.update((sig_a, sig_b))
            else:
                train.append(take_ml)
                sig_train.update((sig_a, sig_b))

        global_result.add(TUPLE)  # добавляю тюпл в глобал
        if len(validation) == 1000:
            NUMBER.add(max(NUMBER) + 1)
            with open('/home/nadia/data/validation2/{}validation.pickle'.format(max(NUMBER)), 'wb') as f:
                dump(validation, f)
            validation = []
            NUMBER2.add(max(NUMBER2) + 1)
            with open('/home/nadia/data/test2/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            test = []
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/data/train2/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train[:8000], f)
            train = train[8000:]
            logger.info(f" train : {max(NUMBER3)*8000},  test : {max(NUMBER2)*1000},"
                        f" validation : {max(NUMBER)*1000}, doubles : {len(doubles)}")
        # если длина трайн достигла 8000, то сгружаем трайн полностью
        if len(train) == 16000:
            NUMBER3.add(max(NUMBER3) + 1)
            with open('/home/nadia/data/train2/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train[8000:], f)
            train = train[:8000]
            logger.info(f" train : {max(NUMBER3)*8000},  test : {max(NUMBER2)*1000},"
                        f" validation : {max(NUMBER)*1000}, doubles : {len(doubles)}")
        # когда дошли до последнего тюпла последней молекулы все сгружаем в файл
        if numeric == 43491 and take_ml == tuples[-1]:
            NUMBER3.add(max(NUMBER3) + 1)
            NUMBER2.add(max(NUMBER2) + 1)
            NUMBER.add(max(NUMBER) + 1)
            with open('/home/nadia/data/train2/{}train.pickle'.format(max(NUMBER3)), 'wb') as f:
                dump(train, f)
            with open('/home/nadia/data/test2/{}test.pickle'.format(max(NUMBER2)), 'wb') as f:
                dump(test, f)
            with open('/home/nadia/data/validation2/{}validation.pickle'.format(max(NUMBER)), 'wb') as f:
                dump(validation, f)
            logger.info(f" train : {(max(NUMBER3)-1)*8000 + len(train)},  test : {(max(NUMBER2)-1)*1000 + len(test)},"
                        f" validation : {(max(NUMBER)-1)*1000 + len(validation)}, doubles : {len(doubles)}")
            train.clear()
            test.clear()
            validation.clear()
with open('/home/nadia/data/test2/doubles.pickle', 'wb') as f:
    dump(doubles, f)
print(len(doubles))
print('train files:', max(NUMBER3), ' test files:', max(NUMBER2),
      'validation files:', max(NUMBER)*1000, 'doubles:', len(doubles))
print('Intersection', len(sig_train.intersection(sig_test)))




