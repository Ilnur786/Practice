from CGRtools.files import *
from pickle import load, dump

with open('uspto/double_reactants_rules.pickle', 'rb') as f:
    double_reactants_rules = load(f)

with open('/home/ilnur/Practice/NN_reactant/uspto/reaction_containers.pickle', 'rb') as f:
    reaction_containers = load(f)

with open('uspto/all_rules_ids.pickle', 'rb') as f:
    ids = load(f)

result = []
with RDFRead('uspto/USPTO.rdf', indexable=True) as f:
    for i, reactions in enumerate(ids):
        products = []
        for reaction_num in reactions:
            for k, rules_reactants_atoms in enumerate([x for x in reaction_containers[i].reactants[0].connected_components]):
                for j, rdf_reactants_atoms in enumerate([y.atoms_numbers for y in f[reaction_num].reactants]):
                    if set(rules_reactants_atoms).issubset(set(rdf_reactants_atoms)) and k == 0:
                        A = f[reaction_num].reactants[j]
                    elif set(rules_reactants_atoms).issubset(set(rdf_reactants_atoms)) and k == 1:
                        B = f[reaction_num].reactants[j]
            for rules_products_atoms in [x for x in reaction_containers[i].products[0].connected_components]:
                for o, rdf_products_atoms in enumerate([y.atoms_numbers for y in f[reaction_num].products]):
                    if set(rules_products_atoms).issubset(rdf_products_atoms):
                        products.append(f[reaction_num].products[o])
            for p in products:
                result.append((A, p, B, True))
                result.append((B, p, A, True))

    c = reaction_containers[0].reactants[0].split()
    for i in c:
        for j in [x for x in f[0].reactants]:
            print(i <= j)
with open('uspto/new_true_ATB.pickle', 'wb') as f:
    dump(result, f)
