from typing import List

from algorithm.shuffle_algorithm import shuffle_list
import random

def test_shuffling_empty():
    shuffled = shuffle_list([])
    assert len(shuffled) == 0

def test_shuffling_one():
    shuffled = shuffle_list([1])
    assert shuffled == [1]

def test_shuffling_asc():
    elements = 100
    initial_list = [i for i in range(elements)]

    shuffled = shuffle_list(initial_list)

    assert len(shuffled) == len(initial_list)
    assert len(set(shuffled)) == len(shuffled)


def test_shuffling_desc():
    elements = 100
    initial_list = [i for i in range(elements-1, -1, -1)]

    shuffled = shuffle_list(initial_list)

    assert len(shuffled) == len(initial_list)
    assert len(set(shuffled)) == len(shuffled)

def test_shuffling_multiple():
    elements = 100
    initial_list = [i for i in range(elements)]
    for i in range(5):
        shuffled = shuffle_list(initial_list)
        assert len(shuffled) == len(initial_list)
        assert len(set(shuffled)) == len(shuffled)

def _verify_counts(initial_list: List[int], shuffled: List[int]):
    counts_init = {}
    counts_shuffled = {}

    for i in initial_list:
        if i in counts_init:
            counts_init[i] += 1
        else:
            counts_init[i] = 1
    for i in shuffled:
        if i in counts_shuffled:
            counts_shuffled[i] += 1
        else:
            counts_shuffled[i] = 1
    assert counts_init == counts_shuffled

def test_shuffling_duplicates():
    elements = 32
    initial_list = [i % 5 for i in range(elements)]
    shuffled = shuffle_list(initial_list)
    assert len(shuffled) == len(initial_list)
    _verify_counts(initial_list, shuffled)

def test_shuffling_random():
    elements = 100
    initial_list = []
    for i in range(elements):
        a = random.randint(0, 2000)
        initial_list.append(a)
    shuffled = shuffle_list(initial_list)
    assert len(shuffled) == len(initial_list)
    _verify_counts(initial_list, shuffled)

