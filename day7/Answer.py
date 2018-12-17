import sys


def is_more():
    pass


def find_next(steps, first, ready):
    for i in steps:
        if i[1] == first and i[0] not in ready:
            return
    print(first)
    ready.add(first)
    for i in steps:
        if i[0] == first:
            find_next(steps, i[1], ready)


def do_it(_data):
    steps = []
    ready = set()
    for i in _data:
        _step, step, _must, _b, _fin, _before, _s, next_step, _can, _beg = i.split(' ')
        steps.append([step, next_step])
    steps.sort()

    for i in steps:
        found = False
        for j in steps:
            if i[0] == j[1]:
                found = True
        if found == False:
            first = i[0]
            break
    while first != '':

        print(first)
        ready.add(first)
        for i in steps:
            if i[0] == first and i[1] not in ready:
                find_next(steps, i[1], ready)
        first = ''
        for i in steps:
            found = False
            for j in steps:
                if i[0] == j[1] and j[0] not in ready:
                    found = True
            if not found and i[0] not in ready:
                first = i[0]
                print('next is ', first)
                break
    print('final length', len(ready))




if __name__ == '__main__':
    print("Day 5: https://adventofcode.com/2018/day/5")

    file = open("test_input.txt", 'r')

    _test_input = file.read().split('\n')

    print('#Test Set')
    # print(do_it(_test_input))

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
