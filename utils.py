from typing import Any, Union
from pathlib import Path


def read_input_list_from_path(input_filepath: Union[str, Path], as_type: type = str):
    with input_filepath.open() as file:
        file_str = file.read()
        text_list = file_str.split('\n')
        text_list = text_list[:-1]  # there is a final empty string we need to shave off at the end
        return [as_type(text) for text in text_list]


def get_input_filepath(day_number: Union[int, str]) -> Path:
    return Path(__file__).parent / 'inputs' / f'day{str(day_number)}.txt'


def get_input_list_from_day(day_number: Union[int, str], as_type: type = str) -> list[Any]:
    input_filepath = get_input_filepath(day_number)
    input_list = read_input_list_from_path(input_filepath, as_type=as_type)
    return input_list
