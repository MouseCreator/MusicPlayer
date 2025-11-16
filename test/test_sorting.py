import random

from algorithm.sort_algorithm import sort_list


def test_sorting():
    elements = 100
    initial_list = []
    for i in range(elements):
        a = random.randint(0, 2000)
        initial_list.append(a)

    sorted_list = sort_list(initial_list)

    for i in range(1, elements):
        assert sorted_list[i-1] <= sorted_list[i]