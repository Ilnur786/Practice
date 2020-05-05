from pickle import dump, load
import logging
from time import time

#false
start = time()
logger = logging.getLogger("exampleApp")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("test_train/false_train_test.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.info("Program started")

with open("test_train/false_base_ids.pickle", 'rb') as f:
    pickle_file = load(f)
print('загрузился файл false_base_ids.pickle ')

with open("test_train/true_train_molecules_ids.pickle", 'rb') as f:
    true_train_molecules_ids = load(f)
print('загрузился файл true_train_molecules_ids.pickle ')

with open("test_train/true_test_molecules_ids.pickle", 'rb') as f:
    true_test_molecules_ids = load(f)
print('загрузился файл true_test_molecules_ids.pickle ')

pickle_file = list(pickle_file)
false_test_set = set()
print('в false_test_set добавлены 1000 тюплов')

false_train_set = set()
false_test_molecules_ids = set()

false_train_molecules_ids = set()
print('в false_test_molecules_ids хранятся молекулы из тюплов false_test_set.pickle')

false_lost_set = set()
false_lost_molecules_ids = set()
a = 0
b = 0
c = 0
intersection_dict = {}

for i, kortezh in enumerate(set(pickle_file)):
    if i > 0 and i % 1000 == 0:
        if false_train_molecules_ids & false_test_molecules_ids:
            a += 1
            print('есть пересечение aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            logger.info('есть пересечение aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        elif false_train_molecules_ids & true_test_molecules_ids:
            b += 1
            print('есть пересечение bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
            logger.info('есть пересечение bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        elif false_test_molecules_ids & true_train_molecules_ids:
            intersection_dict[i] = kortezh
            c += 1
            print('есть пересечение cccccccccccccccccccccccccccccccccccccccccccccccccc')
            logger.info('есть пересечение cccccccccccccccccccccccccccccccccccccccccccc')
    if set(kortezh) & false_train_molecules_ids or set(kortezh) & false_test_molecules_ids or set(kortezh) & true_train_molecules_ids or set(kortezh) & true_test_molecules_ids:
        if set(kortezh) & false_train_molecules_ids and (not set(kortezh) & false_test_molecules_ids) and (not set(kortezh) & true_test_molecules_ids):
            false_train_set.add(kortezh)
            false_train_molecules_ids.update(kortezh)
        # elif (not set(kortezh) & false_train_molecules_ids) and (not set(kortezh) & true_train_molecules_ids) and (set(kortezh) & false_test_molecules_ids or set(kortezh) & true_test_molecules_ids):
        #     false_test_set.add(kortezh)
        #     false_test_molecules_ids.update(kortezh)
        elif set(kortezh) & false_test_molecules_ids and (not set(kortezh) & false_train_molecules_ids) and (not set(kortezh) & true_train_molecules_ids):
            if set(kortezh) & true_train_molecules_ids:
                continue
            else:
                false_test_set.add(kortezh)
                false_test_molecules_ids.update(kortezh)
        elif set(kortezh) & true_test_molecules_ids and (not set(kortezh) & true_train_molecules_ids) and (not set(kortezh) & false_train_molecules_ids):
            if set(kortezh) & true_train_molecules_ids:
                continue
            else:
                false_test_set.add(kortezh)
                false_test_molecules_ids.update(kortezh)
        elif set(kortezh) & true_train_molecules_ids and (not set(kortezh) & true_test_molecules_ids) and (not set(kortezh) & false_test_molecules_ids):
            false_train_set.add(kortezh)
            false_train_molecules_ids.update(kortezh)
        else:
            false_lost_set.add(kortezh)
            false_lost_molecules_ids.update(kortezh)
    else:
        false_test_set.add(kortezh)
        false_test_molecules_ids.update(kortezh)
    print('номер кортежа', i)
print('в false_train_set добавились все кортежи из false_base_ids.pickle, молекулы которых не входят false_test_molecules_ids')
print('в false_test_set добавились все кортежи из false_base_ids.pickle, молекулы которых не входят false_train_molecules_ids и в true_train_molecules_ids')
logger.info('пересекалось молекул false_train_molecules_ids & false_test_molecules_ids: {}'.format(a))
logger.info('пересекалось молекул false_train_molecules_ids & true_test_molecules_ids: {}'.format(b))
logger.info('пересекалось молекул false_test_molecules_ids & true_train_molecules_ids: {}'.format(c))

with open("test_train/false_test_set.pickle", 'wb') as m:
    dump(false_test_set, m)
print('false_test_set сохранился как false_test_set.pickle ')

with open("test_train/false_test_molecules_ids.pickle", 'wb') as j:
    dump(false_test_molecules_ids, j)
print('false_test_molecules_ids был схранен как false_test_molecules_ids.pickle')

with open("test_train/false_train_set.pickle", 'wb') as t:
    dump(false_train_set, t)
print('false_train_set был схранен как false_train_set.pickle')

with open("test_train/false_train_molecules_ids.pickle", 'wb') as i:
    dump(false_train_molecules_ids, i)
print('false_train_molecules_ids был схранен как false_train_molecules_ids.pickle')

with open("test_train/false_lost_set.pickle", 'wb') as o:
    dump(false_lost_set, o)
print('false_lost_set был схранен как false_lost_set_set.pickle')

with open("test_train/false_lost_molecule_ids.pickle", 'wb') as n:
    dump(false_lost_molecules_ids, n)
print('false_lost_molecules_ids был сохранен как false_lost_molecules_ids.pickle')

with open("test_train/intersection_dict.pickle", 'wb') as n:
    dump(intersection_dict, n)
print('intersection_dict был сохранен')

end = time()
print(end - start)

print('колличество тюплов в false_test_set = {}'.format(len(false_test_set)))
print('колличество тюплов в false_train_set = {}'.format(len(false_train_set)))
print('пересекалось молекул false_train_molecules_ids & false_test_molecules_ids: ', a)
print('пересекалось молекул false_train_molecules_ids & true_test_molecules_ids: ', b)
print('пересекалось молекул false_test_molecules_ids & true_train_molecules_ids: ', c)
print('количество тюплов потеряно: false_lost_set =', len(false_lost_set))

logger.info('колличество тюплов в false_test_set = {}'.format(len(false_test_set)))
logger.info('колличество тюплов в true_train_set = {}'.format(len(false_train_set)))

# последние результаты:
# колличество тюплов в false_test_set = 131636
# колличество тюплов в false_train_set = 2056008
# пересекалось молекул false_train_molecules_ids & false_test_molecules_ids:  0
# пересекалось молекул false_train_molecules_ids & true_test_molecules_ids:  0
# пересекалось молекул false_test_molecules_ids & true_train_molecules_ids:  0
# количество тюплов потеряно: false_lost_set = 1373036