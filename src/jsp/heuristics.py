
import math
import random

from .decoder import decode
from .neighborhood import get_random_neighbor, neighbors, shake, random_swap_move, swap_neighborhood

# pyright: reportFunctionMemberAccess=false


def local_search(instance, sequence, firstimprov=False, budget=None, start=None, neighborhood=swap_neighborhood):
    best_score = decode(instance,sequence)
    best_sequence = list(sequence)

    stalled = False
    while not stalled:
        if budget is not None and decode.calls - start >= budget:
            break
        stalled = True
        for neighbor in neighborhood(instance,sequence):

            value = decode(instance, neighbor)

            if budget is not None and decode.calls - start >= budget:
                stalled = True
                break

            if value < best_score:
                best_score = value
                best_sequence = neighbor
                stalled = False
                if firstimprov:
                    break

        sequence = best_sequence

    return best_score, best_sequence

#LOCAL SEARCH with BUDGET
def local_search_budget(instance, sequence, budget=100000, neighborhood=swap_neighborhood):
    start = decode.calls
    best_score, best_seq = local_search(instance, sequence, budget=budget, start=start, neighborhood=neighborhood)
    while decode.calls - start < budget:
        s = random.sample(sequence, len(sequence))
        value, seq = local_search(instance, s, budget=budget, start=start, neighborhood=neighborhood)
        if value < best_score:
            best_score, best_seq = value, seq
    return best_score, best_seq

# SIMULATED ANNEALING
def simulated_annealing(instance, sequence, budget = 100000, move=random_swap_move,
                        T0=20, Tk=0.001):
    start = decode.calls
    best_sequence = list(sequence)
    best_score = decode(instance, sequence)
    T = T0
    alpha = (Tk/T0)**(1/budget)

    current = sequence
    current_value = decode(instance,sequence)
    while decode.calls - start < budget:

        neighbor = move(instance,current)

        T *= alpha
        value = decode(instance,neighbor)

        if value < current_value:
            current = neighbor
            current_value = value

            if value < best_score:
                best_sequence = neighbor
                best_score = value

        else:
            delta = abs(current_value-value)

            p = math.e ** (- delta / T )
            if random.random() < p:
                current = neighbor
                current_value = value

    return best_score, best_sequence

# VARIABLE NEIGHBORHOOD SEARCH


def vns(instance, sequence, kmax=10, budget=1000):
    start = decode.calls
    current = sequence
    best_score = decode(instance,current)
    best_seq = current

    while decode.calls - start < budget:
        k = 1
        while k < kmax and decode.calls - start < budget:
            neigbor = shake(current,k)
            value, seq_ret = local_search(instance, neigbor, firstimprov=True,
                                          budget=budget, start=start)
            if value < best_score:
                best_score = value
                best_seq = seq_ret
                current = seq_ret
                k = 1 
            else:
                k+=1

    return best_score, best_seq



def crossover(parent1, parent2):
    mask = [random.randrange(2) for i in range(len(parent1))]

    p1 = list(parent1)
    p2 = list(parent2)

    c1 = []
    for idx, bit in enumerate(mask):
        if bit:
            c1.append(p1[0])
            p2.remove(p1[0])
            p1.pop(0)
        else:
            c1.append(p2[0])
            p1.remove(p2[0])
            p2.pop(0)

    return c1
            

def select_parent(seq):
    return min(seq, key=(lambda x: x[1]))

def mutation(el, p, inplace=True):

    if random.random() < p:
        return get_random_neighbor(el,inplace=inplace)
    return el


def genetic_algorithm(instance, sequence, budget=100000,population_size=50, p = 0.3, elitism = 0.02, tournament_pct=0.3):

    starting_population = [random.sample(sequence, len(sequence)) for i in range(population_size)]


    start = decode.calls

    best_seen = (starting_population[0], decode(instance,starting_population[0]))

    TOUR_SIZE = int(tournament_pct * len(starting_population))
    ELITISM = int(population_size * elitism)

    current_scores = [(seq, decode(instance,seq)) for seq in starting_population]
    current_scores.sort(key=(lambda x: x[1]))
    generation = 0
    while decode.calls - start < budget:
        generation += 1


        next_generation = list(current_scores[:ELITISM])

        for i in range(ELITISM, len(current_scores), 2):
            p1 = select_parent(random.sample(current_scores,TOUR_SIZE))
            p2 = select_parent(random.sample(current_scores,TOUR_SIZE))

            c1 = crossover(p1[0],p2[0])
            c2 = crossover(p1[0],p2[0])

            c1 = mutation(c1,p=p,inplace=True)
            c2 = mutation(c2,p=p,inplace=True)


            next_generation.append((c1,decode(instance, c1)))
            next_generation.append((c2,decode(instance, c2)))

            

        next_generation.sort(key=(lambda x: x[1]))
        
        current_scores = next_generation
        if(current_scores[0][1] < best_seen[1]):
            best_seen = current_scores[0]

    return best_seen[1], best_seen[0]
