from utils import get_input_list_from_day, convert_list_to_type, SearchGrid

import numpy as np


class OctopusGrid(SearchGrid):
    total_flashes = 0

    def get_flashing_points(self):
        flashing_points = []
        for y, x in zip(*np.where(self.values > 9)):
            if (x, y) not in self.searched_squares:
                flashing_points.append((x, y))
        return flashing_points

    def increase_energy_at_point(self, x, y):
        self.iloc[y, x] += 1

    def add_daily_energy(self):
        self.__init__(data=self.values + 1)

    def octopus_flash(self, x, y):
        assert self.values[y, x] > 9
        assert (x, y) not in self.searched_squares
        neighbours = self.get_neighbours(x, y, include_diagonals=True)
        for neighbour in neighbours:
            x_neighbour, y_neighbour = neighbour
            self.increase_energy_at_point(x_neighbour, y_neighbour)
        self.record_search(x, y)
        self.total_flashes += 1

    def set_exploded_points_to_0(self):
        for x, y in self.searched_squares:
            self.iloc[y, x] = 0

    def one_day_passes(self):
        self.add_daily_energy()
        flashing_points = self.get_flashing_points()
        while len(flashing_points) > 0:
            for x, y in flashing_points:
                self.octopus_flash(x, y)
            flashing_points = self.get_flashing_points()
        self.set_exploded_points_to_0()


if __name__ == "__main__":
    input_list = get_input_list_from_day(11, list)
    input_list = [convert_list_to_type(input_, int) for input_ in input_list]
    grid = OctopusGrid(data=input_list)
    for _ in range(100):
        grid.one_day_passes()
    print(f"Part 1: {grid.total_flashes}")
    grid = OctopusGrid(data=input_list)
    steps_taken = 0
    while not all((grid == 0).all()):
        grid.one_day_passes()
        steps_taken += 1
    print(f"Part 2: {steps_taken}")
