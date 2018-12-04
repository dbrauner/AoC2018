import collections
import datetime


def do_it(data):
    schedule = {}
    f = "%Y-%m-%d %H:%M"
    for _i in data:
        date_string = _i[1:17]
        d = datetime.datetime.strptime(date_string, f)
        if '#' in _i:
            sub = _i[_i.index('#') + 1:]
            schedule[d] = int(sub[:sub.index(' ')])
        if 'asleep' in _i:
            schedule[d] = 'asleep'
        if 'wakes up' in _i:
            schedule[d] = 'wakes up'
    items = list(schedule.keys())
    items.sort()

    ordered_schedule = collections.OrderedDict()
    for item in items:
        ordered_schedule[item] = schedule[item]

    sleeping = {}
    sleeping_total = {}
    last_id = 0
    for _os in ordered_schedule:
        if isinstance(ordered_schedule[_os], int):
            last_id = ordered_schedule[_os]
            continue
        if 'asleep' == ordered_schedule[_os]:
            start = _os
            continue
        if 'wakes up' == ordered_schedule[_os]:
            end = _os
            diff = end - start
            minutes_since = int(diff.total_seconds() / 60)
            if last_id in sleeping_total:
                sleeping_total[last_id] += minutes_since
            else:
                sleeping_total[last_id] = minutes_since
            minute = datetime.timedelta(minutes=1)
            while start < end:
                if (last_id, start.minute) in sleeping:
                    sleeping[(last_id, start.minute)] += 1
                else:
                    sleeping[(last_id, start.minute)] = 1
                start += minute
    max_sleep = 0
    id_sleep = 0
    for _i in sleeping_total:
        if sleeping_total[_i] > max_sleep:
            max_sleep = sleeping_total[_i]
            id_sleep = _i

    max_sleep = 0
    for _i in sleeping:
        if _i[0] == id_sleep and sleeping[_i] > max_sleep:
            max_sleep = sleeping[_i]
            max_time = int(_i[1]) * int(_i[0])
    print('Part One', max_time)
    # Part Two
    for _i in sleeping:
        if sleeping[_i] > max_sleep:
            max_sleep = sleeping[_i]
            max_time = int(_i[1]) * int(_i[0])
    print('Part Two', max_time)


if __name__ == '__main__':
    print("Day 4: https://adventofcode.com/2018/day/4")

    file = open("test_input.txt", 'r')

    _test_input = file.read().split('\n')
    print('#Test Set')
    do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    do_it(_input)
