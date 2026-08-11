
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
