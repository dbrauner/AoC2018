import sys
import collections


def do_it(data):
    state = data[0][15:]

    keys = dict()
    for i in range(2, len(data)):
        key, _for, pot = data[i].split(' ')
        keys[key] = pot
    plants = 0

    d = list(state)
    offset = 0
    disposition = set()
    # Answer for part one is the range of 20
    for index in range(10000):
        d_next = list()
        if d[0] == '#':
            d.insert(0, '.')
            d.insert(0, '.')
            d.insert(0, '.')
            offset += 3

        if d[len(d) - 1] == '#':
            d.append('.')
            d.append('.')
            d.append('.')

        for id in range(len(d)):
            if id == 0:
                comb = '..' + d[id] + d[id + 1] + d[id + 2]
            elif id == 1:
                comb = '.' + d[id - 1] + d[id] + d[id + 1] + d[id + 2]
            elif id == len(d) - 2:
                comb = d[id - 2] + d[id - 1] + d[id] + d[id + 1] + '.'
            elif id == len(d) - 1:
                comb = d[id - 2] + d[id - 1] + d[id] + '..'
            else:
                comb = d[id - 2] + d[id - 1] + d[id] + d[id + 1] + d[id + 2]
            if comb in keys:
                d_next.append(keys[comb])
            else:
                d_next.append('.')

        d = d_next
        str_d = ''.join(d)
        plants = 0
        for id in range(len(d)):
            if d[id] == '#':
                plants += id - offset
        # Answer for day two is 50kkk times the count + the difference for the plants value
        print(plants, str_d.count('#'))
    for id in range(len(d)):
        if d[id] == '#':
            plants += id - offset
    print(plants)
    pass


if __name__ == '__main__':
    print("Day 12: https://adventofcode.com/2018/day/12")
    file = open("test_input.txt", 'r')

    _test_input = file.read().split('\n')

    print('#Test Set')
    do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
