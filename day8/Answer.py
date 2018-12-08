import sys


class Node:
    def __init__(self, q_nodes, q_metada, childs, metadata):
        self.q_nodes = q_nodes
        self.q_metadata = q_metada
        self.childs = childs
        self.metadata = metadata


def get_next(tree):
    for i in tree:
        yield i


def process_tree(f_tree, nodes, attr, node):
    metadata = 0
    node_list = list()
    for i in range(nodes):
        _nodes = f_tree.__next__()
        _attr = f_tree.__next__()
        n = Node(_nodes, _attr, None, None)
        metadata += process_tree(f_tree, _nodes, _attr, n)
        node_list.append(n)
    metadata_list = list()
    for j in range(attr):
        x = f_tree.__next__()
        metadata += x
        metadata_list.append(x)
    node.metadata = metadata_list
    node.childs = node_list
    return metadata


def part_two(node):
    value = 0
    if node.q_nodes == 0:
        return sum(node.metadata)

    for i in range(node.q_metadata):
        if node.q_nodes >= node.metadata[i]:
            value += part_two(node.childs[node.metadata[i] - 1])
    return value


def do_it(data):
    tree = tuple(map(int, data.split(' ')))
    f_tree = get_next(tree)
    nodes = f_tree.__next__()
    attr = f_tree.__next__()

    root = Node(nodes, attr, None, None)

    metadata = process_tree(f_tree, nodes, attr, root)
    print('Part One', metadata)

    m2 = part_two(root)
    print('Part Two', m2)


if __name__ == '__main__':
    print("Day 8: https://adventofcode.com/2018/day/8")

    _test_input = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'

    print('#Test Set')
    do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')[0]
    print("#Solutions")
    do_it(_input)
