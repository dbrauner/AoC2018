import sys


def create_ground_map(clays, max_x, max_y):
    ground = list()
    for i in range(max_y + 1):
        ground.append(list())
        for j in range(max_x + 1):
            key = (j,i)
            if key in clays:
                ground[i].append('#')
            else:
                ground[i].append('.')
    return ground


def print_ground(ground, min_x, max_x, min_y, max_y):
    for i in range(min_y, max_y + 1):
        s = ''.join(ground[i][min_x:max_x + 1])
        # for j in range(min_y, max_y):
        #     s += ground[i][j]
        print(s)


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
                max_y =int(data[4])
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
                max_y =int(data[1])
            if int(data[1]) < min_y:
                min_y = int(data[1])
            for i in range(int(data[3]), int(data[4]) + 1):
                clays[(i, int(data[1]))] = '#'

    ground = create_ground_map(clays, max_x, max_y)
    print_ground(ground, min_x, max_x, min_y, max_y)
    pass

if __name__ == '__main__':
    print('day 17')

    file = open("test_input.txt", 'r')
    _test_input = file.read().split('\n')
    print("#Test Set")
    do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    do_it(_input)
