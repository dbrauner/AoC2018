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


class Unit:
    def __init__(self, _class, _x, _y, power):
        self._x = _x
        self._y = _y
        self._class = _class
        self.life = 200
        self.power = power


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
            selected.clear()
            selected[location] = next_pos

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
    if target not in d_enemies:  # impossible to reach target
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


def attack_enemy(unit, enemy):
    if unit.life > 0:
        enemy.life -= unit.power


def do_turn(unit, units, _map, counter):
    continue_battle = True
    enemies = find_enemies(unit, units)
    if len(enemies) == 0:
        continue_battle = False
        return continue_battle
    execute_action(enemies, unit, _map, units)

    # os.system('clear')
    # print('Round ' + str(counter))
    # print_map(_map, units)

    return continue_battle


def create_map_and_units(_input, elf_power):
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
                units.append(Unit('G', i, j, 3))
            if x == 'E':
                units.append(Unit('E', i, j, elf_power))
    return _map, units


def do_it(_input):
    _map, units = create_map_and_units(_input, 3)
    continue_battle = True
    counter = 0
    while True:
        units.sort(key=operator.attrgetter('_x', '_y'))
        # os.system('clear')
        # print('Round ' + str(counter))
        # print_map(_map, units)

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

def do_part_two(_input):

    elf_power = 3
    while True:
        elf_power += 1
        print('Trying with elf power ' + str(elf_power))
        _map, units = create_map_and_units(_input, elf_power)
        continue_battle = True
        counter = 0
        elfs_died = False
        while True:
            units.sort(key=operator.attrgetter('_x', '_y'))
            # os.system('clear')
            # print('Round ' + str(counter))
            # print_map(_map, units)

            for unit in units:
                continue_battle = do_turn(unit, units, _map, counter)
                if not continue_battle:
                    break

            for x in units:
                if x.life <= 0 and x._class == 'E':
                    elfs_died = True
                    break
            units = [x for x in units if x.life > 0]
            if not continue_battle or elfs_died:
                break
            counter += 1
        if elfs_died:
            continue
        result = sum([x.life for x in units]) * counter
        print('Final ')
        print_map(_map, units)

        print('Part Two', result)
        return result


if __name__ == '__main__':
    print('day 15')
    # print('#Test Set')

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

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    # print(do_it(_input))
    print(do_part_two(_input))