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
