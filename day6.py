from typing import Iterable

import time
import pandas as pd

from utils import get_input_list_from_day, read_numbers_line


class Lanternfish:
    def __init__(self, init_age=None):
        if init_age is None:
            self.birth_timer = 8
            self.ready_to_birth = False
        else:
            self.birth_timer = init_age
            if self.birth_timer == 0:
                self.ready_to_birth = True
            else:
                self.ready_to_birth = False

    def age(self):
        if self.ready_to_birth:
            self.birth_timer = 6
            self.ready_to_birth = False
            return "BIRTH"
        else:
            self.birth_timer -= 1
            if self.birth_timer == 0:
                self.ready_to_birth = True


class Midwife:
    def __init__(self):
        pass

    @staticmethod
    def give_birth(lanternfish: Lanternfish):
        return Lanternfish()

    def deliver(self, fish_iter, lanternfish):
        fish_iter.append(self.give_birth(lanternfish))
        return fish_iter


class Swarm:
    def __init__(self, fish_iter: Iterable[Lanternfish]):
        self.day = 0
        self.fish = list(fish_iter)
        self.midwife = Midwife()

    def age(self):
        new_fish = []
        for fish in self.fish:
            if fish.age() == 'BIRTH':
                self.midwife.deliver(new_fish, fish)
        self.fish += new_fish
        self.day += 1

    def days_pass(self, days, print_day=False):
        for day in range(days):
            self.age()
            if print_day:
                time.sleep(0.25)
                print(f"Day number: {self.day}")

    def __repr__(self):
        return [fish.birth_timer for fish in self.fish].__repr__()

    def count(self):
        return len(self.fish)


class SwarmCounter:
    def __init__(self, numbers_dict):
        self.options = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.numbers = {}
        for number in self.options:
            if number in numbers_dict.keys():
                self.numbers[number] = numbers_dict[number]
            else:
                self.numbers[number] = 0

    def day_passes(self):
        new_dict = {}
        for number in self.options:
            if number not in [6, 8]:
                new_dict[number] = self.numbers[number + 1]
            elif number == 6:
                new_dict[6] = self.numbers[7] + self.numbers[0]
            elif number == 8:
                new_dict[8] = self.numbers[0]
        self.numbers = new_dict

    def days_pass(self, days):
        for day in range(days):
            self.day_passes()

    def count(self):
        return sum(self.numbers.values())


if __name__ == "__main__":
    input_list = get_input_list_from_day(6)
    input_list = read_numbers_line(input_list[0])
    swarm = Swarm([Lanternfish(init_age) for init_age in input_list])
    swarm.days_pass(80)
    print(f"Part 1: after 80 days there are {swarm.count()}")
    # the problem is then about efficiency. We need to do part 2 mathematically
    # shorten for check
    swarmcount = SwarmCounter(pd.Series(input_list).value_counts().sort_index().to_dict())
    swarmcount.days_pass(80)
    print(f"Part 1 as a generalisation of part 2: after 80 days there are {swarmcount.count()}")
    swarmcount.days_pass(256-80)
    print(f"Part 2: after 256 days there are {swarmcount.count()}")
