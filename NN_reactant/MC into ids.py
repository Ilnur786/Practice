# Этот код предназначен для замены молекул контейнеров в кортежах в их индексы из реакций в рдф файлах
from pickle import load, dump

true_base_ids = set()
for i in range(1, 460):
    with open(f'uspto/{i}.pickle', 'rb') as f:
        pickle_file = load(f)
    for kortezh in pickle_file:
        r1, t, r2, _ = kortezh
        true_base_ids.add(((r1.meta['id'], r1.meta['index']), (t.meta['id'], t.meta['index']), (r2.meta['id'], r2.meta['index']), True))
