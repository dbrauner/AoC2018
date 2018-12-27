import operator
import os
import sys
import collections


class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

import heapq
import operator

# from . import custom_graph


# from .custom_graph import *
# import CustomGraph

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


#
# class SimpleGraph:
#     def __init__(self):
#         self.edges = {}
#
#     def neighbors(self, id):
#         return self.edges[id]
#

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.obstacles

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]

        results.sort(key=operator.itemgetter(0, 1))

        # if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

#
# def neighbors(node, _map, d_units):
#     dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
#     result = []
#     for dir in dirs:
#         neighbor = [node[0] + dir[0], node[1] + dir[1]]
#         if 0 <= neighbor[0] < len(_map) and 0 <= neighbor[1] < len(_map[0]) and neighbor not in d_units:
#             result.append(neighbor)
#     return result

def create_graph_from_map(_map, d_units, unit):
    grid = GridWithWeights(len(_map[0]), len(_map))
    for i, x in enumerate(_map):
        for j, y in enumerate(x):
            if _map[i][j] == '#' or (i, j) in d_units:
                if (i, j) != (unit._x, unit._y): # ignores the unit itself
                    grid.obstacles.append((i, j))
    return grid

class Unit:
    def __init__(self, _class, _x, _y):
        self._x = _x
        self._y = _y
        self._class = _class
        self.life = 200
        # self.cross_mod = 0
        # self.dead = False


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]

        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


def print_map(_map, units):
    for i, v in enumerate(_map):
        s = ''
        line_units = list()
        for j, x in enumerate(v):
            found = False
            for a, unit in enumerate(units):
                if [i, j] == [unit._x, unit._y]:
                    s += unit._class
                    # s += str(a)
                    line_units.append(unit)
                    found = True
            if not found:
                s += x
        if len(line_units) > 0:
            first = True
            for unit in line_units:
                if first:
                    s += '   '
                else:
                    s += ', '
                first = False
                s += unit._class + '(' + str(unit.life) + ')'
        print(s)


def bsf_search(graph, start, goals):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()
        if current in goals:
            break

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from, current


def create_graph(the_map, units, unit):
    d_units = {(unit._x, unit._y): unit.life for unit in units}

    graph = SquareGrid(len(the_map[0]), len(the_map))

    for i, x in enumerate(the_map):
        for j, y in enumerate(the_map[i]):
            if the_map[i][j] == '#':
                graph.walls.append((i, j))
            if (i, j) in d_units:
                if d_units[(i, j)] > 0:
                    for a, u in enumerate(units):
                        if (i, j) == (u._x, u._y) and (i, j) != (unit._x, unit._y) and unit._class == u._class:
                            graph.walls.append((i, j))
    return graph


def calculate_cost_to_reach(graph, came_from, current):
    min_cost = sys.maxsize
    location = None
    for next in graph.neighbors(current):
        if next in came_from:
            cost = 0
            p = next
            while came_from[p] is not None:
                cost += 1
                p = came_from[p]
            if cost < min_cost:
                min_cost = cost
                location = next
    return min_cost, location


def move_unit_to_closest_target(unit, target, graph):
    x, y = unit._x, unit._y
    next_positions = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
    selected_position = None
    selected = {}
    nearest = sys.maxsize
    for next_pos in next_positions:
        if next_pos in graph.walls:
            continue
        came_from, current = bsf_search(graph, next_pos, target)
        min_cost, location = calculate_cost_to_reach(graph, came_from, current)
        if min_cost == nearest and location not in selected:
            selected[location] = next_pos
        if min_cost < nearest:
            nearest = min_cost
            selected_position = next_pos
            selected.clear()
            selected[location] = next_pos

    # max_hp = sys.maxsize
    # for s in selected:
    #     if target[s] < max_hp:
    #         max_hp = target[s]
    #         selected_position = s

    # selected_list = list(collections.OrderedDict(sorted(selected.items())).values())
    # # selected.sort(key=operator.itemgetter(0,1))
    # unit._x = selected_list[0][0]
    # unit._y = selected_list[0][1]
    key = min(selected)
    unit._x = selected[key][0]
    unit._y = selected[key][1]


def attack_enemy_with_least_hp(unit, graph, enemies):
    x, y = unit._x, unit._y
    next_positions = [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]
    selected_enemy = None
    min_hp = sys.maxsize

    for next_pos in next_positions:
        if next_pos in graph.walls:
            continue
        for i, enemy in enumerate(enemies):
            if (enemy._x, enemy._y) == next_pos:
                if enemy.life < min_hp:
                    min_hp = enemy.life
                    selected_enemy = i
    attack_enemy(unit, enemies[selected_enemy])

def execute_action(enemies, unit, _map, units):
    graph = create_graph(_map, units, unit)
    d_enemies = {(unit._x, unit._y): unit.life for unit in enemies}

    came_from, target = bsf_search(graph, (unit._x, unit._y), d_enemies)
    if target not in d_enemies: # impossible to reach target
        return

    min_cost, location = calculate_cost_to_reach(graph, came_from, target)

    if min_cost > 0:
        move_unit_to_closest_target(unit, d_enemies, graph)
        min_cost -= 1
    if min_cost == 0:
        attack_enemy_with_least_hp(unit, graph, enemies)
    pass


def find_enemies(unit, units):
    enemies = list()
    for u in units:
        if u._class != unit._class and u.life > 0:
            enemies.append(u)
    return enemies


def check_position(_x, _y, d_units, _map):
    occupied = False
    if _map[_x][_y] == '.':
        if (_x, _y) in d_units:
            if d_units[_x, _y] > 0:
                # for a, unit in enumerate(units):
                #     if [_x, _y] == [unit._x, unit._y] and unit.life > 0:
                occupied = True
                # break
        if not occupied:
            return True
    return False


def steps_to_reach(x, y, el, _map, units, visited, steps):
    if not check_position(x, y, units, _map) or (x, y) in visited:
        return - 1
    steps += 1
    if (x, y) == (el[0], el[1]):
        return steps

    visited.append((x, y))

    a = steps_to_reach(x - 1, y, el, _map, units, visited, steps)
    # if x > - 1:
    #     a = x
    # if next > -1:
    #     # steps = next
    #     # if next > steps:
    #     return next
    b = steps_to_reach(x, y - 1, el, _map, units, visited, steps)
    # if next > -1:
    #     steps = next
    #     # if next > steps:
    #     return next
    c = steps_to_reach(x, y + 1, el, _map, units, visited, steps)
    # if next > -1:
    #     steps = next
    #     # if next > steps:
    #     return next
    d = steps_to_reach(x + 1, y, el, _map, units, visited, steps)
    # if next > -1:
    #     steps = next
    #     # if next > steps:
    #     return next
    _range = [x for x in [a, b, c, d] if x > -1]
    if len(_range) > 0:
        return min(_range)
    else:
        return - 1


def calculate_steps(unit, enemy, _map, units, move):
    d_units = {(unit._x, unit._y): unit.life for unit in units}
    graph = create_graph_from_map(_map, d_units)
    came_from, cost_so_far = a_star_search(graph, (unit._x, unit._y), (enemy._x, enemy._y))

    # path = reconstruct_path(came_from, (unit._x, unit._y), (enemy._x, enemy._y))
    range = list()

    if check_position(enemy._x - 1, enemy._y, d_units, _map) or (enemy._x - 1, enemy._y) == (unit._x, unit._y):
        range.append((enemy._x - 1, enemy._y))
    if check_position(enemy._x, enemy._y - 1, d_units, _map) or (enemy._x, enemy._y - 1) == (unit._x, unit._y):
        range.append((enemy._x, enemy._y - 1))
    if check_position(enemy._x, enemy._y + 1, d_units, _map) or (enemy._x, enemy._y + 1) == (unit._x, unit._y):
        range.append((enemy._x, enemy._y + 1))
    if check_position(enemy._x + 1, enemy._y, d_units, _map) or (enemy._x + 1, enemy._y) == (unit._x, unit._y):
        range.append((enemy._x + 1, enemy._y))

    nearest = - 1
    minimum_steps = sys.maxsize
    direction = ''
    for i, el in enumerate(range):
        if unit._x == el[0] and unit._y == el[1]:
            return 0
        steps_up = steps_to_reach(unit._x - 1, unit._y, el, _map, d_units, list(), 0)
        if minimum_steps > steps_up > - 1:
            minimum_steps = steps_up
            direction = 'up'
            nearest = i
        steps_left = steps_to_reach(unit._x, unit._y - 1, el, _map, d_units, list(), 0)
        if minimum_steps > steps_left > - 1:
            minimum_steps = steps_left
            direction = 'left'
            nearest = i
        steps_right = steps_to_reach(unit._x, unit._y + 1, el, _map, d_units, list(), 0)
        if minimum_steps > steps_right > - 1:
            minimum_steps = steps_right
            direction = 'right'
            nearest = i
        steps_down = steps_to_reach(unit._x + 1, unit._y, el, _map, d_units, list(), 0)
        if minimum_steps > steps_down > - 1:
            minimum_steps = steps_down
            direction = 'down'
            nearest = i
    if not move:
        return minimum_steps

    if direction == 'up':
        unit._x -= 1
    if direction == 'down':
        unit._x += 1
    if direction == 'left':
        unit._y -= 1
    if direction == 'right':
        unit._y += 1


def attack_enemy(unit, enemy):
    if unit.life > 0:
        enemy.life -= 3

def calculate_enemy_cost(unit, enemy, _map, units):
    d_units = {(unit._x, unit._y): unit.life for unit in units}
    graph = create_graph_from_map(_map, d_units, unit)
    came_from, cost_so_far = a_star_search(graph, (unit._x, unit._y), (enemy._x, enemy._y))

    destinations = list(graph.neighbors((enemy._x, enemy._y)))
    costs = [value for key, value in cost_so_far.items() if key in destinations]
    if len(costs) == 0:
        return -1
    return min(costs)


def move_to_enemy(unit, enemy, _map, units):
    d_units = {(unit._x, unit._y): unit.life for unit in units}
    graph = create_graph_from_map(_map, d_units, unit)
    came_from, cost_so_far = a_star_search(graph, (unit._x, unit._y), (enemy._x, enemy._y))

    destinations = list(graph.neighbors((enemy._x, enemy._y)))
    costs = {key: value for key, value in cost_so_far.items() if key in destinations}
    key_destination = next(iter(costs))
    _next = key_destination
    while came_from[_next] != (unit._x, unit._y):
        _next = came_from[_next]

    unit._x = _next[0]
    unit._y = _next[1]


def do_turn(unit, units, _map, counter):
    continue_battle = True
    enemies = find_enemies(unit, units)
    if len(enemies) == 0:
        continue_battle = False
        return continue_battle
    execute_action(enemies, unit, _map, units)

    # enemy_to_attack = - 1
    # near_distance = sys.maxsize
    # minimum_hp = sys.maxsize
    # for i, enemy in enumerate(enemies):
    #     steps = calculate_steps(unit, enemy, _map, units, False)
    #     if near_distance > steps > - 1:
    #         enemy_to_attack = i
    #         near_distance = steps
    #         minimum_hp = enemy.life
    #     if near_distance == steps and enemy.life < minimum_hp:
    #         enemy_to_attack = i
    #         minimum_hp = enemy.life
    # if near_distance > 0:
    #     calculate_steps(unit, enemies[enemy_to_attack], _map, units, True)
    #     near_distance -= 1
    #
    # if near_distance == 0:
    #     attack_enemy(unit, enemies[enemy_to_attack])

    os.system('clear')
    print('Round ' + str(counter))
    print_map(_map, units)

    return continue_battle


def do_it(_input):
    _map = list()
    units = list()
    for i, line in enumerate(_input):
        _map.append(list())
        for j, x in enumerate(line):
            if x == '#':
                _map[i].append('#')
            else:
                _map[i].append('.')
            if x == 'G':
                units.append(Unit('G', i, j))
            if x == 'E':
                units.append(Unit('E', i, j))

    continue_battle = True
    counter = 0
    while True:
        units.sort(key=operator.attrgetter('_x', '_y'))
        os.system('clear')
        print('Round ' + str(counter))
        print_map(_map, units)

        for unit in units:
            continue_battle = do_turn(unit, units, _map, counter)
            if not continue_battle:
                break
        units = [x for x in units if x.life > 0]
        if not continue_battle:
            break
        counter += 1
    result = sum([x.life for x in units]) * counter
    print('Final ')
    print_map(_map, units)

    print('Part One', result)
    return result


if __name__ == '__main__':
    print('day 15')
    # print('#Test Set')

    # file = open("test_input_custom.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 27730

    # file = open("test_input.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 27730
    #
    # file = open("test_input_2.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 36334
    # file = open("test_input_3.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 39514
    # file = open("test_input_4.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 27755
    # file = open("test_input_5.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 28944
    # file = open("test_input_6.txt", 'r')
    # _test_input = file.read().split('\n')
    # assert do_it(_test_input) == 18740
    #
    # file = open("round_29.txt", 'r')
    # _input = file.read().split('\n')
    # print("#Solutions")
    # print(do_it(_input))


    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
    print('incorrect answers: 194040 ')