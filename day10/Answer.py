import sys


def do_it(data):
    points = list()
    max_x, max_y = 0, 0
    min_x, min_y = sys.maxsize, sys.maxsize
    for i in data:
        line = i.replace(' ', '').replace('<', ' ').replace('>', ' ').replace(',', ' ').split(' ')
        p = int(line[1]), int(line[2])
        v = int(line[4]), int(line[5])
        p = list(p)
        v = list(v)
        print(p, v)
        if max_x < p[0]:
            max_x = p[0]
        if max_y < p[1]:
            max_y = p[1]
        if p[0] < min_x:
            min_x = p[0]
        if p[1] < min_y:
            min_y = p[1]
        points.append([p, v])

    # w, h = 8, 5
    for index in range(10000):
        display = [['.' for x in range(max_x - (min_x) + 1)] for y in range(max_y - (min_y) + 1)]

        for i in points:
            x, y = i[0][0] - min_x, i[0][1] - min_y
            if x > 0 and y > 0:
                display[y][x] = '#'
            i[0][0] += i[1][0]
            i[0][1] += i[1][1]


        for i in range(len(display)):
            s = ''
            for j in range(len(display[i])):
                if display[i][j] == '#':
                    s += '#'
                else:
                    s += '.'
            print(s)
        print('Then')

if __name__ == '__main__':
    print("Day 10: https://adventofcode.com/2018/day/10")

    file = open("test_input.txt", 'r')

    _test_input = file.read().split('\n')
    print('#Test Set')
    # do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    do_it(_input)

