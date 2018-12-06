import sys
from string import ascii_lowercase


def part_two(data):
    min = sys.maxsize
    for c in ascii_lowercase:
        if c not in data:
            continue
        print(c)
        _data = ''
        for _c in data:
            if str(c).upper() != _c.upper():
                _data += _c
        result = do_it(_data)
        if result < min:
            min = result
    return min


def do_it(data):
    reacted = True

    while reacted:

        last = ''
        _data = ''
        for c in data:
            if last != c and str(c).upper() == last.upper():
                last = ''
            else:
                _data += last
                last = c
        _data += last
        if data == _data:
            reacted = False
        data = _data

    return len(_data)


if __name__ == '__main__':
    print("Day 5: https://adventofcode.com/2018/day/5")

    # file = open("test_input.txt", 'r')

    _test_input = "dabAcCaCBAcCcaDA"
    print('#Test Set')
    print(do_it(_test_input))

    file = open("input.txt", 'r')
    _input = file.read().split('\n')[0]
    print("#Solutions")
    print(do_it(_input))

    print(part_two(_test_input))
    print(part_two(_input))
