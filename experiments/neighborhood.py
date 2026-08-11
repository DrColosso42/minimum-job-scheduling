
import csv
import random
import pathlib
import sys

BASE_PATH = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,"src")
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