#apply a genetic algorithm to solve the 8-queens problem
#chess board representation

import matplotlib.pyplot as plt
import random

def print_board(board):
    for row in range(8):
        line = ""
        for col in range(8):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()

#fitness calculation 
def count_conflicts(board):
    conflicts = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j]:          # same row
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):  # same diagonal
                conflicts += 1
    return conflicts

def random_board():
    return [random.randint(0, 7) for _ in range(8)]

#selection
def tournament_select(population, k=4):
    candidates = random.sample(population, k)
    return min(candidates, key=count_conflicts)

def select_parents(population, num_pairs=24):
    return [(tournament_select(population), tournament_select(population)) for _ in range(num_pairs)]

def get_average_fitness(parents):
    if len(parents) == 0:
        return 100
    avg = 0
    for i in range(len(parents)):
        avg += count_conflicts(parents[i]) 
    return avg / len(parents)

def get_best_fitness(parents):
    if len(parents) == 0:
        return 100
    best = float('inf')
    for i in range(len(parents)):
        best = min(best, count_conflicts(parents[i]))
    return best

def breed(parents):
    p_len = len(parents)
    children = []
    for x in range(p_len):
        split = random.randint(1, 7)
        children.append(parents[x][0][:split] + parents[x][1][split:])
        children.append(parents[x][1][:split] + parents[x][0][split:])
    return children

def mutate(child):
    child = child.copy()
    for i in range(len(child)):
        if random.randint(0, 3) == 0:
            child[i] = random.randint(0, 7)
    return child

trial = 0
trials = []
avg_fitness = []
best_fitness = []

POP_SIZE = 500

population = [random_board() for _ in range(POP_SIZE)]

solved = False
stagnation = 0
last_best = float('inf')
STAGNATION_LIMIT = 100

while not solved:
    elites = sorted(population, key=count_conflicts)[:POP_SIZE//4]
    parents = select_parents(population)
    children = breed(parents)

    for i in range(len(children)):
        children[i] = mutate(children[i])

    population = elites + children

    current_best = count_conflicts(sorted(population, key=count_conflicts)[0])
    if current_best < last_best:
        last_best = current_best
        stagnation = 0
    else:
        stagnation += 1

    if stagnation >= STAGNATION_LIMIT:
        # replace bottom half with fresh random boards to break out of stagnation 
        population = sorted(population, key=count_conflicts)[:POP_SIZE//2] + [random_board() for _ in range(POP_SIZE//2)]
        stagnation = 0
        last_best = float('inf')

    for i in range(len(population)):
        if count_conflicts(population[i]) == 0:
            print_board(population[i])
            print("Solved")
            solved = True
    avg_fitness.append(get_average_fitness(population))
    best_fitness.append(get_best_fitness(population))
    trial += 1
    trials.append(trial)

plt.plot(trials, avg_fitness, label='average fitness')
plt.plot(trials, best_fitness, label='best fitness')

plt.xlabel('iteration')
plt.ylabel('# of conflicts')
plt.title('8-queens GA solution progress')
plt.legend()
plt.show()
