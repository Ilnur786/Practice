from pickle import dump
from pony.orm import db_session
from CGRdb import load_schema
import logging
import time
from multiprocessing import Process, Queue, current_process
from db_values import user, password, port, host, database

start = time.time()

logger = logging.getLogger("exampleApp")
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler("MULTIPROCESSING_POSITIVE_EXAMPLES.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

logger.info("Program started")

db = load_schema('all_patents', user=user, password=password, host=host, database=database, port=port)

reactions = db.Reaction.select()  # итератор реакций


def divide_chunks(l, n):
    l = list(l)
    for i in range(0, len(l), n):
        yield l[i:i + n]


input = Queue()
output = Queue()
result = set()
with db_session:
    c = reactions.count() // 100
a = 1
for i in range(c):
    input.put(i)

number_of_processes = 12

for i in range(number_of_processes):
    input.put('stop')


def worker(input, output):
    for o in iter(input.get, 'stop'):
        print('Количество тюплов записанных в result на данный момент {}'.format(len(result)))
        with db_session:
            reaction_structure = {reaction.structure: {'reaction_reactants': {mr.molecule.structure: mr.molecule.id
                                                                              for mr in reaction.molecules if
                                                                              not mr.is_product},
                                                       'reaction_products': {mr.molecule.structure: mr.molecule.id
                                                                             for mr in reaction.molecules if
                                                                             mr.is_product}} for reaction in
                                  reactions.page(o, pagesize=100)
                                  if len(set(reaction.structure.reactants)) == 2}
        logger.info("Count of pages were reading: {}".format(o))
        for reaction, reaction_members in reaction_structure.items():
            reactants_list = []
            for reactant, number in reaction_members['reaction_reactants'].items():
                reactant._meta = {'id': number}
                reactants_list.append(reactant)
            for product, number in reaction_members['reaction_products'].items():
                product._meta = {'id': number}
                result.add((reactants_list[0], product, reactants_list[1], True))
                result.add((reactants_list[1], product, reactants_list[0], True))
        output.put(result)




for i in range(number_of_processes):
    Process(target=worker, args=(input, output)).start()


global_result = set()


for j in range(c):
    b = output.get()
    flag = True
    while flag:
        if b:
            flag = False
            for i in b:
                global_result.add(i)

    if len(global_result) >= 1000:
        for chunk in divide_chunks(global_result, 1000):
            if len(chunk) < 1000:
                global_result = set(chunk)
            else:
                print('dumping...')
                with open('MULTIPROCESSING_POSITIVE_EXAMPLES/{}.pickle'.format(a), 'wb') as f:
                    dump(chunk, f)
                print('dumping successful!')
                logger.info('отгрузился файл под номером {}'.format(a))
                result = set()
                a += 1
    if j == c:
        print('dumping last time...')
        with open('MULTIPROCESSING_POSITIVE_EXAMPLES/{}.pickle'.format(a), 'wb') as f:
            dump(result, f)
        print('dumping successful!')
        logger.info('отгрузился последний файл под номером {}'.format(a))
    logger.info('Количество тюплов в result после очередного пейджа {}'.format(len(global_result)))

end = time.time()

logger.info("Done!")
logger.info('time of executing: {}'.format(end - start))
