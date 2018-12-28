import collections


def is_addr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] + before[instruction[2]]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_addi(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] + instruction[2]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_mulr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] * before[instruction[2]]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_muli(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] * instruction[2]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_banr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] & before[instruction[2]]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_bani(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] & instruction[2]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_borr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] | before[instruction[2]]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_bori(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]] | instruction[2]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_setr(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = before[instruction[1]]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_seti(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = instruction[1]
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_gtrr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = 1 if before[instruction[1]] > before[instruction[2]] else 0
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_gtri(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = 1 if before[instruction[1]] > instruction[2] else 0
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_gtir(e):
    if e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = 1 if instruction[1] > before[instruction[2]] else 0
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_eqrr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = 1 if before[instruction[1]] == before[instruction[2]] else 0
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_eqri(e):
    if e[1][1] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = 1 if before[instruction[1]] == instruction[2] else 0
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def is_eqir(e):
    if e[1][2] > 3:
        return False
    before = e[0]
    instruction = e[1]
    after = e[2]
    c = 1 if instruction[1] == before[instruction[2]] else 0
    r = after.copy()
    r[instruction[3]] = c
    return r == after


def determine_opcodes(e, opcode_list, funs):
    opcodes = 0
    for f in funs:
        if globals()[f](e):
            opcodes += 1
        elif f in opcode_list[e[1][0]]:
            opcode_list[e[1][0]].remove(f)
    return opcodes
def getKey(op):
    return len(op)


def execute_instruction(opcode_list, instruction):
    f = opcode_list[instruction[0]]
    return globals()[opcode_list[instruction[0]]()[2:]](instruction)


def do_it(input):
    input = iter(input)

    executions = []
    for line in input:
        if 'Before' not in line:
            break
        before = list(
            map(int, str(line)[9:].replace(' ', '').replace('[', ' ').replace(']', '').replace(',', ' ').split(' ')))
        line = next(input)
        instruction = list(map(int, str(line).split(' ')))
        line = next(input)
        after = list(
            map(int, str(line)[9:].replace(' ', '').replace('[', ' ').replace(']', '').replace(',', ' ').split(' ')))
        executions.append([before, instruction, after])
        next(input)
    behave_3_more_opcodes = 0
    funs = ['is_addr', 'is_addi', 'is_mulr', 'is_muli', 'is_banr', 'is_bani', 'is_borr', 'is_bori', 'is_setr',
            'is_seti', 'is_gtrr', 'is_gtri', 'is_gtir', 'is_eqrr', 'is_eqri', 'is_eqir']
    opcode_list = []
    for i, f in enumerate(funs):
        opcode_list.append(funs.copy())


    for e in executions:
        opcodes = determine_opcodes(e, opcode_list, funs)
        if opcodes >= 3:
            behave_3_more_opcodes += 1
        print(e)
    opcode_list.sort(key=getKey)
    x = 0
    removed = set()
    while len(removed) < len(opcode_list):
        for op in opcode_list:
            if len(op) == 1 and opcode_list[op][0] not in removed:
                removed.add(opcode_list[op][0])

                for i in range(len(opcode_list)):
                    if
        to_remove = opcode_list[x]
        x += 1
        for i in range(1, len(opcode_list)):
            opcode_list[i].remove(to_remove)

    registers = [0,0,0,0]
    line = next(input, None)

    while line is not None:
        line = next(input, None)
        instruction = list(map(int, str(line).split(' ')))
        registers = execute_instruction(opcode_list, instruction)

    return behave_3_more_opcodes


if __name__ == '__main__':
    print('day 16')

    test = ['Before: [3, 2, 1, 1]', '9 2 1 2', 'After:  [3, 2, 2, 1]', '']
    print('# Test')
    print(do_it(test))
    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    print(do_it(_input))
