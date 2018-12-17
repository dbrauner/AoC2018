import os


def do_it(data):
    os.system('cls')  # on windows

    carts = list()
    tracks = list()

    for i, v in enumerate(data):
        tracks.append(list())
        for j, x in enumerate(v):
            if x in ['>', '<', '^', 'v']:
                carts.append([i, j, x, 0])
                if x in ['>', '<']:
                    tracks[i].append('-')
                else:
                    tracks[i].append('|')
            else:
                tracks[i].append(x)
    not_colided = True
    while not_colided:

        colision_set = set()
        carts.sort()
        for cart in carts:
            if cart[2] == '>':
                _next = tracks[cart[0]][cart[1] + 1]
                cart[1] += 1
                if _next == '\\':
                    cart[2] = 'v'
                if _next == '/':
                    cart[2] = '^'
                if _next == '+':
                    if cart[3] == 0:
                        cart[2] = '^'
                    elif cart[3] == 2:
                        cart[2] = 'v'
                    cart[3] += 1
                    if cart[3] == 3:
                        cart[3] = 0
            elif cart[2] == '<':
                _next = tracks[cart[0]][cart[1] - 1]
                cart[1] -= 1
                if _next == '\\':
                    cart[2] = '^'
                if _next == '/':
                    cart[2] = 'v'
                if _next == '+':
                    if cart[3] == 0:
                        cart[2] = 'v'
                    elif cart[3] == 2:
                        cart[2] = '^'
                    cart[3] += 1
                    if cart[3] == 3:
                        cart[3] = 0
            elif cart[2] == '^':
                _next = tracks[cart[0] - 1][cart[1]]
                cart[0] -= 1
                if _next == '\\':
                    cart[2] = '<'
                if _next == '/':
                    cart[2] = '>'
                if _next == '+':
                    if cart[3] == 0:
                        cart[2] = '<'
                    elif cart[3] == 2:
                        cart[2] = '>'
                    cart[3] += 1
                    if cart[3] == 3:
                        cart[3] = 0
            elif cart[2] == 'v':
                _next = tracks[cart[0] + 1][cart[1]]
                cart[0] += 1
                if _next == '\\':
                    cart[2] = '>'
                if _next == '/':
                    cart[2] = '<'
                if _next == '+':
                    if cart[3] == 0:
                        cart[2] = '>'
                    elif cart[3] == 2:
                        cart[2] = '<'
                    cart[3] += 1
                    if cart[3] == 3:
                        cart[3] = 0

            if (cart[0], cart[1]) in colision_set:
                print((cart[0], cart[1]))
                not_colided = False
            colision_set.add((cart[0], cart[1]))

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
