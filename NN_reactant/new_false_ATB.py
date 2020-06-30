from pickle import load, dump
from random import choice

with open('uspto/all_reactants.pickle', 'rb') as f:
    all_reactants = list(load(f))

def divide_chunks(o, n):
    o = list(o)
    for z in range(0, len(o), n):
        yield o[z:z + n]

x = 1
result = set()
for i in range(1, 459):
    with open(f'uspto/new_true_ATB/{i}.pickle', 'rb') as k:
        atb = load(k)
    for j in atb:
        a, t, b, c = j
        result.add((choice(all_reactants), t, b, c))
        result.add((a, t, choice(all_reactants), c))
    if len(result) >= 5000:
        for chunk in divide_chunks(result, 5000):
            if len(chunk) < 5000:
                result = set(chunk)
            else:
                print(f'dumping {i}')
                with open('uspto/new_false_ATB/{}.pickle'.format(x), 'wb') as b:
                    dump(chunk, b)
                print('dumping successful!')
                result = set()
                x += 1
    if i == 459:
        print('dumping last time...')
        with open('uspto/new_false_ATB/{}.pickle'.format(x), 'wb') as b:
            dump(result, b)
        print('dumping successful!')
