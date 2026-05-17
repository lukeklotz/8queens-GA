# 8-Queens Genetic Algorithm Solver

## How it works

1. **Population**: starts with 500 randomly placed boards
2. **Selection**: tournament selection picks the least-conflicted boards as parents
3. **Crossover**: pairs of parents swap segments to produce children
4. **Mutation**: each gene has a 25% chance of being randomized
5. **Elitism**: the top 25% of each generation survive unchanged
6. **Stagnation recovery**: if fitness stops improving for 100 generations, the bottom half of the population is replaced with fresh random boards

The loop runs until a board with zero conflicts is found, then prints the solution and plots average and least conflicts per generation over time.

## Usage 

### Windows

```bash
python main.py
```

### Linux/Max

```bash
python3 main.py
```

Requires `matplotlib`.
