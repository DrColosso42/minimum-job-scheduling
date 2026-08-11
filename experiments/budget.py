
import  csv
import numpy as np
import sys
import pathlib
import time
import random

BASE_PATH = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH / "src"))
from jsp import *

BUDGET_RANGE  = np.logspace(3, 6, 8).astype(int)      # 1 000 … 1 000 000
INSTANCES = [("ft06", 55), ("ft10", 930), ("ft20", 1165)]
METHODS   = {"annealing": simulated_annealing,
            "vns": vns,
            "ga": genetic_algorithm,
            "local_search": local_search_budget}
REPEATS = 5



def experiment(instance, name,method, optimum, repeats=30, seed=0, printinfo=True, **kwargs):
    decode.calls = 0
    L = sum(len(job) for job in instance)
    base = [j for j, job in enumerate(instance) for _ in job]
    rng = random.Random(seed)

    t0 = time.perf_counter()
    results = []

    for _ in range(repeats):
        start = rng.sample(base, L)
        if(kwargs):
            score, _ = method(instance, start, **kwargs)
        else:
            score, _ = method(instance, start)
        results.append(score)


    dt = time.perf_counter() - t0

    if printinfo:
        print("===========================")
        print(f"{name}: Started {repeats} optimizations with different starting points.")
        print(f"Took {dt:.1f} seconds. Called decode {decode.calls} times")
        print(f"Best score: {min(results)}, avg: {sum(results)/repeats:.1f}. Worst: {max(results)}")
        print(f"Optimum {optimum}")
        print(f"Local optimums found: {sorted(set(results))}")
        print("===========================")

    result = {
        'time': dt,
        'decode_calls': decode.calls,
        'best_score': min(results),
        'optimum': optimum,
        'optimums': sorted(set(results)),
        'average': sum(results)/repeats,
    }
    return result


with open(BASE_PATH / "results/budget.csv", "w", newline="") as f:
    w = csv.writer(f)

    w.writerow(["instance", "method", "budget", "decode_calls",
                "best", "average", "optimum", "time"])

    for name, opt in INSTANCES:
        inst = load(BASE_PATH / f"data/{name}.txt")
        for method_name, method in METHODS.items():
            for b in BUDGET_RANGE:
                r = experiment(inst, name, method, opt,
                               repeats=REPEATS, seed=42,
                               printinfo=False, budget=int(b))
                w.writerow([name, method_name, int(b),
                            r["decode_calls"],
                            r["best_score"], round(r["average"], 2),
                            opt, round(r["time"], 1)])
                f.flush()
                print(f"{name:6} {method_name:13} {b:>8} -> "
                      f"{r['average']:7.1f}  ({r['time']:.0f}s)", flush=True)




