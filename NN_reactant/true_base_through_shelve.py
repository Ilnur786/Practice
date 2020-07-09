#Этот код предназначен для того чтобы собрать базу "позитивных" примеров (тюплы) через модуль shelve
from time import time
import shelve
import pickle

# true
start = time()


def divide_chunks(o, n):
    o = list(o)
    for z in range(0, len(o), n):
        yield o[z:z + n]

true_test_set = set()
true_test_molecules_signatures = set()
true_train_molecules_signatures = set()
true_train_set = set()
true_lost_molecules_signatures = set()
counter, true_lost_set = 0, 0
a, q = 1, 1

for v in range(1, 460):
    print('номер файла', v)
    with open(f'uspto/new_true_ATB/{v}.pickle', 'rb') as z:
        pickle_file = pickle.load(z)
    for i, kortezh in enumerate(pickle_file):
        print('номер кортежа', i)
        r1, t, r2, _ = kortezh
        tmp = {bytes(r1), bytes(t), bytes(r2)}
        if (v > 0 and v % 50 == 0) or (v == 459 and i == 483):
            if true_train_molecules_signatures & true_test_molecules_signatures:
                counter += 1
                print('есть пересечение', len(true_train_molecules_signatures & true_test_molecules_signatures))
        if tmp & true_train_molecules_signatures or tmp & true_test_molecules_signatures:
            if tmp & true_train_molecules_signatures and (not tmp & true_test_molecules_signatures):
                true_train_set.add(kortezh)
                true_train_molecules_signatures.update(tmp)
            elif tmp & true_test_molecules_signatures and (not tmp & true_train_molecules_signatures):
                true_test_set.add(kortezh)
                true_test_molecules_signatures.update(tmp)
            else:
                print('---')
                true_lost_set += 1
                true_lost_molecules_signatures.update(tmp)
        else:
            if not true_test_set or len(true_train_molecules_signatures) / len(true_test_molecules_signatures) >= 3:
                print('!!!')
                true_test_set.add(kortezh)
                true_test_molecules_signatures.update(tmp)
            else:
                print('+++')
                true_train_set.add(kortezh)
                true_train_molecules_signatures.update(tmp)
        if len(true_test_set) >= 5000:
            for chunk in divide_chunks(true_test_set, 5000):
                if len(chunk) < 5000:
                    true_test_set = set(chunk)
                else:
                    print('shelving...', a)
                    with shelve.open('uspto/true_base/through_shelve/true_test_set.shelve') as true_test:
                        true_test[str(a)] = chunk
                    print('shelving successful!')
                    true_test_set = set()
                    a += 1
        if len(true_train_set) >= 5000:
            for chunk in divide_chunks(true_train_set, 5000):
                if len(chunk) < 5000:
                    true_train_set = set(chunk)
                else:
                    print('shelving...', q)
                    with shelve.open('uspto/true_base/through_shelve/true_train_set.shelve') as true_train:
                        true_train[str(q)] = chunk
                    print('shelving successful!')
                    true_train_set = set()
                    q += 1
        if v == 459 and i == 483:
            print('shelving last time...')
            with shelve.open('uspto/true_base/through_shelve/true_test_set.shelve') as true_test:
                true_test[str(a)] = true_test_set
            with shelve.open('uspto/true_base/through_shelve/true_train_set.shelve') as true_train:
                true_train[str(q)] = true_train_set
            print('shelving successful!')
print('в true_train_set добавились все кортежи из new_true_ATB, молекулы которых не входят true_test_molecules_signatures')

with open("uspto/true_base/through_shelve/true_lost_molecules_signatures.pickle", 'wb') as n:
    pickle.dump(true_lost_molecules_signatures, n)
print('true_lost_molecules_signatures был сохранен как true_lost_molecules_signatures.pickle')

with open("uspto/true_base/through_shelve/true_train_molecules_signatures.pickle", 'wb') as i:
    pickle.dump(true_train_molecules_signatures, i)
print('true_train_molecules_signatures был схранен как true_train_molecules_signatures.pickle')

with open("uspto/true_base/through_shelve/true_test_molecules_signatures.pickle", 'wb') as j:
    pickle.dump(true_test_molecules_signatures, j)
print('true_test_molecules_signatures был схранен как true_test_molecules_signatures.pickle')

print('количество тюплов потеряно: true_lost_set =', true_lost_set)
print('пересекалось кортежей = ', counter)
end = time()
print(end - start)
# последние результаты:
# в true_train_set добавились все кортежи из new_true_ATB, молекулы которых не входят true_test_molecules_signatures
# true_lost_molecules_signatures был сохранен как true_lost_molecules_signatures.pickle
# true_train_molecules_signatures был схранен как true_train_molecules_signatures.pickle
# true_test_molecules_signatures был схранен как true_test_molecules_signatures.pickle
# количество тюплов потеряно: true_lost_set = 462227
# пересекалось кортежей =  0
# 3771.6709480285645