from CGRtools.files import *  # import all available readers and writers
import logging
from pickle import dump
from pony.orm import db_session
from CGRdb import load_schema
from db_values import user, password, port, host, database

logger = logging.getLogger("exampleApp")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("new_log.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.info("Program started")

db = load_schema('all_patents', user=user, password=password, host=host, database=database, port=port)


def divide_chunks(l, n):
    l = list(l)
    for i in range(0, len(l), n):
        yield l[i:i + n]


def prepare_1(db):
    reactions = db.Reaction.select()  # итератор реакций
    result = set()
    a = 1
    with db_session:
        c = reactions.count() // 1000
    for i in range(1, c + 1):
        print('Количество тюплов записанных в result на данный момент  {}'.format(len(result)))
        with db_session:
            reaction_structure = {reaction.structure: {'reaction_reactants': {mr.molecule.structure: mr.molecule.id
                                                                              for mr in reaction.molecules if
                                                                              not mr.is_product},
                                                       'reaction_products': {mr.molecule.structure: mr.molecule.id
                                                                             for mr in reaction.molecules if
                                                                             mr.is_product}} for reaction in
                                  reactions.page(i, pagesize=10)
                                  if len(set(reaction.structure.reactants)) == 2}
        logger.info("Count of pages were reading: {}".format(i))
        for reaction, reaction_members in reaction_structure.items():
            reactants_list = []
            for reactant, number in reaction_members['reaction_reactants'].items():
                reactant._meta = {'id': number}
                reactants_list.append(reactant)
            for product, number in reaction_members['reaction_products'].items():
                product._meta = {'id': number}
            #проверка на нахождения тюпла в списке уникальных. И только потом добавлять в резалт
                result.add((reactants_list[0], product, reactants_list[1], True))
                result.add((reactants_list[1], product, reactants_list[0], True))
        logger.info('Количество тюплов записанных в result на данный момент {}'.format(len(result)))
        if len(result) >= 1000:
            for chunk in divide_chunks(result, 1000):
                if len(chunk) < 1000:
                    result = set(chunk)
                else:
                    print('dumping...')
                    with open('RESULT/{}.pickle'.format(a), 'wb') as f:
                        dump(chunk, f)
                    print('dumping successful!')
                    logger.info('отгрузился файл под номером {}'.format(a))
                    result = set()
                    a += 1
        if i == c:
            print('dumping last time...')
            with open('RESULT/{}.pickle'.format(a), 'wb') as f:
                dump(result, f)
            print('dumping successful!')
            logger.info('отгрузился последний файл под номером {}'.format(a))


prepare_1(db)
logger.info("Done!")
