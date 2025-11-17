import random

from algorithm.sort_algorithm import sort_list


def test_sorting_empty():
    sorted_list = sort_list([])
    assert len(sorted_list) == 0

def test_sorting_one():
    sorted_list = sort_list([1])
    assert sorted_list == [1]

def test_sorting_random():
    elements = 100
    initial_list = []
    for i in range(elements):
        a = random.randint(0, 2000)
        initial_list.append(a)

    sorted_list = sort_list(initial_list)

    for i in range(1, elements):
        assert sorted_list[i-1] <= sorted_list[i]

def test_sorting_ascending():
    elements = 100
    initial_list = [i for i in range(elements)]

    sorted_list = sort_list(initial_list)

    for i in range(1, elements):
        assert sorted_list[i-1] <= sorted_list[i]

def test_sorting_descending():
    elements = 100
    initial_list = [i for i in range(elements-1, -1, -1)]

    sorted_list = sort_list(initial_list)

    for i in range(1, elements):
        assert sorted_list[i-1] <= sorted_list[i]
