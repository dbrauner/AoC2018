def addr(before, instruction):
    c = before[instruction[1]] + before[instruction[2]]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_addr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before, instruction, after = e
    r = addr(before, instruction)
    return r == after


def addi(before, instruction):
    c = before[instruction[1]] + instruction[2]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_addi(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = addi(before, instruction)
    return r == after


def mulr(before, instruction):
    c = before[instruction[1]] * before[instruction[2]]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_mulr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before, instruction, after = e
    r = mulr(before, instruction)
    return r == after


def muli(before, instruction):
    c = before[instruction[1]] * instruction[2]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_muli(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = muli(before, instruction)
    return r == after


def banr(before, instruction):
    c = before[instruction[1]] & before[instruction[2]]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_banr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before, instruction, after = e
    r = banr(before, instruction)
    return r == after


def bani(before, instruction):
    c = before[instruction[1]] & instruction[2]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_bani(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = bani(before, instruction)
    return r == after


def borr(before, instruction):
    c = before[instruction[1]] | before[instruction[2]]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_borr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before, instruction, after = e
    r = borr(before, instruction)
    return r == after


def bori(before, instruction):
    c = before[instruction[1]] | instruction[2]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_bori(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = bori(before, instruction)
    return r == after


def setr(before, instruction):
    c = before[instruction[1]]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_setr(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = setr(before, instruction)
    return r == after


def seti(before, instruction):
    c = instruction[1]
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_seti(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = seti(before, instruction)
    return r == after


def gtrr(before, instruction):
    c = 1 if before[instruction[1]] > before[instruction[2]] else 0
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_gtrr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before, instruction, after = e
    r = gtrr(before, instruction)
    return r == after


def gtri(before, instruction):
    c = 1 if before[instruction[1]] > instruction[2] else 0
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_gtri(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = gtri(before, instruction)
    return r == after


def gtir(before, instruction):
    c = 1 if instruction[1] > before[instruction[2]] else 0
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_gtir(e):
    if e[1][2] > 3:
        return False
    before, instruction, after = e
    r = gtir(before, instruction)
    return r == after


def eqrr(before, instruction):
    c = 1 if before[instruction[1]] == before[instruction[2]] else 0
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_eqrr(e):
    if e[1][1] > 3 or e[1][2] > 3:
        return False
    before, instruction, after = e
    r = eqrr(before, instruction)
    return r == after


def eqri(before, instruction):
    c = 1 if before[instruction[1]] == instruction[2] else 0
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_eqri(e):
    if e[1][1] > 3:
        return False
    before, instruction, after = e
    r = eqri(before, instruction)
    return r == after


def eqir(before, instruction):
    c = 1 if instruction[1] == before[instruction[2]] else 0
    r = before.copy()
    r[instruction[3]] = c
    return r


def is_eqir(e):
    if e[1][2] > 3:
        return False
    before, instruction, after = e
    r = eqir(before, instruction)
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


def execute_instruction(opcode_list, instruction, registers):
    f = opcode_list[instruction[0]][0][3:]  # addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtrr, gtri, gtir, eqrr, eqri, eqir
    return globals()[f](registers, instruction)


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
    for _ in funs:
        opcode_list.append(funs.copy())

    for e in executions:
        opcodes = determine_opcodes(e, opcode_list, funs)
        if opcodes >= 3:
            behave_3_more_opcodes += 1
        print(e)
    print('# Part One ', behave_3_more_opcodes)

    removed = set()
    while len(removed) < len(opcode_list):
        for i, op in enumerate(opcode_list):
            if len(op) == 1 and opcode_list[i][0] not in removed:
                removed.add(opcode_list[i][0])

                for j in range(len(opcode_list)):
                    if i != j and op[0] in opcode_list[j]:
                        opcode_list[j].remove(op[0])

    registers = [0, 0, 0, 0]

    next(input)  # Skip blank line
    line = next(input, None)

    while line is not None:
        instruction = list(map(int, str(line).split(' ')))
        registers = execute_instruction(opcode_list, instruction, registers)
        line = next(input, None)

    print(registers)
    return behave_3_more_opcodes


if __name__ == '__main__':
    print('day 16')

    file = open("input.txt", 'r')
    _input = file.read().split('\n')
    print("#Solutions")
    do_it(_input)
