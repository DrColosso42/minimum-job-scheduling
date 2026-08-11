from more_itertools import distinct_permutations

from .decoder import decode


def brute_force(instance):
    possible = [i for i, inst  in enumerate(instance) for j in range(len(inst))]
    best_makespan = float('inf')
    best_sequence = []
    for perm in distinct_permutations(possible):
        makespan = decode(instance, perm)
        if makespan < best_makespan:
            best_makespan = makespan
            best_sequence = list(perm)

    return best_makespan, best_sequence
