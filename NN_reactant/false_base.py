# Этот код предназначен для разделения базы негативных примеров на тест и трейн (работает с реальной базой и с тюплами в которых молекул контейнеры.)
from pickle import dump, load
from time import time

start = time()

with open('uspto/true_base/true_test_molecules_signatures.pickle', 'rb') as f:
    true_test_molecules_signatures = load(f)

with open('uspto/true_base/true_train_molecules_signatures.pickle', 'rb') as q:
    true_train_molecules_signatures = load(q)

def divide_chunks(o, n):
    o = list(o)
    for z in range(0, len(o), n):
        yield o[z:z + n]

false_train_molecules_signatures = set()
false_test_molecules_signatures = set()
false_test_set = set()
false_train_set = set()
false_lost_molecules_signatures = set()
false_lost_set, y, u, p = 0, 0, 0, 0
a, c = 1, 1

for i in range(1, 918):
    print('номер файла', i)
    with open(f'uspto/new_false_ATB/{i}.pickle', 'rb') as r:
        pickle_file = load(r)
    for j, kortezh in enumerate(pickle_file):
        print('номер кортежа', j)
        r1, t, r2, _ = kortezh
        tmp = {bytes(r1), bytes(t), bytes(r2)}
        if (i > 0 and i % 50 == 0) or (i == 917 and j == len(pickle_file) - 1):
            if false_train_molecules_signatures & false_test_molecules_signatures:
                y += 1
                print('есть пересечение yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
            elif false_train_molecules_signatures & true_test_molecules_signatures:
                u += 1
                print('есть пересечение uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
            elif false_test_molecules_signatures & true_train_molecules_signatures:
                p += 1
                print('есть пересечение pppppppppppppppppppppppppppppppppppppppppppppp')
        if tmp & false_train_molecules_signatures or tmp & false_test_molecules_signatures or tmp & true_train_molecules_signatures or tmp & true_test_molecules_signatures:
            if tmp & false_train_molecules_signatures and (not tmp & false_test_molecules_signatures) and (not tmp & true_test_molecules_signatures):
                false_train_set.add(kortezh)
                false_train_molecules_signatures.update(tmp)
            elif tmp & false_test_molecules_signatures and (not tmp & false_train_molecules_signatures) and (not tmp & true_train_molecules_signatures):
                false_test_set.add(kortezh)
                false_test_molecules_signatures.update(tmp)
            elif tmp & true_test_molecules_signatures and (not tmp & true_train_molecules_signatures) and (not tmp & false_train_molecules_signatures):
                false_test_set.add(kortezh)
                false_test_molecules_signatures.update(tmp)
            elif tmp & true_train_molecules_signatures and (not tmp & true_test_molecules_signatures) and (not tmp & false_test_molecules_signatures):
                false_train_set.add(kortezh)
                false_train_molecules_signatures.update(tmp)
            else:
                false_lost_set += 1
                false_lost_molecules_signatures.update(tmp)
        else:
            false_test_set.add(kortezh)
            false_test_molecules_signatures.update(tmp)
        if len(false_test_set) >= 5000:
            for chunk in divide_chunks(false_test_set, 5000):
                if len(chunk) < 5000:
                    false_test_set = set(chunk)
                else:
                    print('dumping...', a)
                    with open(f'uspto/false_base/false_test_set/{a}.pickle', 'wb') as f:
                        dump(chunk, f)
                    print('dumping successful!')
                    false_test_set = set()
                    a += 1
        if len(false_train_set) >= 5000:
            for chunk in divide_chunks(false_train_set, 5000):
                if len(chunk) < 5000:
                    false_train_set = set(chunk)
                else:
                    print('dumping...', c)
                    with open(f'uspto/false_base/false_train_set/{c}.pickle', 'wb') as f:
                        dump(chunk, f)
                    print('dumping successful!')
                    false_train_set = set()
                    c += 1
        if i == 917 and j == len(pickle_file) - 1:
            print('dumping last time...')
            with open(f'uspto/false_base/false_test_set/{a}.pickle', 'wb') as f:
                dump(false_test_set, f)
            with open(f'uspto/false_base/false_train_set/{t}.pickle', 'wb') as g:
                dump(false_train_set, g)
            print('dumping successful!')

with open("uspto/false_base/false_train_molecules_signatures.pickle", 'wb') as m:
    dump(false_train_molecules_signatures, m)
print('false_train_molecules_signatures сохранился как false_train_molecules_signatures.pickle ')

with open("uspto/false_base/false_test_molecules_signatures.pickle", 'wb') as m:
    dump(false_test_molecules_signatures, m)
print('false_test_molecules_signatures сохранился как false_test_molecules_signatures.pickle ')

print('количесвто тюплов потеряно false_lost_set', false_lost_set)
print('пересекалось молекул false_train_molecules_signatures & false_test_molecules_signatures: ', y)
print('пересекалось молекул false_train_molecules_signatures & true_test_molecules_signatures: ', u)
print('пересекалось молекул false_test_molecules_signatures & true_train_molecules_signatures: ', p)

end = time()
print(end - start)
#Последние резултаты:
# количесвто тюплов потеряно false_lost_set 2007093
# пересекалось молекул false_train_molecules_signatures & false_test_molecules_signatures:  0
# пересекалось молекул false_train_molecules_signatures & true_test_molecules_signatures:  0
# пересекалось молекул false_test_molecules_signatures & true_train_molecules_signatures: 0
# 11532.240439414978