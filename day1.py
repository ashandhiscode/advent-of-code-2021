from typing import Union

from utils import get_input_list_from_day

numerical = Union[int, float]


def get_increments(input_list: list[numerical]) -> int:
    number_of_increments = 0
    first_number = input_list[0]
    prev = first_number
    for i in range(1, len(input_list)):
        curr = input_list[i]
        if curr > prev:
            number_of_increments += 1
        prev = curr
    return number_of_increments


def get_window_increments(input_list: list[numerical], window_size: int = 1) -> int:
    number_of_increments = 0
    first_window = sum(input_list[0:window_size])
    prev_window = first_window
    for i in range(1, len(input_list) - window_size + 1):
        curr_window = sum(input_list[i:i + window_size])
        if curr_window > prev_window:
            number_of_increments += 1
        prev_window = curr_window
    return number_of_increments


if __name__ == "__main__":
    input_list = get_input_list_from_day(1, int)
    print(f"Part 1: {get_increments(input_list)}")
    print(f"Part 1 as a generalisation of part 2: {get_window_increments(input_list, 1)}")
    print(f"Part 2: {get_window_increments(input_list, 3)}")
