import os
import operator

def do_it(data):
    # os.system('cls')  # on windows

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

        if len(carts) == 1:
            print('Part Two', carts[0][0], carts[0][1])
            break
        # carts.sort()
        carts.sort(key=operator.itemgetter(0, 1))

        # carts_pos = [[cart[0], cart[1]] for cart in carts]
        # for i in range(len(tracks)):
        #     line = ''
        #     for j in range(len(tracks[i])):
        #         pos = [i, j]
        #         if pos in carts_pos:
        #             for cart in carts:
        #                 if [cart[0], cart[1]] == [i, j]:
        #                     line += cart[2]
        #         else:
        #             line += tracks[i][j]
        #     print(line)
        # print('next')

        remove_list = set()

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
            colision_set = set()
            remove = list()
            for xcart in carts:
                if (xcart[0], xcart[1]) in colision_set:
                    print('Part One', (xcart[0], xcart[1]))
                    # not_colided = False
                    remove.append((xcart[0], xcart[1]))
                colision_set.add((xcart[0], xcart[1]))

            if len(remove) > 0:
                for _i in range(len(carts)):
                    if (carts[_i][0], carts[_i][1]) in remove:
                        remove_list.add(_i)
                # print('before', carts)
                # carts[:] = (value for value in carts if (value[0], value[1]) not in remove)
                # print('after', carts)
        if len(remove_list) > 0:
            offset = 0
            for _j in remove_list:
                del carts[_j - offset]
                offset += 1


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
