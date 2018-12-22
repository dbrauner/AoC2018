import sys


def find_closer(coord, i, j):
    for k in range(len(coord)):
        yield abs(i - coord[k][0]) + abs(j - coord[k][1])


def do_it(data):
    coord = list()
    max_x = 0
    max_y = 0
    lines = [l.split() for l in data]
    r =
    r = ((x, y) for i in data i.split(' '))
    for _i in range(len(data)):
        xy = list(map(int, str(data[_i]).replace(',', '').split(' ')))
        coord.append(xy)
        if xy[0] > max_x:
            max_x = xy[0]
        if xy[1] > max_y:
            max_y = xy[1]
    closest = {}
    region = 0
    for _i in range(max_x):
        for _j in range(max_y):
            distance = sys.maxsize
            closer = -1
            total_distance = 0
            f_closer = find_closer(coord, _i, _j)
            for index, item in enumerate(f_closer):
                if item == distance:
                    closer = -1
                if item < distance:
                    distance = item
                    closer = index
                total_distance += item

            if total_distance < 10000:
                region += 1
            if closer >= 0:
                if closer in closest:
                    closest[closer] += 1
                else:
                    closest[closer] = 1

    for i in range(max_y):
        distance = sys.maxsize
        closer = -1
        f_closer = find_closer(coord, i, -1)
        for index, item in enumerate(f_closer):
            if item == distance:
                closer = -1
            if item < distance:
                distance = item
                closer = index
        if closer >= 0 and closer in closest:
            del closest[closer]

    for i in range(max_y):
        distance = sys.maxsize
        closer = -1
        f_closer = find_closer(coord, i, max_y + 1)
        for index, item in enumerate(f_closer):
            if item == distance:
                closer = -1
            if item < distance:
                distance = item
                closer = index
        if closer >= 0 and closer in closest:
            del closest[closer]

    for i in range(max_x):
        distance = sys.maxsize
        closer = -1
        f_closer = find_closer(coord, -1, i)
        for index, item in enumerate(f_closer):
            if item == distance:
                closer = -1
            if item < distance:
                distance = item
                closer = index
        if closer >= 0 and closer in closest:
            del closest[closer]

    for i in range(max_y):
        distance = sys.maxsize
        closer = -1
        f_closer = find_closer(coord, max_y + 1, -1)
        for index, item in enumerate(f_closer):
            if item == distance:
                closer = -1
            if item < distance:
                distance = item
                closer = index
        if closer >= 0 and closer in closest:
            del closest[closer]

    print('#Part One', max(closest.values()))
    print('#Part Two', region)


if __name__ == '__main__':
    print("Day 5: https://adventofcode.com/2018/day/5")

    file = open("test_input.txt", 'r')

    _test_input = file.read().split('\n')

    print('#Test Set')
    print(do_it(_test_input))

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
