import time
import itertools
import pulp
import sys
import pathlib
import re
BASE_PATH = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_PATH / "src"))
from jsp import load
import csv
import os



INSTANCES = [
    "mini3","ft06","la01","la02","la03","la04","la05","ft10","ft20"]


CPX = "/opt/ibm/ILOG/CPLEX_Academic/cplex/bin/x86-64_linux/cplex"



def build(instance):
    prob = pulp.LpProblem("jsp", pulp.LpMinimize)

    s = {}
    for j, job in enumerate(instance):
        for k in range(len(job)):
            s[(j,k)] = pulp.LpVariable(f"s_{j}_{k}", lowBound=0)

    Cmax = pulp.LpVariable("Cmax", lowBound=0)
    prob += Cmax

    for j, job in enumerate(instance):
        for k in range(len(job) -1 ):
            prob += s[(j,k+1)] >= s[(j,k)] + job[k][1]

        prob += Cmax >= s[(j, len(job) -1)] + job[-1][1]

    per_machine = {}
    for j, job in enumerate(instance):
        for k, (mid, dur) in enumerate(job):
            per_machine.setdefault(mid, []).append((j,k,dur))

    M = sum(d for job in instance for _, d in job)

    for mid, ops in per_machine.items():
        for (j1, k1, d1), (j2,k2,d2) in itertools.combinations(ops,2):
            z = pulp.LpVariable(f"z_{j1}_{k1}_{j2}_{k2}", cat="Binary")

            prob += s[(j1,k1)] + d1 <= s[(j2,k2)] + M * (1 - z)
            prob += s[(j2,k2)] + d2 <= s[(j1,k1)] + M * z
        


    return prob,s, Cmax

def parse_log(filepath):
    text = open(filepath).read()

    if "Integer optimal" in text:
        return None, True

    m= re.findall(r"Current MIP best bound\s*=\s*([\d.e+]+)",text)

    if m:
        return (float(m[-1])), False
    else: 
        return None, False

def ilp(instance, time_limit=18000, log=BASE_PATH / "results/cplex.log"):
    if os.path.exists(log):
        os.remove(log)
    prob, s, Cmax = build(instance)
    nv= len(prob.variables()) 
    nc = len(prob.constraints)

    t0 = time.perf_counter()
    prob.solve(pulp.CPLEX_CMD(
        path=CPX, msg=0, timeLimit=time_limit, logPath=str(log),
        keepFiles=False,
        gapRel=0,
        options=["set output clonelog -1"]

    ))
    dt = time.perf_counter() - t0

    makesp  = int(round(Cmax.value()))

    bound, proven = parse_log(log)
    

    return {
        "makespan": makesp,
        "proven": proven,
        "bound": makesp if proven else bound,
        "time": round(dt,1),
        "num_vars": nv,
        "num_constrs": nc
    }


with open(BASE_PATH / "results/ilp.csv", "w", newline="") as f:
    w = csv.writer(f)

    w.writerow(["instance", "num_vars", "num_constrs", "makespan", "bound",
                "proven", "gap", "time","time_limit"])

    for name in INSTANCES:
        inst = load(BASE_PATH / f"data/{name}.txt")
        r = ilp(inst, time_limit=3600,
                log=BASE_PATH / f"results/logs/cplex_{name}.log")

        msp = r["makespan"]
        bound = r["bound"]
        gap = round((msp - bound) / msp * 100,2)

        w.writerow(
            [name, r["num_vars"], r["num_constrs"], r["makespan"],
             int(r["bound"]), r["proven"], gap, r["time"],3600]
        )

        f.flush()
        print(name, r, flush=True)
