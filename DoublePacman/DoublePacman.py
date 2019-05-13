# Title: DoublePacman
# Written: by MrezaGh
# Date: March 3 2019
# Intro:
#     this program solves a problem in which we are looking for the best way to eat all the beans in a pacman envirment
#     in which there are 2 pacmans and various walls and no ghosts
#     I implemented A* algorithm for doing so
#     cheers :)
# Sample input:
#     4 4
#     3 3 2 3
#     2 4 4 2
#     3 1 2 3
#     2 3 3 1
#     O


def main():
    m, n, initial_map, initial_pac_man1, initial_pac_man2, non_overlapping = get_inputs()

    # initialize frontier and visited list
    frontier = []
    visited = []

    # building the initial state using inputs
    start_node = Node(initial_map, initial_pac_man1, initial_pac_man2, None)

    frontier.append(start_node)

    number_of_expansions = 0
    while frontier:  # as long as frontier is not empty do this

        # finding the best node to expand(using f) # TODO: could be better in performance
        current_node = frontier[0]
        current_index = 0
        for index, item in enumerate(frontier):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # if it's goal state return path
        if check_goal_state(current_node.game_map):
            # print('number of expansions: ' + str(number_of_expansions))
            # print('cost: ')
            print(current_node.g)
            solution_path = path(current_node)
            for movement in solution_path:
                print(movement)
            return

        # remove current node from frontier and add to visited
        frontier.pop(current_index)
        visited.append(current_node)

        number_of_expansions = number_of_expansions + 1

        # build all possible next states after expansion
        children = expand_node(current_node, non_overlapping)

        # add them to frontier
        add_children_to_frontier(children, frontier, visited)

    return print("couldn't find it")


def heuristic(current_node):  # TODO
    # return 0
    h1 = count_number_of_remaining_beans(current_node)/2
    # return h1
    h2 = north_south_west_east_distance(current_node)
    # return h2
    h3 = furthest_bean_distance(current_node)
    # return h3
    return max(h1, h2, h3)


def add_children_to_frontier(children, frontier, visited):
    for node in children:
        if not visited.__contains__(node):
            if frontier.__contains__(node):  # idk if this is necessary...
                for index, item in enumerate(frontier):
                    if item == node and node.g < item.g:
                        frontier[index] = node  # todo: update frontier or resort it
            else:
                frontier.append(node)


def expand_node(current_node, non_overlapping):
    children = []
    # if action is pac_man1: Up and pac_man2: Up
    if p1_up_is_possible(current_node) and p2_up_is_possible(current_node):
        # build the new state after moving up
        new_state = build_new_state(current_node, 'U', 'U')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_up_is_possible(current_node) and p2_down_is_possible(current_node):
        new_state = build_new_state(current_node, 'U', 'D')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_up_is_possible(current_node) and p2_right_is_possible(current_node):
        new_state = build_new_state(current_node, 'U', 'R')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_up_is_possible(current_node) and p2_left_is_possible(current_node):
        new_state = build_new_state(current_node, 'U', 'L')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_down_is_possible(current_node) and p2_up_is_possible(current_node):
        new_state = build_new_state(current_node, 'D', 'U')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_down_is_possible(current_node) and p2_down_is_possible(current_node):
        new_state = build_new_state(current_node, 'D', 'D')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_down_is_possible(current_node) and p2_right_is_possible(current_node):
        new_state = build_new_state(current_node, 'D', 'R')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_down_is_possible(current_node) and p2_left_is_possible(current_node):
        new_state = build_new_state(current_node, 'D', 'L')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_right_is_possible(current_node) and p2_up_is_possible(current_node):
        new_state = build_new_state(current_node, 'R', 'U')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_right_is_possible(current_node) and p2_down_is_possible(current_node):
        new_state = build_new_state(current_node, 'R', 'D')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_right_is_possible(current_node) and p2_right_is_possible(current_node):
        new_state = build_new_state(current_node, 'R', 'R')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_right_is_possible(current_node) and p2_left_is_possible(current_node):
        new_state = build_new_state(current_node, 'R', 'L')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_left_is_possible(current_node) and p2_up_is_possible(current_node):
        new_state = build_new_state(current_node, 'L', 'U')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_left_is_possible(current_node) and p2_down_is_possible(current_node):
        new_state = build_new_state(current_node, 'L', 'D')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_left_is_possible(current_node) and p2_right_is_possible(current_node):
        new_state = build_new_state(current_node, 'L', 'R')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_left_is_possible(current_node) and p2_left_is_possible(current_node):
        new_state = build_new_state(current_node, 'L', 'L')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_up_is_possible(current_node):
        new_state = build_new_state(current_node, 'U', 'S')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_down_is_possible(current_node):
        new_state = build_new_state(current_node, 'D', 'S')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_right_is_possible(current_node):
        new_state = build_new_state(current_node, 'R', 'S')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p1_left_is_possible(current_node):
        new_state = build_new_state(current_node, 'L', 'S')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p2_up_is_possible(current_node):
        new_state = build_new_state(current_node, 'S', 'U')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p2_down_is_possible(current_node):
        new_state = build_new_state(current_node, 'S', 'D')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p2_right_is_possible(current_node):
        new_state = build_new_state(current_node, 'S', 'R')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    if p2_left_is_possible(current_node):
        new_state = build_new_state(current_node, 'S', 'L')
        if non_overlapping:
            if not new_state.pac_man1 == new_state.pac_man2:
                children.append(new_state)
        else:
            children.append(new_state)
    return children


def north_south_west_east_distance(current_node):
    northern_bean = None
    southern_bean = None
    eastern_bean = None
    western_bean = None
    for height, line in enumerate(current_node.game_map):
        for width, tile in enumerate(line):
            if tile == 2:
                if not northern_bean:
                    northern_bean = height
                if not southern_bean:
                    southern_bean = height
                if not eastern_bean:
                    eastern_bean = width
                if not western_bean:
                    western_bean = width

                if height < northern_bean:
                    northern_bean = height
                if height > southern_bean:
                    southern_bean = height
                if width < western_bean:
                    western_bean = width
                if width > eastern_bean:
                    eastern_bean = width
    p1_to_northern_bean = current_node.pac_man1[0] - northern_bean
    if p1_to_northern_bean < 0:
        p1_to_northern_bean = 0
    p2_to_northern_bean = current_node.pac_man2[0] - northern_bean
    if p2_to_northern_bean < 0:
        p2_to_northern_bean = 0
    p1_to_southern_bean = southern_bean - current_node.pac_man1[0]
    if p1_to_southern_bean < 0:
        p1_to_southern_bean = 0
    p2_to_southern_bean = southern_bean - current_node.pac_man2[0]
    if p2_to_southern_bean < 0:
        p2_to_southern_bean = 0
    p1_to_western_bean = current_node.pac_man1[1] - western_bean
    if p1_to_western_bean < 0:
        p1_to_western_bean = 0
    p2_to_western_bean = current_node.pac_man2[1] - western_bean
    if p2_to_western_bean < 0:
        p2_to_western_bean = 0
    p1_to_eastern_bean = eastern_bean - current_node.pac_man1[1]
    if p1_to_eastern_bean < 0:
        p1_to_eastern_bean = 0
    p2_to_eastern_bean = eastern_bean - current_node.pac_man2[1]
    if p2_to_eastern_bean < 0:
        p2_to_eastern_bean = 0
    h2 = min(p1_to_northern_bean, p2_to_northern_bean) + min(p1_to_southern_bean, p2_to_southern_bean) + \
         min(p1_to_eastern_bean, p2_to_eastern_bean) + min(p1_to_western_bean, p2_to_western_bean)
    return h2


def count_number_of_remaining_beans(current_node):
    number_of_beans = 0
    for line in current_node.game_map:
        for tile in line:
            if tile == 2:
                number_of_beans = number_of_beans + 1
    return number_of_beans


def furthest_bean_distance(current_node):
    max_distance = None
    for height, line in enumerate(current_node.game_map):
        for width, tile in enumerate(line):
            if tile == 2:
                p1_horizontal_distance = abs(current_node.pac_man1[1] - width)
                p2_horizontal_distance = abs(current_node.pac_man2[1] - width)

                p1_vertical_distance = abs(current_node.pac_man1[0] - height)
                p2_vertical_distance = abs(current_node.pac_man2[0] - height)

                p1_manhattan_distance = p1_vertical_distance + p1_horizontal_distance
                p2_manhattan_distance = p2_vertical_distance + p2_horizontal_distance

                distance = min(p1_manhattan_distance, p2_manhattan_distance)

                if not max_distance:
                    max_distance = distance
                elif distance > max_distance:
                    max_distance = distance
    return max_distance






class Node:
    def __init__(self, game_map, pac_man1, pac_man2, parent=None, action=None):
        self.parent = parent
        self.game_map = game_map
        self.pac_man1 = pac_man1
        self.pac_man2 = pac_man2
        self.g = 0
        self.h = 0
        self.f = 0
        self.action = action

    def __eq__(self, other):
        return self.game_map == other.game_map and self.pac_man1 == other.pac_man1 and self.pac_man2 == other.pac_man2

    def __str__(self):
        return str(self.game_map)

    def __copy__(self):
        return Node(self.game_map[:], self.pac_man1, self.pac_man2, self.parent, self.action)


def get_inputs():
    file = open("./testCase1", 'r')
    pac_man1 = None
    pac_man2 = None
    first_line = file.readline()
    first_line = first_line.split()
    m = int(first_line[0])
    n = int(first_line[1])
    game_map = [[0 for i in range(n)] for j in range(m)]
    for i in range(m):
        line = file.readline()
        line = line.split()
        for j in range(n):
            game_map[i][j] = int(line[j])
            if int(line[j]) == 1 and not pac_man1:
                pac_man1 = (i, j)
            elif int(line[j]) == 1 and not pac_man2:
                pac_man2 = (i, j)
    none_overlapping = True
    if not file.readline() == 'N':
        none_overlapping = False

    # if none_overlapping:
    #     print('none-overlapping')
    # else:
    #     print('overlapping')
    # print(m, n)
    # print(game_map)
    # print('pac_man1: ', pac_man1)
    # print('pac_man2: ', pac_man2)
    return m, n, game_map, pac_man1, pac_man2, none_overlapping


def check_goal_state(game_map):
    for line in game_map:
        for tile in line:
            if tile == 2:
                return False
    return True


def build_new_state(current_node, pac_man1_direction, pac_man2_direction):
    new_map = [i[:] for i in current_node.game_map]
    new_pac_man1 = current_node.pac_man1
    new_pac_man2 = current_node.pac_man2
    action = pac_man1_direction + pac_man2_direction

    new_map[current_node.pac_man1[0]][current_node.pac_man1[1]] = 3
    if pac_man1_direction == 'U':
        new_map[current_node.pac_man1[0] - 1][current_node.pac_man1[1]] = 1
        new_pac_man1 = (current_node.pac_man1[0] - 1, current_node.pac_man1[1])
    elif pac_man1_direction == 'D':
        new_map[current_node.pac_man1[0] + 1][current_node.pac_man1[1]] = 1
        new_pac_man1 = (current_node.pac_man1[0] + 1, current_node.pac_man1[1])
    elif pac_man1_direction == 'L':
        new_map[current_node.pac_man1[0]][current_node.pac_man1[1] - 1] = 1
        new_pac_man1 = (current_node.pac_man1[0], current_node.pac_man1[1] - 1)
    elif pac_man1_direction == 'R':
        new_map[current_node.pac_man1[0]][current_node.pac_man1[1] + 1] = 1
        new_pac_man1 = (current_node.pac_man1[0], current_node.pac_man1[1] + 1)
    elif pac_man1_direction == 'S':
        new_map[current_node.pac_man1[0]][current_node.pac_man1[1]] = 1

    new_map[current_node.pac_man2[0]][current_node.pac_man2[1]] = 3
    if pac_man2_direction == 'U':
        new_map[current_node.pac_man2[0] - 1][current_node.pac_man2[1]] = 1
        new_pac_man2 = (current_node.pac_man2[0] - 1, current_node.pac_man2[1])
    elif pac_man2_direction == 'D':
        new_map[current_node.pac_man2[0] + 1][current_node.pac_man2[1]] = 1
        new_pac_man2 = (current_node.pac_man2[0] + 1, current_node.pac_man2[1])
    elif pac_man2_direction == 'L':
        new_map[current_node.pac_man2[0]][current_node.pac_man2[1] - 1] = 1
        new_pac_man2 = (current_node.pac_man2[0], current_node.pac_man2[1] - 1)
    elif pac_man2_direction == 'R':
        new_map[current_node.pac_man2[0]][current_node.pac_man2[1] + 1] = 1
        new_pac_man2 = (current_node.pac_man2[0], current_node.pac_man2[1] + 1)
    elif pac_man2_direction == 'S':
        new_map[current_node.pac_man2[0]][current_node.pac_man2[1]] = 1

    new_state = Node(new_map, new_pac_man1, new_pac_man2, parent=current_node, action=action)
    new_state.g = current_node.g + 1
    new_state.h = heuristic(current_node)  # TODO: implement
    new_state.f = new_state.g + new_state.h

    # print("from build state: " + str(current_node.game_map))

    return new_state


def p1_up_is_possible(current_node):
    # goes out of map
    if current_node.pac_man1[0] - 1 < 0:
        return False
    up_not_wall = current_node.game_map[current_node.pac_man1[0] - 1][current_node.pac_man1[1]] != 4
    return up_not_wall


def p2_up_is_possible(current_node):
    # goes out of map
    if current_node.pac_man2[0] - 1 < 0:
        return False
    up_not_wall = current_node.game_map[current_node.pac_man2[0] - 1][current_node.pac_man2[1]] != 4
    return up_not_wall


def p1_down_is_possible(current_node):
    # goes out of map
    if current_node.pac_man1[0] + 1 >= current_node.game_map.__len__():
        return False
    down_not_wall = current_node.game_map[current_node.pac_man1[0] + 1][current_node.pac_man1[1]] != 4
    return down_not_wall


def p2_down_is_possible(current_node):
    # goes out of map
    if current_node.pac_man2[0] + 1 >= current_node.game_map.__len__():
        return False
    down_not_wall = current_node.game_map[current_node.pac_man2[0] + 1][current_node.pac_man2[1]] != 4
    return down_not_wall


def p1_right_is_possible(current_node):
    # goes out of map
    if current_node.pac_man1[1] + 1 >= current_node.game_map[0].__len__():
        return False
    right_not_wall = current_node.game_map[current_node.pac_man1[0]][current_node.pac_man1[1] + 1] != 4
    return right_not_wall


def p2_right_is_possible(current_node):
    # goes out of map
    if current_node.pac_man2[1] + 1 >= current_node.game_map[0].__len__():
        return False
    right_not_wall = current_node.game_map[current_node.pac_man2[0]][current_node.pac_man2[1] + 1] != 4
    return right_not_wall


def p1_left_is_possible(current_node):
    # goes out of map
    if current_node.pac_man1[1] - 1 < 0:
        return False
    left_not_wall = current_node.game_map[current_node.pac_man1[0]][current_node.pac_man1[1] - 1] != 4
    return left_not_wall


def p2_left_is_possible(current_node):
    # goes out of map
    if current_node.pac_man2[1] - 1 < 0:
        return False
    left_not_wall = current_node.game_map[current_node.pac_man2[0]][current_node.pac_man2[1] - 1] != 4
    return left_not_wall


def path(current_node):
    solution_path = []
    while current_node.parent is not None:
        solution_path.append(current_node.action)
        current_node = current_node.parent

    return solution_path[::-1]


# ==============================================================================================================

main()
