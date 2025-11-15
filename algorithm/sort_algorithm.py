from typing import TypeVar, List

T = TypeVar('T')

def _merge(left: List[T], right: List[T]) -> List[T]:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged

def sort_list(element_list: List[T]) -> List[T]:
    if len(element_list) <= 1:
        return element_list[:]
    mid = len(element_list) // 2
    left = sort_list(element_list[:mid])
    right = sort_list(element_list[mid:])
    return _merge(left, right)