import os
from CGRtools.files import * # import all available readers and writers
from pickle import dump
from pony.orm import db_session
from CGRdb import load_schema
from db_values import user, password, port, host, database


#os.environ['PATH']+=':/home/ilnur/Practice'


with RDFread('/home/ilnur/Practice/sn2.rdf') as f:
    first = next(f)  # get first reaction using generator
    data = f.read()

def prepare(data, name):
    result = []
    a = 1
    for reaction in data:
        if len(reaction.reactants) != 2:
            continue
        #for i, reactant in enumerate(reaction.reactants):
        for product in reaction.products:
            reactant1, reactant2 = reaction.reactants[0], reaction.reactants[1]
            result.append((reactant1, product, reactant2, True))
            result.append((reactant2, product, reactant1, True))
            if len(result) == 1000:
                with open(name + '_' + str(a), 'wb') as f:
                    dump(result, f)
                result = []
                a += 1
    if len(result) > 0:
        with open(name + '_' + str(a), 'wb') as f:
            dump(result, f)
    del result

prepare(data, '/home/ilnur/Practice/name')


db = load_schema('all_patents', user=user, password=password, host=host, database=database, port=port)


def prepare_1(db, name='file'):
    reactions = db.Reaction.select() # итератор реакций
    result = []
    a = 1
    with db_session:
        c = reactions.count() // 1000
    for i in range(1, 11):
        with db_session:
            for reaction in reactions.page(i, pagesize=100):
                reactants_structure = {reaction.structure : {mr.molecule.structure: mr.molecule.id
                                                             for mr in reaction.molecules if not mr.is_product}
                                                            for reaction in reactions.page(i, pagesize=100)}
                reaction_structure = {'reaction_structure' : {reaction.structure.reactants : {mr.molecule.structure: mr.molecule.id
                                                             for mr in reaction.molecules if not mr.is_product}, reaction.structure.products : {mr.molecule.structure: mr.molecule.id
                                                             for mr in reaction.molecules if mr.is_product}
                                                             for product in reaction.structure.products } for reaction in reactions.page(i, pagesize=100)}

                # products_structure = {mr.molecule.structure: mr.molecule.id for mr in reaction.molecules if mr.is_product}

                if len(reaction.sctructure.reactants) != 2:
                    continue
                with db_session:
                    reactants_structure = {mr.molecule.structure : mr.molecule.id for mr in reaction.molecules if not mr.is_product}
                    products_structure = {mr.molecule.structure : mr.molecule.id for mr in reaction.molecules if mr.is_product}
                for reactant, value in reactants_structure.items():
                    reactant.meta = {'id' : value}
                for product, value in products_structure:
                    product.meta = {'id' : value}
                result.append((reactants_structure[0], product, reactants_structure[1], True))
                result.append((reactants_structure[1], product, reactants_structure[0], True))
                if len(result) == 1000:
                    print('колличесво тысяч на очередном шаге: {}'.format(a))
                    # with open('{}_{}'.format(name, a), 'wb') as f:
                    #     dump(result, f)
                    result = []
                    a += 1
                if len(result) > 0:
                    print('всего тысяч после последнего шага: {}'.format(a))
                    # with open('{}_{}'.format(name, a), 'wb') as f:
                    #     dump(result, f)
                del result


