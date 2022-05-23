import sortedcontainers as s
import numpy as np


def multiply_matrices(a, b, n):
    ab = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if a[i][k] == 1 and b[k][j] == 1:
                    ab[i][j] = 1
                    break
    return ab


def insert_matrix(sets, n):
    for subset in sets:
        for subset1 in sets:
            sets.add(make_tuples(multiply_matrices(subset, subset1, n)))
    return sets


def make_tuples(matrix):
    return tuple(tuple(row) for row in matrix)


def task2():
    n = int(input('Введите количество элементов на множестве: '))
    st = [int(value) for value in input(f'Введите элементы порождающего множества ({n}): ').split()]
    m = int(input('"Введите количество матриц в порождающем множестве: '))

    in_matrices = s.SortedDict()
    out_matrices = s.SortedDict()
    sets = set()
    k = 0
    for i in range(0, m):
        print('Введите матрицу ', chr(65 + k))
        print(" ", *st)
        matrix = make_tuples([list(map(int, input(f"{st[i]} ").split())) for i in range(n)])
        sets.add(matrix)
        in_matrices[chr(65 + k)] = matrix
        k += 1
        out_matrices[matrix] = chr(65 + k)

    group = sets.copy()
    k_updated = 0
    while True:
        for value in sets:
            for value1 in sets:
                new_matrix = make_tuples(multiply_matrices(value, value1, n))
                if new_matrix not in group:
                    in_matrices[chr(65 + k + k_updated)] = new_matrix
                    k_updated += 1
                    out_matrices[new_matrix] = chr(65 + k + k_updated)
                    group.add(new_matrix)

        if group == sets:
            sets = insert_matrix(sets, n)
            print('Полученная полугруппа:')
            for subset in sets:
                print(chr(ord(out_matrices[subset]) - 1), ':')
                for i in range(len(subset)):
                    print(*subset[i])
                print('\n')
            print('Таблица Кэли: ')
            print(' ', *[chr(65 + i) for i in range(len(out_matrices))])
            for i in range(len(out_matrices)):
                print(chr(65 + i), end=' ')
                for j in range(len(out_matrices)):
                    print(chr(ord(out_matrices[make_tuples(multiply_matrices(in_matrices[chr(65 + i)],
                                                                             in_matrices[chr(65 + j)], n))]) - 1),
                          end=' ')
                print('\n')
            return
        else:
            sets = group.copy()


def check_associative(cayley, input_list):
    n = len(input_list)
    for a in range(n):
        for x in range(n):
            for z in range(n):
                if cayley[x, input_list.index(str(cayley[a, z]))] \
                        != cayley[input_list.index(str(cayley[x, a])), z]:
                    return False
    return True


def build_cayley():
    input_list = input('Введите элементы алфавита: ').split()
    n = int(input('Введите количество определяющих соотношений: '))
    rules = {}

    for i in range(n):
        print(f'Введите элементы {i + 1}-го соотношения:')
        elems = input().replace(" =", "").split()
        first_elem, second_elem = elems
        rules[first_elem] = second_elem

    semigroup = input_list.copy()
    while True:
        new_elems = []
        for elem_1 in semigroup:
            for elem_2 in semigroup:
                new_elem = elem_1 + elem_2
                while True:
                    new_elem_copy = str(new_elem)
                    for first_elem, second_elem in rules.items():
                        if first_elem in new_elem:
                            new_elem = new_elem.replace(first_elem, second_elem)
                    if new_elem_copy == new_elem:
                        break
                new_elems.append(new_elem)
        new_semigroup = set(semigroup.copy())
        for new_elem in new_elems:
            if new_elem not in semigroup:
                semigroup.append(new_elem)
        if new_semigroup == set(semigroup):
            break

    semigroup = list(semigroup)
    matrix = []
    for elem_1 in semigroup:
        matrix_string = []
        for elem_2 in semigroup:
            new_elem = elem_1 + elem_2
            while True:
                new_elem_copy = str(new_elem)
                for first_elem, second_elem in rules.items():
                    if first_elem in new_elem:
                        new_elem = new_elem.replace(first_elem, second_elem)
                if new_elem_copy == new_elem:
                    break
            matrix_string.append(new_elem)
        matrix.append(matrix_string)

    group_length = len(semigroup)
    matrix = np.array(matrix).reshape(group_length, group_length)
    print('Полугруппа: {', end='')
    print(*semigroup, sep=', ', end='')
    print('}')
    print('Таблица Кэли:')
    for i in range(len(matrix)):
        print(*matrix[i], sep='\t')


def build_sub_semigroup():
    input_list = input("Введите элементы множества: ").split()
    n = len(input_list)

    subset = input("Введите элементы подмножества: ").split()

    print("Введите значения таблицы Кэли множества, для которой будет строится подполугруппа: ")
    print(" ", *input_list)
    cayley = [list(map(str, input(f"{input_list[i]} ").split())) for i in range(n)]
    cayley_table = np.array(cayley).reshape(n, n)

    x_current = subset.copy()
    while True:
        x_l = []
        for x in x_current:
            for y in subset:
                x_l.append(cayley_table[input_list.index(x)][input_list.index(y)])
        previous_x = x_current.copy()
        x_current = list(set(x_current).union(set(x_l)))
        x_current.sort()
        if previous_x == x_current:
            break

    print("Подполугруппа: {", end='')
    print(*x_current, sep=', ', end='}\n')


def main():
    print("Выберите действие: ")
    print("Построить подполугруппу по таблице Кэли (1)")
    print("Построить полугруппу бинарных отношений по порождающему множеству (2)")
    print("Построить полугруппу по порождающему множеству и определяющим соотношениям (3)")
    action = input()
    if action:
        if action == "1":
            build_sub_semigroup()
        if action == '2':
            task2()
        if action == '3':
            build_cayley()


if __name__ == "__main__":
    main()
