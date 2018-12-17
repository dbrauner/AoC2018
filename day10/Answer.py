import sys


def do_it(data):
    points = list()

    for i in data:
        s = i.replace(' ', '').replace('<', ' ').replace('>', ' ').replace(',', ' ').split(' ')
        p = [int(s[1]), int(s[2])]
        v = [int(s[4]), int(s[5])]
        points.append([p, v])
    counter = 0
    while True:
    # for index in range(500):
        counter += 1
        min_x = sys.maxsize
        max_x = 0
        min_y = sys.maxsize
        max_y = 0

        for item in points:
            if item[0][0] > max_y:
                max_y = item[0][0]
            if item[0][0] < min_y:
                min_y = item[0][0]

            if item[0][1] > max_x:
                max_x = item[0][1]
            if item[0][1] < min_x:
                min_x = item[0][1]
        if max_x - min_x > 100 or max_y - min_y > 100:
            for item in points:
                item[0][0] += item[1][0]
                item[0][1] += item[1][1]
            # print('skip')
            continue
        x = [item[0] for item in points]
        for i in range(min_x, max_x + 1):
            s = ''
            for j in range(min_y, max_y + 1):
                if [j, i] in x:
                    s += '#'
                else:
                    s += '.'
            print(s)
        print(counter)
        print('Then')
        for item in points:
            item[0][0] += item[1][0]
            item[0][1] += item[1][1]


if __name__ == '__main__':
    print("Day 5: https://adventofcode.com/2018/day/5")

    # file = open("test_input.txt", 'r')

    # _test_input = file.read().split('\n')

    # print('#Test Set')
    # print(do_it(_test_input))

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
