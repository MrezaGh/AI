from Society import *
from copy import copy


def create_rnd_law_book():
    law_book = {}
    for i in range(256):
        law_book[Society.base_convert(i, 2, 8)] = np.random.randint(0, 2)
    return law_book


def create_rnd_state(size=(15, 15)):
    return np.random.binomial(1, 0.5, size).astype(int)


def create_neighbors(law_book):
    neighbors = [law_book.copy() for i in range(256)]
    for i in range(256):
        if law_book[Society.base_convert(i, 2, 8)] == 1:
            neighbors[i][Society.base_convert(i, 2, 8)] = 0
        else:
            neighbors[i][Society.base_convert(i, 2, 8)] = 1
    return neighbors


def fitness_function(law_book, initial_state, depth):

    # state = [[initial_state[i][j] for j in range(len(initial_state[0]))] for i in range(len(initial_state))]
    state = copy(initial_state)

    global done
    num_of_awake = 0
    num_of_asleep = 0
    society = Society(law_book, state)
    society.compute_next_state(depth)

    for line in society.state:
        for item in line:
            if item == 0:
                num_of_asleep = num_of_asleep + 1
            else:
                num_of_awake = num_of_awake + 1

    made_awake = False
    if num_of_awake - num_of_asleep >= 0:
        made_awake = True
    asleep_awake_rate = abs(num_of_asleep - num_of_awake)

    society.compute_next_state()
    num_of_awake = 0
    num_of_asleep = 0
    for line in society.state:
        for item in line:
            if item == 0:
                num_of_asleep = num_of_asleep + 1
            else:
                num_of_awake = num_of_awake + 1
    if made_awake:
        value = num_of_asleep - num_of_awake + asleep_awake_rate
    else:
        value = num_of_awake - num_of_asleep + asleep_awake_rate

    if value == 450:
        done = True
    return value


def best_neighbor(law_book, law_book_fitness, neighbors, fitness):
    global best_value
    best_book = law_book
    best_fitness = law_book_fitness
    for i in range(256):
        if fitness[i] >= best_fitness:
            best_fitness = fitness[i]
            best_book = neighbors[i]
    best_value = best_fitness
    return best_book


def calculate_fitness(neighbors, state, depth):
    fitness = [0 for i in range(256)]
    for i in range(256):
        fitness[i] = fitness_function(neighbors[i], state, depth)
    return fitness


size = (15, 15)
state = create_rnd_state(size)
best_law_book = {}
best_value = 0
depth = 15


def main():
    global state, depth

    law_book = create_rnd_law_book()
    law_book_fitness = fitness_function(law_book, state.copy(), depth)

    while(True):
        neighbors = create_neighbors(law_book)
        fitness = calculate_fitness(neighbors, state.copy(), depth)
        law_book = best_neighbor(law_book, law_book_fitness, neighbors, fitness)
        law_book_fitness = fitness_function(law_book, state.copy(), depth)
        Society.save_law_book(law_book, './', 'hill_law_book')
        print(fitness)
        print("fitness: " + str(best_value))

main()



