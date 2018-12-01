#!/bin/python3

import math
import os
import random
import re
import sys
import operator


def process_lines(arr, total):
    for line in arr:
        if line[0] == '+':
            total += int(line[1:])
        else:
            total -= int(line[1:])
        yield total


def detect_frequency(arr):
    total = 0

    _func = process_lines(arr, total)

    for i in _func:
        total = i
    return total


def detected_twice(arr):
    already_seen = set()
    total = 0
    while True:
        _func = process_lines(arr, total)

        for i in _func:
            total = i
            if total in already_seen:
                return total
            already_seen.add(total)


if __name__ == '__main__':
    print("Day 1: https://adventofcode.com/2018/day/1")
    file = open("input.txt", 'r')

    input = file.read().split('\n')

    # Part One
    print(detect_frequency(input))

    test_input = ["+7", "+7", "-2", "-7", "-4"]
    print(detected_twice(test_input))

    # Part Two
    print(detected_twice(input))
