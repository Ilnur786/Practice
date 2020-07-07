#Этот код предназначен для деления "позитивных" примеров на тест и трейн (пиклами)
from pickle import dump, load
from time import time

#true
start = time()
def divide_chunks(o, n):
    o = list(o)
    for z in range(0, len(o), n):
        yield o[z:z + n]
        
# with open("test_train/true_base_ids.pickle", 'rb') as f:
#     pickle_file = load(f)
# print('загрузился файл true_base_ids.pickle ')
# 
# pickle_file = list(pickle_file)
true_test_set = set()
# true_test_set.update(pickle_file[:100])
# print('в true_test_set добавлены 5000 тюплов')

true_test_molecules_signatures = set()
true_train_molecules_signatures = set()
# for kortezh in true_test_set:
#     true_test_molecules_signatures.update(kortezh)
# print('в true_test_molecules_signatures хранятся молекулы из тюплов true_test_set.pickle')


true_train_set = set()
true_lost_set = 0
true_lost_molecules_signatures = set()
counter = 0
a = 1
q = 1
for v in range(1, 460):
    print('номер файла', v)
    with open(f'uspto/new_true_ATB/{v}.pickle', 'rb') as z:
        pickle_file = load(z)
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
                    print('dumping...', a)
                    with open(f'uspto/true_base/true_test_set/{a}.pickle', 'wb') as f:
                        dump(chunk, f)
                    print('dumping successful!')
                    true_test_set = set()
                    a += 1
        if len(true_train_set) >= 5000:
            for chunk in divide_chunks(true_train_set, 5000):
                if len(chunk) < 5000:
                    true_train_set = set(chunk)
                else:
                    print('dumping...', q)
                    with open(f'uspto/true_base/true_train_set/{q}.pickle', 'wb') as f:
                        dump(chunk, f)
                    print('dumping successful!')
                    true_train_set = set()
                    q += 1
        if v == 459 and i == 483:
            print('dumping last time...')
            with open(f'uspto/true_base/true_test_set/{a}.pickle', 'wb') as f:
                dump(true_test_set, f)
            with open(f'uspto/true_base/true_train_set/{q}.pickle', 'wb') as p:
                dump(true_train_set, p)
            print('dumping successful!')

print('в true_train_set добавились все кортежи из new_true_ATB, молекулы которых не входят true_test_molecules_signatures')

with open("uspto/true_base/true_lost_molecules_signatures.pickle", 'wb') as n:
    dump(true_lost_molecules_signatures, n)
print('true_lost_molecules_signatures был сохранен как true_lost_molecules_signatures.pickle')

with open("uspto/true_base/true_train_molecules_signatures.pickle", 'wb') as i:
    dump(true_train_molecules_signatures, i)
print('true_train_molecules_signatures был схранен как true_train_molecules_signatures.pickle')

with open("uspto/true_base/true_test_molecules_signatures.pickle", 'wb') as j:
    dump(true_test_molecules_signatures, j)
print('true_test_molecules_signatures был схранен как true_test_molecules_signatures.pickle')

print('количество тюплов потеряно: true_lost_set =', true_lost_set)
print('пересекалось кортежей = ', counter)
end = time()
print(end - start)
#последний запуск:
# в true_train_set добавились все кортежи из new_true_ATB, молекулы которых не входят true_test_molecules_signatures
# true_lost_molecules_signatures был сохранен как true_lost_molecules_signatures.pickle
# true_train_molecules_signatures был схранен как true_train_molecules_signatures.pickle
# true_test_molecules_signatures был схранен как true_test_molecules_signatures.pickle
# количество тюплов потеряно: true_lost_set = 462225
# пересекалось кортежей =  0
# 3788.1044702529907






