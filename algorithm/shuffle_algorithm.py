import random
from typing import TypeVar, List

T = TypeVar('T')

def shuffle_list(element_list: List[T]) -> List[T]:
    new_list = []
    n = len(element_list)
    prev_list = list(element_list)
    for i in range(n):
        index = random.randint(0, n-1)
        a = prev_list.pop(index)
        new_list.append(a)
        n -= 1
    return new_list