#!/bin/python3

import math
import os
import random
import re
import sys
import operator


def calculate_checksum(input):
    exactly_twice = 0
    exactly_trice = 0
    for i in input:
        map_letter = {}
        for c in i:
            if c in map_letter:
                map_letter[c] += 1
            else:
                map_letter[c] = 1
        exactly_twice += 1 if 2 in map_letter.values() else 0
        exactly_trice += 1 if 3 in map_letter.values() else 0
    print(exactly_twice, exactly_trice)
    print(exactly_twice * exactly_trice)


def find_correct_id(input):
    ids = set()

    for i in input:
        for id in ids:
            diff = 0
            for index in range(len(i)):
                if diff > 1:
                    break
                if id[index] != i[index]:
                    diff += 1
            if diff == 1:
                box1 = id
                box2 = i
                print(box1, box2)

        ids.add(i)
    x = ''.join(box1[_i] for _i in range(len(box1)) if box1[_i] == box2[_i])
    print(x)


if __name__ == '__main__':
    print("Day 1: https://adventofcode.com/2018/day/1")

    file = open("test_input.txt", 'r')
    input = file.read().split('\n')
    # Test Part One
    calculate_checksum(input)

    file = open("input.txt", 'r')
    input = file.read().split('\n')
    # Part One
    calculate_checksum(input)

    file = open("test_input_part_2.txt", 'r')
    test_input = file.read().split('\n')
    # Test Part Two
    find_correct_id(test_input)

    # Part Two
    find_correct_id(input)
