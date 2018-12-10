import sys

from collections import deque, defaultdict

def play_game(max_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values()) if scores else 0

def circular_players(n):
    while True:
        for i in range(1, n + 1):
            yield i


def do_it(players, marbles):
    circle = [0]
    score = {}
    current = 0
    current_player = circular_players(players)
    for i in range(1, marbles):
        p = current_player.__next__()

        m23 = i % 23 == 0
        if m23:
            if p in score:
                score[p] += i
            else:
                score[p] = i
            r = (circle.index(current) - 7) % len(circle)
            v = circle[r]
            circle.remove(v)
            score[p] += v
            current = circle[r]
            continue
        a = (circle.index(current) + 1) % len(circle)
        b = (circle.index(current) + 2) % len(circle)
        if a > b:
            circle = circle[b:a + 1] + [i]
        if b > a:
            circle = circle[0:a + 1] + [i] + circle[b:]
        if b == a:
            circle = circle[a:] + [i]

        current = i
        # print(p, circle)

    print('winner: ', max(score.values()))


if __name__ == '__main__':
    print("Day 9: https://adventofcode.com/2018/day/9")

    test_set = (9, 250)

    print(play_game(477, 7085100))

    do_it(test_set[0], test_set[1])

    test_set = (10, 16180)

    do_it(test_set[0], test_set[1])
    test_set = (13, 7999)

    do_it(test_set[0], test_set[1])

    test_set = (17, 1104)
    do_it(test_set[0], test_set[1])

    test_set = (21, 6111)
    do_it(test_set[0], test_set[1])

    test_set = (477, 70851)
    do_it(test_set[0], test_set[1])

