import csv, random, time, pathlib, sys

BASE_PATH = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH / "src"))

from jsp import *

INSTANCES = [("la03", 597), ("ft10", 930), ("ft20", 1165)]
BUDGET = 200000
REPEATS = 10

SCENARIOS = [
    ("annealing", "T0", [5,20,50,100],
    lambda i, s, b, v: simulated_annealing(i,s,b, T0=v)),
    ("vns", "kmax", [2,5,10,20],
    lambda i, s, b, v: vns(i,s,budget=b, kmax=v)),
     
    ("ga", "population_size", [20,50,100,200],
    lambda i, s, b, v: genetic_algorithm(i,s,budget=b, population_size=v)),
    ("ga", "p", [0.1,0.3,0.5,0.7],
    lambda i, s, b, v: genetic_algorithm(i,s,budget=b, p=v)),
    ("ga", "tournament_pct", [0.1,0.3,0.6],
    lambda i, s, b, v: genetic_algorithm(i,s,budget=b,tournament_pct=v)),

]

with open(BASE_PATH / f"results/parameters.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["instance", "method", "parameter", "value", "run", "seed", "makespan", "decode_calls",
                 "time", "optimum"])


    for name, optimum in INSTANCES:
        instance = load(BASE_PATH / f"data/{name}.txt")
        base = [j for j, job in enumerate(instance) for _ in job]

        for method, param, values, runner in SCENARIOS:
            for value in values:
                for r in range(REPEATS):
                    seed = 1000 * r + 7
                    random.seed(seed)
                    start_seq = random.sample(base,len(base))

                    decode.calls=0
                    t0 = time.perf_counter()

                    score, seq= runner(instance, start_seq, BUDGET, value)
                    dt = time.perf_counter() - t0

                    w.writerow([
                        name, method, param, value, r, seed, score, decode.calls,
                        dt, optimum
                    ])

                    f.flush()
                    print(f"{name} {method} {r} | ({param}:{value}) -> {score}", flush=True)