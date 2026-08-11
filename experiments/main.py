import csv, time, random, platform, sys, pathlib, cpuinfo, psutil, datetime

BASE_PATH = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH / "src"))

from jsp import *


# pyright: reportFunctionMemberAccess=false


INSTANCES = [
    # name, lower bound, optimum, optimum source
    ("mini3",10,11, "bruteforce"),
    ("ft06",47,55, "Fisher & Thompson 1963"),
    ("la01",666,666,"lower bound"),
    ("la02",635,655,"Lawrence 1984"),
    ("la03",588,597,"Lawrence 1984"),
    ("la04",537,590,"Lawrence 1984"),
    ("la05",593,593,"donja granica = optimum"),
    ("ft10",655,930,"Fisher & Thompson 1963"),
    ("ft20",1119, 1165,"Fisher & Thompson 1963")
]

METHODS = {
    "local_search": local_search_budget,
    "annealing": simulated_annealing,
    "vns": vns,
    "ga": genetic_algorithm
}

BUDGET = 200_000
REPEATS = 30
DATA_PATH = BASE_PATH / "data"
# INSTANCES = INSTANCES[]




with open(BASE_PATH / "results/environment.txt", "w") as f:
    ci = cpuinfo.get_cpu_info()
    f.write(f"procesor: {ci['brand_raw']}\n")
    f.write(f"freq:     {ci['hz_advertised_friendly']}\n")
    f.write(f"cores:    {psutil.cpu_count(logical=False)} / {psutil.cpu_count()} (cores/threads)\n")
    f.write(f"RAM:      {psutil.virtual_memory().total / 2**30:.1f} GB\n")
    f.write(f"OS:       {platform.platform()}\n")
    f.write(f"Python:   {sys.version.split()[0]}\n")


ts = datetime.datetime.now()
with open(BASE_PATH / f"results/results-{ts}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["instance", "method", "run", "seed", "makespan", "decode_calls",
                 "time", "lower_bound", "optimum", "optimum_source"])

    
    for name, lb, opt, opt_s in INSTANCES:
        instance = load(DATA_PATH / f"{name}.txt")

        base = [j for j, job in enumerate(instance) for _ in job]

        for method_name, method in METHODS.items():
            for r in range(REPEATS):
                seed = 1000 * r + 7
                random.seed(seed)
                start_seq = random.sample(base,len(base))

                decode.calls = 0
                t0 = time.perf_counter()
                score, _ = method(instance, start_seq, budget=BUDGET)
                dt = time.perf_counter() - t0

                w.writerow([
                    name, method_name, r, seed, score,
                    decode.calls, round(dt,3),lb,opt, opt_s
                ])
                f.flush()
                print(f"{name} {method_name} {r}: {score}", flush=True)