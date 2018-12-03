def calculate_overlap(data):
    checked = {}
    overlap = set()
    claimed = set()
    for line in data:
        id, _at, position, size = line.split(' ')
        id = id[1:]
        x, y = map(int, position.replace(':', '').split(','))
        width, height = map(int, size.split('x'))

        for _i in range(x, x + width):
            for _j in range(y, y + height):
                if (_i, _j) in checked:
                    overlap.add((_i, _j))
                    claimed.add(checked[(_i, _j)])
                    checked[(_i, _j)] = id
                    claimed.add(id)
                else:
                    checked[(_i, _j)] = id
        # print(' overlap ', overlap)
        # print('checked', checked)
    for i in range(1341):
        if str(i) not in claimed:
            print("uniq", i)
    ids = set(checked.values())
    # print(ids)
    sym = ids ^ claimed
    # print(sym)
    # print(len(sym))
    # print(checked.values())
    # print(claimed)
    # print(len(overlap))


if __name__ == '__main__':
    print("Day 3: https://adventofcode.com/2018/day/3")

    _test_input = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
    # Test Part One
    calculate_overlap(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Part One")
    calculate_overlap(_input)
