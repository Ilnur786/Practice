from pickle import dump, load
import random
#
# result = set()
# # c помощью этого кода я вытащил из всех трушек только их айдишки:
# for i in range(1, 1790):
#     print('сейчас будет обрабатываться pickle под номером {}'.format(i))
#     with open('RESULT/{}.pickle'.format(i), 'rb') as f:
#         pickle_file = load(f)
#     for kortezh in pickle_file:
#         result.add(tuple([x.meta['id'] for x in kortezh[:-1]]))
#
# print('все pickles обработались')
# with open("all_tuples_id's.pickle", 'wb') as f:
#     dump(result, f)
# print("файл с наборами id's отгрузился. Done! len(result) = {}".format(len(result)))

# получилось 1780340 кортежей, когда резалт был set
# получилось 1788067 кортежей, когда резалт был листом
#
##
#
#с помощью этого кода я сохранил в файл фолсы ( с изменными ректантами)
result = set()
reactants = set()

with open("test_train/true_test_set.pickle", 'rb') as f:
    pickle_file = load(f)

for kortezh in pickle_file:
    reactants.add(kortezh[0])
    reactants.add(kortezh[2])

reactants = list(reactants)
counter = 0

for kortezh in pickle_file:
    counter += 1
    print('начльный кортеж:', kortezh)
    a = tuple([random.choice(reactants), kortezh[1], kortezh[2]])
    while True:
        if a not in pickle_file:
            print('заменен 1 реактант', a)
            result.add(a)
            break
        else:
            a = tuple([random.choice(reactants), kortezh[1], kortezh[2]])
            print('еще раз заменили 1 ректант', a)
    b = tuple([kortezh[0], kortezh[1], random.choice(reactants)])
    while True:
        if b not in pickle_file:
            print('заменен 2 реактант', b)
            result.add(b)
            break
        else:
            b = tuple([kortezh[0], kortezh[1], random.choice(reactants)])
            print('еще раз заменили 1 ректант', a)
    print('Кортежей изменено: ', counter)

with open('false_base/false_test_set_part2.pickle', 'wb') as f:
    dump(result, f)
print('тюплы закончились!')
##

# with open('test_train/true_test_set.pickle', 'rb') as f:
#     true_test_set = load(f)
#
# print('len(true_test_set)',len(true_test_set))
# print(true_test_set)
#
# with open('test_train/true_train_set.pickle', 'rb') as c:
#     true_train_set = load(c)
#
# print('len(true_train_set)',len(true_train_set))
# print(true_train_set)
