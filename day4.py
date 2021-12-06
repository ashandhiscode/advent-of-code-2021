from typing import Any

from utils import get_input_list_from_day, convert_list_to_type, read_numbers_line

import pandas as pd


def read_bingo_line(line_str: str) -> list[int]:
    digits = '0123456789'
    numbers_in_row = []
    if line_str[0] in digits:
        prev_char_was_number = True
        current_number = line_str[0]
    else:
        prev_char_was_number = False
        current_number = ""
    for char in line_str[1:]:
        if char in digits and prev_char_was_number:
            current_number += char
            prev_char_was_number = True
        elif char in digits and ~prev_char_was_number:
            current_number = char
            prev_char_was_number = True
        elif char not in digits and prev_char_was_number:
            numbers_in_row.append(int(current_number))
            current_number = ""
            prev_char_was_number = False
    # final char
    if prev_char_was_number:
        numbers_in_row.append(int(current_number))
    return numbers_in_row


def transform_input_list_to_bingo_cards(input_list: list) -> tuple[list[int], list[Any]]:
    numbers_to_call = read_numbers_line(input_list[0])
    bingo_cards = []
    current_bingo_card = []
    for row in input_list[2:]:
        if row == '':
            bingo_cards.append(current_bingo_card)
            current_bingo_card = []
        else:
            bingo_line = read_bingo_line(row)
            current_bingo_card.append(bingo_line)
    return numbers_to_call, bingo_cards


class BingoCard:
    def __init__(self, list_of_rows):
        self.my_numbers = list_of_rows
        self.height = len(list_of_rows)
        self.width = len(list_of_rows[0])
        self.my_progress = [[False for _ in range(self.width)] for _ in range(self.height)]

    def print_board(self, numbers_so_far=None):
        if numbers_so_far is None:
            print(pd.DataFrame(self.my_numbers))
            print(pd.DataFrame(self.my_progress))
        else:
            print(pd.DataFrame(self.my_numbers).apply(lambda x: 'X' if x in numbers_so_far else x))

    def find_number(self, number):
        for y in range(self.height):
            for x in range(self.width):
                if self.my_numbers[y][x] == number:
                    return x, y

    def strike_position(self, x, y):
        self.my_progress[y][x] = True

    def find_and_strike_number(self, number):
        number_pos = self.find_number(number)
        if number_pos is not None:
            x, y = number_pos
            self.strike_position(x, y)

    def check_for_line(self):
        for row in self.my_progress:
            if all(row):
                return True
        for col in [[row[i] for row in self.my_progress] for i in range(self.width)]:
            if all(col):
                return True
        return False

    def make_full_turn(self, number):
        self.find_and_strike_number(number)
        if self.check_for_line():
            return "BINGO"

    def get_remaining_total(self):
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                if bool(self.my_progress[y][x]):
                    continue
                else:
                    total += self.my_numbers[y][x]
        return total


class BingoManager:
    def __init__(self, numbers_to_call, bingo_cards):
        self.numbers_to_call = numbers_to_call
        self.numbers_called = []
        self.bingo_cards = [BingoCard(bingo_card) for bingo_card in bingo_cards]

    def call_number(self, number):
        winners = []
        for index, bingo_card in enumerate(self.bingo_cards):
            if bingo_card.make_full_turn(number) == 'BINGO':
                winners.append(index)
        if len(winners) > 0:
            return winners

    def play_game(self, print_board_num=None, continue_when_win=False):
        pos_list = []
        winners_so_far = []
        for number in self.numbers_to_call:
            winners = self.call_number(number)
            self.numbers_called.append(number)
            if print_board_num is not None:
                self.bingo_cards[print_board_num].print_board()
            if winners is not None:
                if not continue_when_win:
                    if len(winners) > 1:
                        return winners
                    else:
                        return winners[0]
                else:
                    new_winners = [winner for winner in winners if winner not in winners_so_far]
                    if len(new_winners) > 0:
                        pos_list.append(new_winners)
                    winners_so_far += new_winners
        return pos_list


if __name__ == "__main__":
    input_list = get_input_list_from_day(4)
    numbers_to_call, bingo_cards = transform_input_list_to_bingo_cards(input_list)
    bingo = BingoManager(numbers_to_call, bingo_cards)
    winner = bingo.play_game()
    winning_bingo_card = bingo.bingo_cards[winner]
    winners_remaining = winning_bingo_card.get_remaining_total()
    print(f"Part1: winner number {winner} had remainder {winners_remaining}, with last call {bingo.numbers_called[-1]}")
    # part 2
    bingo = BingoManager(numbers_to_call, bingo_cards)
    positions = bingo.play_game(continue_when_win=True)
    last_place = positions[-1][0]
    bingo = BingoManager(numbers_to_call, [bingo_cards[last_place]])
    winner = bingo.play_game()
    winning_bingo_card = bingo.bingo_cards[winner]
    winners_remaining = winning_bingo_card.get_remaining_total()
    print(f"Part 2: loser {last_place} had remainder {winners_remaining} with last call {bingo.numbers_called[-1]}")
