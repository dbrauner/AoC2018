import sys


def do_it(data):
    grids = [[0] * 300 for _ in range(300)]

    for x in range(1, 300):
        for y in range(1, 300):
            id = x + 10

            level = id * y
            level += data
            level *= id
            digits = str(level)
            if len(digits) > 2:
                digit = digits[len(digits) - 3]
            else:
                digit = 0
            result = int(digit) - 5
            grids[x][y] = result

    max_square = 0
    pos = [0, 0]

    # For Part 1, the size is fixed in 3 (remove first for-loop)
    for size in range(1, 300):
        for x in range(1, 300 - size):
            for y in range(1, 300 - size):
                square = 0
                for i in range(size):
                    for j in range(size):
                        square += grids[x + i][y + j]
                if square > max_square:
                    pos = [x, y]
                    max_square = square
        print(size, max_square, pos)
    print(max_square, pos)


if __name__ == '__main__':
    print("Day 11: https://adventofcode.com/2018/day/11")

    _test_input = 22

    print('#Test Set')
    do_it(18)
    do_it(42)

    print("#Solutions")
    do_it(8444)
