from Society import *
from copy import copy


def create_rnd_law_book():
    law_book = {}
    for i in range(256):
        law_book[Society.base_convert(i, 2, 8)] = np.random.randint(0, 2)
    return law_book


def create_rnd_state(size=(15, 15)):
    return np.random.binomial(1, 0.5, size).astype(int)


def make_situation_matrix(situation_martix, size, current_state):
    for i in range(size[0]):
        for j in range(size[1]):
            awake_neighbors = 0
            asleep_neighbors = 0
            if current_state[i][(j - 1) % size[1]] == 1:
                awake_neighbors = awake_neighbors + 1
                # print("4 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("4 asleep")
            if current_state[i][(j + 1) % size[1]] == 1:
                asleep_neighbors = asleep_neighbors + 1
                # print("5 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("5 sleep")
            if current_state[(i - 1) % size[0]][j] == 1:
                awake_neighbors = awake_neighbors + 1
                # print("2 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("2 asleep")
            if current_state[(i - 1) % size[0]][(j - 1) % size[1]] == 1:
                awake_neighbors = awake_neighbors + 1
                # print("1 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("1 asleep")
            if current_state[(i + 1) % size[0]][(j + 1) % size[1]] == 1:
                awake_neighbors = awake_neighbors + 1
                # print("7 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("7 asleep")
            if current_state[(i - 1) % size[0]][(j + 1) % size[1]] == 1:
                awake_neighbors = awake_neighbors + 1
                # print("3 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("3 asleep")
            if current_state[(i + 1) % size[0]][(j - 1) % size[1]] == 1:
                awake_neighbors = awake_neighbors + 1
                # print("6 awake")
            else:
                asleep_neighbors = asleep_neighbors + 1
                # print("6 asleep")
            situation_martix[i][j][0] = awake_neighbors
            situation_martix[i][j][1] = asleep_neighbors


def fitness_function3(law_book, initial_state, depth):
    global best_value, best_law_book, done
    smaller_state = initial_state[0:15, 0:15]
    society = Society(law_book, smaller_state)
    size = (len(society.state), len(society.state[0]))
    fitness = 0
    toggle = 0
    sync = 0
    for k in range(depth):
        num_of_awake = 0
        num_of_asleep = 0
        previous_state = copy(society.state)
        society.compute_next_state()
        for i in range(size[0]):
            for j in range(size[1]):
                if society.state[i][j] == 1:
                    num_of_awake = num_of_awake + 1
                elif society.state[i][j] == 0:
                    num_of_asleep = num_of_asleep + 1
                if previous_state[i][j] == 1 and society.state[i][j] == 0:
                    toggle = toggle + 1
                elif previous_state[i][j] == 0 and society.state[i][j] == 1:
                    toggle = toggle + 1
        sync = sync + abs(num_of_awake - num_of_asleep)
    sync = sync/depth
    toggle = toggle/depth
    fitness = toggle + sync

    if fitness > best_value:
        best_value = fitness
        print("toggle: " + str(toggle))
        print("sync: " + str(sync))
        best_law_book = law_book
        Society.save_law_book(law_book, './', 'law_book')

    return fitness


def fitness_function2(law_book, initial_state, depth):
    global best_value, best_law_book, done

    smaller_state = initial_state[0:15, 0:15]
    society = Society(law_book, smaller_state)
    size = (len(society.state), len(society.state[0]))
    situation_martix = [[[0 for k in range(2)] for i in range(size[1])] for j in range(size[0])]
    # situation_matrix[0][0][0] = shows number of awakes around (0,0)

    make_situation_matrix(situation_martix, size, society.state)
    toggle_value = 0
    society.compute_next_state()
    for i in range(size[0]):
        for j in range(size[1]):
            if situation_martix[i][j][0] > situation_martix[i][j][1]:  # awake_neighbors > asleep_neighbors
                if society.state[i][j] == 0:
                    toggle_value = toggle_value + 1
            else:
                if society.state[i][j] == 1:
                    toggle_value = toggle_value + 1
    toggle_value = toggle_value - 112

    old_value = 0
    for i in range(size[0]):
        for j in range(size[1]):
            old_value = old_value + abs(situation_martix[i][j][0] - situation_martix[i][j][1])

    society.compute_next_state(depth)
    make_situation_matrix(situation_martix, size, society.state)

    new_value = 0
    for i in range(size[0]):
        for j in range(size[1]):
            new_value = new_value + abs(situation_martix[i][j][0] - situation_martix[i][j][1])

    sync_value = (new_value - old_value)/100

    # value = value/6 + sync_value
    value = toggle_value/10 + sync_value
    if value > best_value:
        best_value = value
        print("toggle: " + str(value - sync_value))
        print("sync: " + str(sync_value))
        best_law_book = law_book
        Society.save_law_book(law_book, './', 'law_book')

    return value


def fitness_function(law_book, initial_state, depth):
    global best_value, best_law_book, done
    num_of_awake = 0
    num_of_asleep = 0

    smaller_state = initial_state[0:15, 0:15]
    society = Society(law_book, smaller_state)
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

    if value > best_value:
        # if value == 450:
        #     done = True
        best_value = value
        best_law_book = law_book
        Society.save_law_book(law_book, './', 'law_book')
    return value


def mix_genes(first_book, second_book):
    modified_first_book = {}
    modified_second_book = {}
    cross_over_position = np.random.randint(1, 256)
    for i in range(cross_over_position):
        modified_first_book[Society.base_convert(i, 2, 8)] = first_book[Society.base_convert(i, 2, 8)]
        modified_second_book[Society.base_convert(i, 2, 8)] = second_book[Society.base_convert(i, 2, 8)]
    for i in range(256 - cross_over_position):
        modified_first_book[Society.base_convert(255 - i, 2, 8)] = second_book[Society.base_convert(255 - i, 2, 8)]
        modified_second_book[Society.base_convert(255 - i, 2, 8)] = first_book[Society.base_convert(255 - i, 2, 8)]

    return modified_first_book, modified_second_book


def cross_over(selected_law_book):
    modified_books = [0 for i in range(sample_space_size)]
    for i in range(0, sample_space_size, 2):
        modified_books[i], modified_books[i + 1] = mix_genes(selected_law_book[i], selected_law_book[i + 1])

    return modified_books


def select_law_book(law_book, chance):
    random = np.random.random()
    current_chance = 0
    for i in range(sample_space_size):
        current_chance = current_chance + chance[i]
        if current_chance >= random:
            # print("selected law book: " + str(i))
            return law_book[i]
    return law_book[sample_space_size - 1]


def select_law_books(fitness, law_book):
    chance = [0.0 for i in range(sample_space_size)]
    min_fitness = min(fitness)
    if min_fitness <= 0:
        for i in range(sample_space_size):
            fitness[i] = fitness[i] + abs(min_fitness) + 1

    fitness_sum = sum(fitness)

    for i in range(sample_space_size):
        chance[i] = fitness[i] / fitness_sum

    selected_law_book = [0 for i in range(sample_space_size)]
    for i in range(sample_space_size):
        selected_law_book[i] = select_law_book(law_book, chance)
    return selected_law_book


def calculate_fitness(law_book, state, depth):
    fitness = [0 for i in range(sample_space_size)]
    for i in range(sample_space_size):
        fitness[i] = fitness_function3(law_book[i], state.copy(), depth)
    return fitness


def mutate_law_book(law_book):
    random_law = np.random.randint(0, 256)
    if law_book[Society.base_convert(random_law, 2, 8)]:
        law_book[Society.base_convert(random_law, 2, 8)] = 0
    else:
        law_book[Society.base_convert(random_law, 2, 8)] = 1
    return law_book


# def mutate(modified_law_book):  # Intragenic mutation
#     for i in range(sample_space_size):
#         if mutation_rate > (np.random.random() * 100):
#             print("mutated: " + str(i))
#             modified_law_book[i] = mutate_law_book(modified_law_book[i])
#     return modified_law_book

def mutate(modified_law_book):  # Intergenic mutation
    mutated_law_book = modified_law_book.copy()
    for i in range(sample_space_size):
        for j in range(256):
            if mutation_rate > (np.random.random() * 100):
                if mutated_law_book[i][Society.base_convert(j, 2, 8)]:
                    mutated_law_book[i][Society.base_convert(j, 2, 8)] = 0
                else:
                    mutated_law_book[i][Society.base_convert(j, 2, 8)] = 1
                # print("mutated: law_book-> " + str(i) + " gene: ->" + str(j))
    return mutated_law_book

# =================================================================================================================


sample_space_size = 14
mutation_rate = 0.5
fitness_depth = 10

best_law_book = {}
best_value = 0
state = create_rnd_state((150, 150))
done = False


def main(fitness_depth):
    depth = fitness_depth
    law_book = [{} for i in range(sample_space_size)]

    for i in range(sample_space_size):  # 10 could be bigger
        law_book[i] = create_rnd_law_book()

    fitness = 0
    rounds_passed = 0

    while(True):
        if done:
            print("done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            break
        fitness = calculate_fitness(law_book, state, depth)
        print(fitness)
        print(sum(fitness))
        print("best: " + str(best_value))
        selected_law_book = select_law_books(fitness, law_book)
        modified_law_book = cross_over(selected_law_book)
        mutated_law_book = mutate(modified_law_book)
        law_book = mutated_law_book
        rounds_passed = rounds_passed + 1
        if rounds_passed % 20 == 0:
            # depth = int(depth*1.1)
            depth = int(depth + 4)  # todo
            print("CURRENT DEPTH: " + str(depth))


main(fitness_depth)

