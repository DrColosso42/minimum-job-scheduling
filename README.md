# Minimum Job Shop Scheduling

Course project for **Computational Intelligence**, Faculty of Mathematics, University of
Belgrade.

The job shop scheduling problem is solved with four metaheuristics, exhaustive search and
integer linear programming, and the resulting solutions are compared under equalised
conditions.

The full description of the problem, methodology and results can be found in [`rad/rad.pdf`](rad/rad.pdf) (in Serbian).

## What is implemented

Each of the four metaheuristics are implemented independently and transparently. Libraries are used for supporting work, primarily
for the analysis, plotting, storing results and stating the ILP problem.

Overview of the implemented methods can be found in the following table:

| method                        | module                  | based on                            |
| ----------------------------- | ----------------------- | ----------------------------------- |
| local search with restarts    | `src/jsp/heuristics.py` |                                     |
| simulated annealing           | `src/jsp/heuristics.py` |                                     |
| variable neighbourhood search | `src/jsp/heuristics.py` |                                     |
| genetic algorithm             | `src/jsp/heuristics.py` | PPX crossover                       |
| exhaustive search             | `src/jsp/exact.py`      |                                     |
| integer program               | `experiments/ilp.py`    | disjunctive formulation, Manne 1960 |

Repository uses **Bierwith's format** for solution encoding and all the supporting methods
are designed to work with that format only.

## Project overview

```
src/jsp/          the library
    instance.py       loading instances, trivial lower bound
    decoder.py        decode, decode_full, critical path reconstruction
    neighborhood.py   neighbourhoods: pairwise and n1
    exact.py          exhaustive search
    heuristics.py     the four optimisation methods
experiments/      scripts that produce the measurements found in results/
notebooks/        development, analysis and figures
data/             nine test instances
results/          measured data, as CSV
rad/              the write-up
```

## Running

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Reproducing the measurements

Each CSV in `results/` is produced by exactly one script:

| script                        | output                                                       |
| ----------------------------- | ------------------------------------------------------------ |
| `experiments/main.py`         | `results.csv`, `environment.txt`                             |
| `experiments/budget.py`       | `budget.csv`                                                 |
| `experiments/neighborhood.py` | `n1.csv`, `neigborhood_size.csv`, `decode_calls_descent.csv` |
| `experiments/ilp.py`          | `ilp.csv`                                                    |

The tables and figures used in the write-up are produced by `notebooks/analysis.ipynb` from
those files.

### Reproducibility

Every run starts from a fixed seed, following `seed = 1000 * r + 7`. The seed is recorded in
each output row, so a single run can be replayed independently of the rest:

```python
random.seed(9007)
start = random.sample(base, len(base))
decode.calls = 0
simulated_annealing(instance, start, budget=200_000)
```

## Exact solving

The project implements the problem formalisation as the ILP and solves it using CPLEX solver
with the help of the PuLP library. It is installed separately and it's path can be adjusted
using the `CPX` constant found in the relevant files.

Note that the community version of the CPLEX solver is limited to 1000 constraints which is not enough for solving largest instances in this repository.
The project relied on the unlimited CPLEX solver's version, obtained through IBM's Academic software licencing program.

## Instances

There are nine instances provided with the repository. Eight of them are obrained from the OR-Library.
Ninth one is generated for this project and has served primarily as a verification tool given it's modest size.
