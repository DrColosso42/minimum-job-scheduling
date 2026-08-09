import random, math

from more_itertools import distinct_permutations

# Instance functions


def load(filepath):
    with open(filepath, "r") as f:
        n, m = (int(x) for x in f.readline().split(" "))
        instance = [[int(x) for x in f.readline().split(" ")] for i in range(n)]
        instance = [list(zip(job[::2],job[1::2])) for job in instance] 

    return instance


def lower_bound(instance):

    longest_per_job = max(
        sum((dur for _, dur in job)) for job in instance)

    m = len(set(m_id for job in instance for (m_id,_) in job))
    machine_lengths = [0] * m

    for job in instance:
        for (m_id, dur) in job:
            machine_lengths[m_id] += dur

    longest_per_machine = max(machine_lengths)

    return max(longest_per_job, longest_per_machine)

# Decoders 


# pyright: reportFunctionMemberAccess=false
def decode(instance, sequence) -> int:
    decode.calls += 1
    n = len(instance)
    m = len({machine for job in instance for machine, _ in job})
    if len(sequence) != sum(len(job) for job in instance):
        print("Invalid sequence")
        return -1


    job_ready = [0 for i in range(n)]
    machine_ready = [0 for i in range(m)]
    job_instr_counters = [0 for i in range(n)]

    for i in sequence:
        m_id, duration = instance[i][job_instr_counters[i]]
        start_ts = max(job_ready[i], machine_ready[m_id])

        job_ready[i ] = start_ts + duration
        machine_ready[m_id] = start_ts + duration

        job_instr_counters[i] += 1

    return max(job_ready)

decode.calls = 0



def reconstruct_path(ancestors, last_finishing_job):
    path = [last_finishing_job]
    while True:
        i, j = path[-1]
        if ancestors[i][j] == None:
            break
        path.append(ancestors[i][j])

    path.reverse()

    return path

def decode_full(instance, sequence):
    n = len(instance)
    m = len({machine for job in instance for machine, _ in job})
    if len(sequence) != sum(len(job) for job in instance):
        print("Invalid sequence")
        return {
            'success': False,
            'makespan': -1,
            'critical_path': [],
            'start': {},
            'end': {},
            'seq_pos': {} 
        }

    total_makespan = 0
    last_finishing_job = instance[0][0]
    job_ready = [0 for i in range(n)]
    machine_ready = [0 for i in range(m)]
    job_instr_counters = [0 for i in range(n)]

    last_job_on_machine = [None for i in range(m)]

    ancestors = [[None for _ in inst] for inst in instance ]
    pos = {}
    start = {}
    end = {}
    for idx, i in enumerate(sequence):
        m_id, duration = instance[i][job_instr_counters[i]]
        if job_ready[i] > machine_ready[m_id]:
            start_ts = job_ready[i]
            ancestors[i][job_instr_counters[i]] = (i,job_instr_counters[i]-1)
        else:
            start_ts = machine_ready[m_id]
            ancestors[i][job_instr_counters[i]] = last_job_on_machine[m_id]


        job_ready[i ] = start_ts + duration
        machine_ready[m_id] = start_ts + duration
        last_job_on_machine[m_id] = (i, job_instr_counters[i])
        pos[(i,job_instr_counters[i])] = idx
        start[(i,job_instr_counters[i])] = start_ts
        end[(i,job_instr_counters[i])] = start_ts + duration

        if start_ts + duration > total_makespan:
            total_makespan = start_ts + duration
            last_finishing_job = (i, job_instr_counters[i])

        job_instr_counters[i] += 1
        

    path = reconstruct_path(ancestors, last_finishing_job)
    return {
        'success': True,
        'makespan': max(job_ready),
        'critical_path': path,
        'start': start,
        'end': end,
        'seq_pos': pos
    }


# Neighbor helpers


def replace_in_seq(seq, i, j, inplace=False):
    if not inplace:
        tmp_seq = list(seq)
    else:
        tmp_seq = seq
    tmp = tmp_seq[i]
    tmp_seq[i] = tmp_seq[j]
    tmp_seq[j] = tmp
    return tmp_seq


def neighbors(sequence):
    for i in range(len(sequence)):
        for j in range(i+1, len(sequence)):
            if(sequence[i] != sequence[j]):
                yield replace_in_seq(sequence,i,j)


def get_random_neighbor(sequence, inplace=False):
    while True:
        i= random.randrange(0,len(sequence))
        j= random.randrange(0,len(sequence))

        if sequence[i] != sequence[j] :   
            return replace_in_seq(sequence,i,j, inplace=inplace)

def shake(seq, k):
    tmp_seq = list(seq)
    for _ in range(k):
        tmp_seq = get_random_neighbor(tmp_seq)
    return tmp_seq


def n1_neighbors(instance, sequence):
    result = decode_full(instance, sequence)
    if not result['success']:
        return None

    path: list = result['critical_path']
    pos: dict = result['seq_pos']


    n1 = []
    for pair in (zip(path, path[1:])):
        i,j = pair[0]
        k,l = pair[1]

        m1, _ = instance[i][j]
        m2, _ = instance[k][l]

        if m1 == m2:
            n1.append(replace_in_seq(sequence,pos[(i,j)], pos[(k,l)]))

    return n1

# methods

# BRUTE FORCE
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


# LOCAL SEARCH
def local_search(instance, sequence, firstimprov=False, budget=None, start=None):
    best_score = decode(instance,sequence)
    best_sequence = list(sequence)

    stalled = False
    while not stalled:
        if budget is not None and decode.calls - start >= budget:
            break
        stalled = True
        for neighbor in neighbors(sequence):

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
def local_search_budget(instance, sequence, budget=100000):
    start = decode.calls
    best_score, best_seq = local_search(instance, sequence, budget=budget, start=start)
    while decode.calls - start < budget:
        s = random.sample(sequence, len(sequence))
        value, seq = local_search(instance, s, budget=budget, start=start)
        if value < best_score:
            best_score, best_seq = value, seq
    return best_score, best_seq

# SIMULATED ANNEALING
def simulated_annealing(instance, sequence, budget = 100000):
    start = decode.calls
    best_sequence = list(sequence)
    best_score = decode(instance, sequence)
    T = 20
    alpha = (0.001/T)**(1/budget)

    current = sequence
    current_value = decode(instance,sequence)
    while decode.calls - start < budget:

        neighbor = get_random_neighbor(current)

        value = decode(instance,neighbor)

        if value < current_value:
            current = neighbor
            current_value = value

            if value < best_score:
                best_sequence = neighbor
                best_score = value

        else:
            delta = abs(current_value-value)

            T *= alpha
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
            p1 = select_parent(random.sample(current_scores[ELITISM:],TOUR_SIZE))
            p2 = select_parent(random.sample(current_scores[ELITISM:],TOUR_SIZE))

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
