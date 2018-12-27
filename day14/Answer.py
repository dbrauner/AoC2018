from collections import deque


def calculate_pos(i, length):
    pass


def do_it(input):
    recipes = deque([3, 7])

    elf_one = 0
    elf_two = 1
    while True:
        combined = recipes[elf_one] + recipes[elf_two]
        if combined > 9:
            recipes.append(int(str(combined)[0:1]))
            recipes.append(int(str(combined)[1:2]))
        else:
            recipes.append(combined)

        step = elf_one + recipes[elf_one] + 1
        if step >= len(recipes):
            offset = step % len(recipes)
            elf_one = offset
        else:
            elf_one = step

        step = elf_two + recipes[elf_two] + 1
        if step >= len(recipes):
            offset = step % len(recipes)
            elf_two = offset
        else:
            elf_two = step

        # for _i in range(len(recipes)):
        #     if _i == elf_one:
        #         print('-', end='')
        #     elif _i == elf_two:
        #         print('+', end='')
        #     else:
        #         print(' ', end='')
        #     print(recipes[_i], end='')
        # print('')

        if len(recipes) > 10 + input:
            result = ''
            for _i in range(input, input + 10):
                result += str(recipes[_i])
            # return ''.join(recipes[input:input + 10])
            return result


def part_two(input):
    recipes = deque([3, 7])

    elf_one = 0
    elf_two = 1
    count = 0
    index = 0
    while True:
        count += 1
        combined = recipes[elf_one] + recipes[elf_two]
        if combined > 9:
            recipes.append(int(str(combined)[0:1]))
            if str(combined)[0] == input[index]:
                index += 1
            else:
                index = 0
                if str(combined)[0] == input[index]:
                    index += 1
            if index == len(input):
                return len(recipes) - index
            recipes.append(int(str(combined)[1:2]))
            if str(combined)[1] == input[index]:
                index += 1
            else:
                index = 0
                if str(combined)[1] == input[index]:
                    index += 1
            if index == len(input):
                return len(recipes) - index
        else:
            recipes.append(combined)
            if str(combined) == input[index]:
                index += 1
            else:
                index = 0
                if str(combined) == input[index]:
                    index += 1

            if index == len(input):
                return len(recipes) - index

        step = elf_one + recipes[elf_one] + 1
        if step >= len(recipes):
            offset = step % len(recipes)
            elf_one = offset
        else:
            elf_one = step

        step = elf_two + recipes[elf_two] + 1
        if step >= len(recipes):
            offset = step % len(recipes)
            elf_two = offset
        else:
            elf_two = step

        # result = ''
        # if len(recipes) > 2 * len(input):
        #     for _i in range(len(recipes) - 2 * len(input), len(recipes)):
        #         result += str(recipes[_i])
        #     if input in result:
        #         result = ''
        #         for _i in range(len(recipes)):
        #             result += str(recipes[_i])
        #         return result.index(input)

def part_two_two(recipes):
        score = '37'
        elf1 = 0
        elf2 = 1
        while recipes not in score[-7:]:
            score += str(int(score[elf1]) + int(score[elf2]))
            elf1 = (elf1 + int(score[elf1]) + 1) % len(score)
            elf2 = (elf2 + int(score[elf2]) + 1) % len(score)

        print('Part 1:', score[int(recipes):int(recipes) + 10])
        print('Part 2:', score.index(recipes))


if __name__ == '__main__':
    print("Day 14: https://adventofcode.com/2018/day/14")

    print('#Test Set')

    print(do_it(9))
    print(do_it(5))
    print(do_it(18))
    print(do_it(2018))

    print(do_it(84601))

    print(part_two('51589'))
    print(part_two('01245'))
    print(part_two('92510'))
    print(part_two('59414'))
    print(part_two('084601'))