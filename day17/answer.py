import os
import pygame
import sys
from collections import deque


class Queue:
    def __init__(self):
        self.elements = deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.pop()


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.came_from = {}

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls and id not in self.came_from

    def sides(self, id):
        (x, y) = id
        results = [(x - 1, y), (x + 1, y)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def neighbors(self, id, water_at_rest):
        (x, y) = id
        if self.passable((x, y + 1)):
            results = [(x, y + 1)]
            results = filter(self.in_bounds, results)
            return results
        if (x, y + 1) in self.walls or (x, y + 1) in water_at_rest:
            results = [(x - 1, y), (x + 1, y)]
            results = filter(self.in_bounds, results)
            results = filter(self.passable, results)
            return results
        return []


def create_ground_map(clays, max_x, max_y):
    ground = list()
    for i in range(max_y + 1):
        ground.append(list())
        for j in range(max_x + 1):
            key = (j, i)
            if key in clays:
                ground[i].append('#')
            else:
                ground[i].append('.')
    return ground


def print_ground(ground, min_x, max_x, min_y, max_y, water_at_rest, came_from):
    os.system('cls')
    print('water state')
    for i in range(min_y, max_y + 1):
        s = ''
        # s = ''.join(ground[i][min_x:max_x + 1])
        for j in range(min_x, max_x + 1):
            if (j, i) in water_at_rest:
                s += '~'
            elif (j, i) in came_from:
                s += '|'
            else:
                s += ground[i][j]
        print(s)


def calculate_volume(ground, clays, min_y, max_y, min_x, max_x):
    # pygame.init()

    size = width, height = max_x, max_y

    white = 255, 255, 255

    # screen = pygame.display.set_mode(size, 0, 8)
    while 1:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT: sys.exit()

        grid = SquareGrid(len(ground[0]), len(ground))
        grid.walls = set(clays)
        start = (500, 0)
        frontier = Queue()
        frontier.put(start)
        came_from = {}
        came_from[start] = None
        grid.came_from = came_from
        water_at_rest = {}

        while not frontier.empty():
            current = frontier.get()
            if current[1] + 1 > max_y:
                continue
            sides = list(grid.sides(current))
            down_next = (current[0], current[1] + 1)
            if (down_next in water_at_rest or grid.passable(down_next)) and len(sides) > 0:
                frontier.put(current)
            for next in grid.neighbors(current, water_at_rest):
                if next not in came_from:
                    frontier.put(next)
                    came_from[next] = current

            left_wall = None
            right_wall = None

            for i in reversed(range(0, current[0])):
                if (i, current[1]) in grid.walls:
                    left_wall = i
                    break
            for i in range(current[0], grid.width):
                if (i, current[1]) in grid.walls:
                    right_wall = i
                    break
            if current not in water_at_rest and left_wall is not None and right_wall is not None:
                all_there = True
                for i in range(left_wall + 1, right_wall):
                    if (i, current[1]) not in came_from:
                        all_there = False
                        break
                if all_there:
                    for i in range(left_wall + 1, right_wall):
                        water_at_rest[(i, current[1])] = True
            # screen.fill(white)

            # print_ground(ground, min_x, max_x, min_y, max_y, water_at_rest, came_from)

            # for i in grid.walls:
            #     screen.set_at(i, (0, 0, 0))
            # for i in came_from:
            #     screen.set_at(i, (0, 0, 255))
            # for i in water_at_rest:
            #     screen.set_at(i, (255, 0, 255))
            #
            # pygame.display.update()

        tiles_with_water = 0
        for e in came_from:
            if e[1] >= min_y and e[1] <= max_y:
                tiles_with_water += 1
        tiles_at_rest = len(water_at_rest)
        return tiles_with_water, tiles_at_rest


def do_it(input):
    clays = {}
    min_y = sys.maxsize
    max_y = 0
    max_x = 0
    min_x = sys.maxsize
    for line in input:
        data = line.replace(' ', '').replace('=', ' ').replace('..', ' ').replace(',', ' ').split(' ')
        if line[0] == 'x':
            if int(data[1]) > max_x:
                max_x = int(data[1])
            if int(data[1]) < min_x:
                min_x = int(data[1])
            if int(data[4]) > max_y:
                max_y = int(data[4])
            if int(data[3]) < min_y:
                min_y = int(data[3])
            for i in range(int(data[3]), int(data[4]) + 1):
                clays[(int(data[1]), i)] = '#'
        else:
            if int(data[4]) > max_x:
                max_x = int(data[4])
            if int(data[3]) < min_x:
                min_x = int(data[3])
            if int(data[1]) > max_y:
                max_y = int(data[1])
            if int(data[1]) < min_y:
                min_y = int(data[1])
            for i in range(int(data[3]), int(data[4]) + 1):
                clays[(i, int(data[1]))] = '#'

    ground = create_ground_map(clays, max_x, max_y)
    # print_ground(ground, min_x, max_x, min_y, max_y, [], [])

    water_volume, tiles_at_rest = calculate_volume(ground, clays, min_y, max_y, min_x, max_x)
    print('Part One: ', water_volume)
    print('Part Two: ', tiles_at_rest)
    pass


if __name__ == '__main__':
    print('day 17')

    # file = open("test_input.txt", 'r')
    # _test_input = file.read().split('\n')
    # print("#Test Set")
    # do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    do_it(_input)
