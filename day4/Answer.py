import datetime
import random
import collections


def do_it(data):
    schedule = {}
    f = "%Y-%m-%d %H:%M"
    for _i in data:
        date_string = _i[1:17]
        d = datetime.datetime.strptime(date_string, f)
        if '#' in _i:
            sub = _i[_i.index('#') + 1:]
            id = sub[:sub.index(' ')]
            id = int(id)
            schedule[date_string] = id
        if 'asleep' in _i:
            schedule[date_string] = 'asleep'
        if 'wakes up' in _i:
            schedule[date_string] = 'wakes up'
    # os = [k for k, v in sorted(schedule.items(), key=lambda p: p[1], reverse=True)]
    items = list(schedule.keys())
    # random.shuffle(items)
    items.sort()

    print(items)

    oschedule = collections.OrderedDict()
    for item in items:
        oschedule[item] = schedule[item]

    sleeping = {}
    sleeping_total = {}
    lastId = 0
    for _os in oschedule:
        if isinstance(oschedule[_os], int):
            lastId = oschedule[_os]
            continue
        if 'asleep' == oschedule[_os]:
            start = datetime.datetime.strptime(_os, f)
            continue
        if 'wakes up' == oschedule[_os]:
            end = datetime.datetime.strptime(_os, f)
            diff = end - start
            # print(diff)
            minutessince = int(diff.total_seconds() / 60)
            # print(minutessince)
            if lastId in sleeping_total:
                sleeping_total[lastId] += minutessince
            else:
                sleeping_total[lastId] = minutessince
            minute = datetime.timedelta(minutes=1)
            while start < end:
                # print(start)
                if (lastId, start.minute) in sleeping:
                    sleeping[(lastId, start.minute)] += 1
                else:
                    sleeping[(lastId, start.minute)] = 1
                start += minute
    max_sleep = 0
    id_sleep = 0
    for _i in sleeping_total:
        if sleeping_total[_i] > max_sleep:
            max_sleep = sleeping_total[_i]
            id_sleep = _i

    print(id_sleep)
    max_sleep = 0
    for _i in sleeping:
        if _i[0] == id_sleep and sleeping[_i] > max_sleep:
            max_sleep = sleeping[_i]
            max_time = int(_i[1]) * int(_i[0])
            print(max_time)

    # Part Two
    print('Part Two')
    for _i in sleeping:
        if sleeping[_i] > max_sleep:
            max_sleep = sleeping[_i]
            max_time = int(_i[1]) * int(_i[0])
            print(_i[1], _i[0], max_time)

    # oschedule = collections.OrderedDict(sorted(schedule.__iter__()))

    # dt = parse('Mon Feb 15 2010')
    # datetime.datetime(2010, 2, 15, 0, 0)
    # print(dt.strftime('%d/%m/%Y'))


if __name__ == '__main__':
    print("Day 3: https://adventofcode.com/2018/day/3")

    file = open("test_input.txt", 'r')

    _test_input = file.read().split('\n')
    # Test Part One
    do_it(_test_input)

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Part One")
    do_it(_input)
