from CGRtools.files import *
from pickle import load, dump

with open('uspto/reaction_containers.pickle', 'rb') as g:
    reaction_containers = load(g)

with open('uspto/all_rules_ids.pickle', 'rb') as h:
    ids = load(h)


def divide_chunks(o, n):
    o = list(o)
    for j in range(0, len(o), n):
        yield o[z:z + n]


a = 1
c = 1
result = set()
A, B = None, None
all_targets = set()

with RDFRead('uspto/USPTO.rdf', indexable=True) as f:
    for i, reactions in enumerate(ids):
        for reaction_num in reactions:
            products = []
            for k, rules_reactant in enumerate(reaction_containers[i].reactants[0].split()):
                for z, rdf_reactant in enumerate([x for x in f[reaction_num - 1].reactants]):
                    if rules_reactant <= rdf_reactant and k == 0:
                        A = rdf_reactant
                        A.meta['id'] = reaction_num - 1
                        A.meta['index'] = z
                    elif rules_reactant <= rdf_reactant and k == 1:
                        B = rdf_reactant
                        B.meta['id'] = reaction_num - 1
                        B.meta['index'] = z
                    if A and B:
                        break
            for rules_product in reaction_containers[i].products[0].split():
                for m, rdf_product in enumerate(f[reaction_num - 1].products[0].split()):
                    if rules_product <= rdf_product:
                        rdf_product.meta['id'] = reaction_num - 1
                        rdf_product.meta['index'] = m
                        products.append(rdf_product)
                        all_targets.add(rdf_product)
            if A and B and products:
                for p in products:
                    result.add((A, p, B, True))
                    result.add((B, p, A, True))
                A = None
                B = None
        if len(result) >= 5000:
            for chunk in divide_chunks(result, 5000):
                if len(chunk) < 5000:
                    result = set(chunk)
                else:
                    print(f'dumping {a}')
                    print(f'dumping {i}')
                    with open('uspto/new_true_ATB/{}.pickle'.format(a), 'wb') as b:
                        dump(chunk, b)
                    print('dumping successful!')
                    result = set()
                    a += 1
        if i == len(ids) - 1:
            print('dumping last time...')
            with open('uspto/new_true_ATB/{}.pickle'.format(a), 'wb') as b:
                dump(result, b)
            print('dumping successful!')
        if len(all_targets) >= 5000:
            for chunk in divide_chunks(all_targets, 5000):
                if len(chunk) < 5000:
                    result = set(chunk)
                else:
                    print(f'dumping {c}')
                    with open('uspto/all_targets/{}.pickle'.format(c), 'wb') as b:
                        dump(chunk, b)
                    print('dumping successful!')
                    all_targets = set()
                    c += 1
        if i == len(ids) - 1:
            print('dumping last time...')
            with open('uspto/all_targets/{}.pickle'.format(c), 'wb') as b:
                dump(all_targets, b)
            print('dumping successful!')
