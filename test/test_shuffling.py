from algorithm.shuffle_algorithm import shuffle_list


def test_shuffling():

    elements = 100
    initial_list = [i for i in range(elements)]

    shuffled = shuffle_list(initial_list)

    assert len(shuffled) == len(initial_list)
    assert len(set(shuffled)) == len(shuffled)