from CGRtools.files import *
from pickle import load, dump

with open('uspto/reaction_containers.pickle', 'rb') as g:
    reaction_containers = load(g)

with open('uspto/all_rules_ids.pickle', 'rb') as h:
    ids = load(h)


def divide_chunks(o, n):
    o = list(o)
    for z in range(0, len(o), n):
        yield o[z:z + n]


a = 1
result = set()
with RDFRead('uspto/USPTO.rdf', indexable=True) as f:
    for i, reactions in enumerate(ids):
        products = []
        for reaction_num in reactions:
            for k, rules_reactant in enumerate(reaction_containers[i].reactants[0].split()):
                for rdf_reactant in [x for x in f[reaction_num - 1].reactants]:
                    if rules_reactant <= rdf_reactant and k == 0:
                        A = rdf_reactant
                        A.meta['id'] = reaction_num - 1
                    elif rules_reactant <= rdf_reactant and k == 1:
                        B = rdf_reactant
                        B.meta['id'] = reaction_num - 1
            for rules_product in reaction_containers[i].products[0].split():
                for rdf_product in [x for x in f[reaction_num - 1].products]:
                    if rules_product <= rdf_product:
                        rdf_product.meta['id'] = reaction_num - 1
                        products.append(rdf_product)
            for p in products:
                result.add((A, p, B, True))
                result.add((B, p, A, True))
            break
        if len(result) >= 5000:
            for chunk in divide_chunks(result, 5000):
                if len(chunk) < 5000:
                    result = set(chunk)
                else:
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