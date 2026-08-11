import random

from .decoder import decode_full

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


def swap_neighborhood(instance, sequence):
    return neighbors(sequence)


def n1_neighborhood(instance, sequence):
    return n1_neighbors(instance, sequence) or []


def random_swap_move(instance, sequence):
    return get_random_neighbor(sequence)


def random_n1_move(instance, sequence):
    candidates = n1_neighbors(instance, sequence)
    return random.choice(candidates) if candidates else get_random_neighbor(sequence)