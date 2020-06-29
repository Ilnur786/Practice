from pickle import load
from CGRtools.files import SDFWrite

all_signatures = set()
with SDFWrite('uspto/all_targets.sdf') as sdf:
    for i in range(1, 233):
        with open(f'uspto/all_targets/{i}.pickle', 'rb') as f:
            all_targets = load(f)
        for target in all_targets:
            if bytes(target) not in all_signatures:
                all_signatures.add(bytes(target))
                sdf.write(target)
        print(i)
