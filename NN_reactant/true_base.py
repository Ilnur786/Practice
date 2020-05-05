from pickle import dump, load
import logging

#true
logger = logging.getLogger("exampleApp")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("test_train/true_train_test.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.info("Program started")

with open("test_train/true_base_ids.pickle", 'rb') as f:
    pickle_file = load(f)
print('загрузился файл true_base_ids.pickle ')

pickle_file = list(pickle_file)
true_test_set = set()
true_test_set.update(pickle_file[:100])
print('в true_test_set добавлены 1000 тюплов')

true_test_molecules_ids = set()
true_train_molecules_ids = set()
for kortezh in true_test_set:
    true_test_molecules_ids.update(kortezh)
print('в true_test_molecules_ids хранятся молекулы из тюплов true_test_set.pickle')


true_train_set = set()
true_lost_set = set()
true_lost_molecules_ids = set()
counter = 0

for i, kortezh in enumerate(pickle_file[100:]):
    if i > 0 and i % 1000 == 0:
        if true_train_molecules_ids & true_test_molecules_ids:
            counter += 1
            print('есть пересечение')
            logger.info('есть пересечение')
    if set(kortezh) & true_train_molecules_ids or set(kortezh) & true_test_molecules_ids:
        if set(kortezh) & true_train_molecules_ids and (not set(kortezh) & true_test_molecules_ids):
            true_train_set.add(kortezh)
            true_train_molecules_ids.update(kortezh)
        elif set(kortezh) & true_test_molecules_ids and (not set(kortezh) & true_train_molecules_ids):
            true_test_set.add(kortezh)
            true_test_molecules_ids.update(kortezh)
        else:
            true_lost_set.add(kortezh)
            true_lost_molecules_ids.update(kortezh)
    else:
        if len(true_train_set) / len(true_test_set) >= 5:
            print('!')
            true_test_set.add(kortezh)
            true_test_molecules_ids.update(kortezh)
        else:
            print('-')
            true_train_set.add(kortezh)
            true_train_molecules_ids.update(kortezh)
    print('номер кортежа', i)
print('в true_train_set добавились все кортежи из true_base_ids.pickle, молекулы которых не входят true_test_molecules_ids')
logger.info('пересекалось кортежей: {}'.format(counter))

with open("test_train/true_test_set.pickle", 'wb') as c:
    dump(true_test_set, c)
print('true_test_set сохранился как true_test_set.pickle ')

with open("test_train/true_train_set.pickle", 'wb') as t:
    dump(true_train_set, t)
print('true_train_set был схранен как true_train_set.pickle')

with open("test_train/true_lost_set.pickle", 'wb') as o:
    dump(true_lost_set, o)
print('true_lost_set был схранен как true_lost_set_set.pickle')

with open("test_train/true_lost_molecule_ids.pickle", 'wb') as n:
    dump(true_lost_molecules_ids, n)
print('true_lost_molecules_ids был сохранен как true_lost_molecules_ids.pickle')

with open("test_train/true_train_molecules_ids.pickle", 'wb') as i:
    dump(true_train_molecules_ids, i)
print('true_train_molecules_ids был схранен как true_train_molecules_ids.pickle')

with open("test_train/true_test_molecules_ids.pickle", 'wb') as j:
    dump(true_test_molecules_ids, j)
print('true_test_molecules_ids был схранен как true_test_molecules_ids.pickle')



print('колличество тюплов в true_test_set = {}'.format(len(true_test_set)))
print('колличество тюплов в true_train_set = {}'.format(len(true_train_set)))
print('пересекалось кортежей = ', counter)
print('количество тюплов потеряно: true_lost_set =', len(true_lost_set))

logger.info('колличество тюплов в true_test_set = {}'.format(len(true_test_set)))
logger.info('колличество тюплов в true_train_set = {}'.format(len(true_train_set)))

# запуск когда в цикле pickle-file:
# колличество тюплов в true_test_set = 217998
# колличество тюплов в true_train_set = 1237104
# пересекалось кортежей =  0
# количество тюплов потеряно: true_lost_set = 325238

# запуск когда в цикле a, а в true_test_set = 10:
# колличество тюплов в true_test_set = 213340
# колличество тюплов в true_train_set = 1231166
# пересекалось кортежей =  0
# количество тюплов потеряно: true_lost_set = 335834

#последний запуск:
# колличество тюплов в true_test_set = 217888
# колличество тюплов в true_train_set = 1237008
# пересекалось кортежей =  0
# количество тюплов потеряно: true_lost_set = 325444






