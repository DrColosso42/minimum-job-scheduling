
import csv
import random
import pathlib
import sys
import time
BASE_PATH = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH / "src"))
from jsp import *

NEIGHBORHOOD_INSTANCES = ["ft06", "ft10", "ft20"]
SAMPLES = 200
SIZE_SEED = 3

with open(BASE_PATH / "results/neigborhood_size.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["instance", "swap", "n1", "ratio", "samples"])

    for name in NEIGHBORHOOD_INSTANCES:
        instance = load(BASE_PATH / f"data/{name}.txt")
        base = [j for j, job in enumerate(instance) for _ in job]

        random.seed(SIZE_SEED)
        total_swap = total_n1 = 0
        for _ in range(SAMPLES):
            s = random.sample(base, len(base))
            total_swap += len(list(neighbors(s)))
            total_n1   += len(n1_neighbors(instance, s) or [])

        swap_avg = total_swap / SAMPLES
        n1_avg   = total_n1 / SAMPLES
        writer.writerow([name, round(swap_avg, 1), round(n1_avg, 1),
                         round(swap_avg / n1_avg, 1), SAMPLES])
        print(f"{name:6} swap {swap_avg:7.1f}   n1 {n1_avg:6.1f}"
              f"   ratio {swap_avg / n1_avg:6.1f}", flush=True)



N1_INSTANCES = [("ft06", 55), ("ft10", 930), ("ft20", 1165)]
BUDGET, REPEATS = 200_000, 10

SETUPS = [
    ("local_search", "swap", lambda i, s, b: local_search_budget(i, s, b)),
    ("local_search", "n1",   lambda i, s, b: local_search_budget(i, s, b, neighborhood=n1_neighborhood)),
    ("annealing",    "swap", lambda i, s, b: simulated_annealing(i, s, b)),
    ("annealing",    "n1",   lambda i, s, b: simulated_annealing(i, s, b, move=random_n1_move)),
]

with open(BASE_PATH / "results/n1.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["instance", "method", "neighborhood", "run", "seed",
                     "makespan", "decode_calls", "time", "optimum"])

    for name, optimum in N1_INSTANCES:
        instance = load(BASE_PATH / f"data/{name}.txt")
        base = [j for j, job in enumerate(instance) for _ in job]

        for method, neighborhood, run_fn in SETUPS:
            for r in range(REPEATS):
                seed = 1000 * r + 7
                random.seed(seed)
                start_seq = random.sample(base, len(base))

                decode.calls = 0
                t0 = time.perf_counter()
                score, _ = run_fn(instance, start_seq, BUDGET)
                dt = time.perf_counter() - t0

                writer.writerow([name, method, neighborhood, r, seed, score,
                                 decode.calls, round(dt, 2), optimum])
                f.flush()
                print(f"{name:6} {method:13} {neighborhood:5} {r:2} -> {score}", flush=True)



DESCENT_INSTANCES = ["ft06", "ft10", "ft20"]
DESCENT_RUNS = 10
DESCENT_SEED = 11

with open(BASE_PATH / "results/decode_calls_descent.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["instance", "improvement", "decode_calls_per_descent",
                     "mean_makespan", "runs"])

    for name in DESCENT_INSTANCES:
        instance = load(BASE_PATH / f"data/{name}.txt")
        base = [j for j, job in enumerate(instance) for _ in job]

        for label, first in [("best", False), ("first", True)]:
            random.seed(DESCENT_SEED)
            decode.calls = 0
            scores = []
            for _ in range(DESCENT_RUNS):
                s = random.sample(base, len(base))
                score, _ = local_search(instance, s, firstimprov=first)
                scores.append(score)

            per_descent = decode.calls // DESCENT_RUNS
            mean_makespan = sum(scores) / DESCENT_RUNS
            writer.writerow([name, label, per_descent,
                             round(mean_makespan, 1), DESCENT_RUNS])
            print(f"{name:6} {label:5} {per_descent:>7} calls/descent"
                  f"   mean {mean_makespan:8.1f}", flush=True)
