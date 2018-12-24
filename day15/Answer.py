import operator
import os
import sys


class Unit:
    def __init__(self, _class, _x, _y):
        self._x = _x
        self._y = _y
        self._class = _class
        self.life = 200
        # self.cross_mod = 0
        # self.dead = False


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
            for unit in line_units:
                s += ' ' + unit._class + '(' + str(unit.life) + ')'
        print(s)


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

    next = steps_to_reach(x - 1, y, el, _map, units, visited, steps)
    if next > -1:
        # steps = next
        # if next > steps:
        return next
    next = steps_to_reach(x, y - 1, el, _map, units, visited, steps)
    if next > -1:
        steps = next
        # if next > steps:
        return next
    next = steps_to_reach(x, y + 1, el, _map, units, visited, steps)
    if next > -1:
        steps = next
        # if next > steps:
        return next
    next = steps_to_reach(x + 1, y, el, _map, units, visited, steps)
    if next > -1:
        steps = next
        # if next > steps:
        return next
    return -1


def calculate_steps(unit, enemy, _map, units, move):
    range = list()
    d_units = {(unit._x, unit._y): unit.life for unit in units}
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
    # pass


def do_turn(unit, units, _map):
    continue_battle = True
    enemies = find_enemies(unit, units)
    if len(enemies) == 0:
        continue_battle = False
        return continue_battle

    enemy_to_attack = - 1
    near_distance = sys.maxsize
    minimum_hp = sys.maxsize
    for i, enemy in enumerate(enemies):
        steps = calculate_steps(unit, enemy, _map, units, False)
        if near_distance > steps > - 1:
            enemy_to_attack = i
            near_distance = steps
            minimum_hp = enemy.life
        if near_distance == steps and enemy.life < minimum_hp:
            enemy_to_attack = i
            minimum_hp = enemy.life
    if near_distance > 0:
        calculate_steps(unit, enemies[enemy_to_attack], _map, units, True)
        near_distance -= 1

    if near_distance == 0:
        attack_enemy(unit, enemies[enemy_to_attack])

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
            continue_battle = do_turn(unit, units, _map)
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
    print('#Test Set')
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
    #


    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
