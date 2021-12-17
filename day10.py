from utils import get_input_list_from_day

import pandas as pd


class BracketsException(Exception):
    pass


def autocomplete(string):
    close_to_open_map = {')': '(', '>': '<', '}': '{', ']': '['}
    open_to_close_map = {'(': ')', '<': '>', '{': '}', '[': ']'}
    open_chunks = []
    for index, char in enumerate(string):
        if char in close_to_open_map.values():
            open_chunks.append(char)
        elif char in close_to_open_map.keys():
            if close_to_open_map[char] != open_chunks[-1]:
                raise BracketsException(char)
            open_chunks.pop(-1)
    closing_autocomplete = ""
    for char in open_chunks[::-1]:
        closing_autocomplete += open_to_close_map[char]
    return closing_autocomplete


def get_syntax_error_score(char):
    syntax_error_score_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
    return syntax_error_score_map[char]


def get_autocomplete_score(substring):
    autocompletion_error_score_map = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0
    for char in substring:
        score *= 5
        score += autocompletion_error_score_map[char]
    return score


if __name__ == "__main__":
    input_list = get_input_list_from_day(10)
    total_error_score = 0
    autocompletion_scores = []
    for chunk_string in input_list:
        try:
            autocomplete_string = autocomplete(chunk_string)
            autocompletion_score = get_autocomplete_score(autocomplete_string)
            autocompletion_scores.append(autocompletion_score)
        except BracketsException as e:
            problem_char = str(e)
            total_error_score += get_syntax_error_score(problem_char)
        except Exception as e:
            raise e
    print(f"Part 1: {total_error_score}")
    print(f"Part 2: {pd.Series(autocompletion_scores).median()}")
