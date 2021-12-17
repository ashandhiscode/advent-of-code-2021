from typing import Any, Union, Iterable
from pathlib import Path

import pandas as pd


def read_input_list_from_path(input_filepath: Union[str, Path], as_type: type = str):
    with input_filepath.open() as file:
        file_str = file.read()
        text_list = file_str.split('\n')
        if text_list[-1] == "":
            text_list = text_list[:-1]
        return [as_type(text) for text in text_list]


def get_input_filepath(day_number: Union[int, str]) -> Path:
    return Path(__file__).parent / 'inputs' / f'day{str(day_number)}.txt'


def get_input_list_from_day(day_number: Union[int, str], as_type: type = str) -> list[Any]:
    input_filepath = get_input_filepath(day_number)
    input_list = read_input_list_from_path(input_filepath, as_type=as_type)
    return input_list


def convert_list_to_type(list_to_convert: list[Any], as_type: type = int) -> Any:
    return [as_type(elem) for elem in list_to_convert]


def read_numbers_line(line_str: str) -> list[int]:
    line_list = line_str.split(',')
    return convert_list_to_type(line_list, int)


def sum_numbers_from_1_to(n: int) -> int:
    return int(n * (n + 1) / 2)


def shave(string1: str, strings_to_shave_off: Union[str, Iterable[str]]) -> str:
    string1_copy = string1
    if isinstance(strings_to_shave_off, str):
        for char in strings_to_shave_off:
            string1_copy = string1_copy.replace(char, '')
    elif isinstance(strings_to_shave_off, Iterable):
        for string2 in strings_to_shave_off:
            for char in string2:
                string1_copy = string1_copy.replace(char, '')
    return string1_copy


def string_intersection(*arg) -> str:
    return_str = ""
    init_string = arg[0]
    for char in init_string:
        if all([char in arg for arg in arg[1:]]):
            return_str += char
    return return_str


class SearchGrid(pd.DataFrame):
    searched_squares = []

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.refresh()

    def refresh(self):
        self.searched_squares = []

    def record_search(self, x, y):
        self.searched_squares.append((x, y))

    def get_neighbours(self, x, y, include_diagonals=False):
        verified_neighbours = []
        neighbours = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        if include_diagonals:
            neighbours += [(x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
        for neighbour in neighbours:
            proposed_x, proposed_y = neighbour
            if 0 <= proposed_x < len(self.columns) and 0 <= proposed_y < self.__len__():
                verified_neighbours.append(neighbour)
        return verified_neighbours

    def next_positions(self, positions, include_diagonals=False):
        next_positions = []
        for position in positions:
            neighbours = self.get_neighbours(*position, include_diagonals)
            for neighbour in neighbours:
                if neighbour not in self.searched_squares and neighbour not in next_positions:
                    next_positions.append(neighbour)
        return next_positions

    def find_unsearched_point(self):
        for x in range(len(self.columns)):
            for y in range(self.__len__()):
                if (x, y) not in self.searched_squares:
                    return x, y

    def search(self,
               start_position,
               stop_if=None,
               include_diagonals=False):
        next_positions = [start_position]
        self.searched_squares += next_positions
        while len(next_positions) > 0:
            if stop_if is not None:
                next_positions = [
                    (x, y) for (x, y) in next_positions
                    if ~stop_if(self.values[y, x])
                ]
            yield next_positions
            next_positions = self.next_positions(next_positions, include_diagonals)
            self.searched_squares += next_positions
