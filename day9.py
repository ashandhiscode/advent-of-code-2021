from utils import get_input_list_from_day, convert_list_to_type, SearchGrid
import numpy as np
from math import prod


class LavaGrid(SearchGrid):
    def find_low_points(self):
        is_low_point_array = np.ones(shape=self.shape)
        number_of_rows, number_of_cols = self.shape
        # check by row
        for row_num in range(number_of_rows):
            this_row = self.loc[row_num, :]
            if row_num == 0:
                rows_to_check = [self.loc[row_num + 1, :]]
            elif row_num < number_of_rows - 1:
                rows_to_check = [
                    self.loc[row_num - 1, :],
                    self.loc[row_num + 1, :]
                ]
            elif row_num == number_of_rows - 1:
                rows_to_check = [self.loc[row_num - 1, :]]
            else:
                raise Exception("Error.")
            for row in rows_to_check:
                is_low_point_array[row_num, :] *= row > this_row
        # check by col
        for col_num in range(number_of_cols):
            this_col = self.loc[:, col_num]
            if col_num == 0:
                cols_to_check = [self.loc[:, col_num + 1]]
            elif col_num < number_of_cols - 1:
                cols_to_check = [
                    self.loc[:, col_num - 1],
                    self.loc[:, col_num + 1]
                ]
            else:
                cols_to_check = [self.loc[:, col_num - 1]]
            for col in cols_to_check:
                is_low_point_array[:, col_num] *= col > this_col
        return is_low_point_array

    def find_risk_levels(self):
        array = self.values
        low_points = self.find_low_points()
        risk_levels = array[low_points == 1] + 1
        return risk_levels

    def find_basin_points(self, starting_point):
        basin_points = []
        for next_squares in self.search(starting_point,
                                        stop_if=lambda x: x == 9,
                                        include_diagonals=False):
            basin_points += next_squares
        return basin_points

    def find_basins(self):
        basins = []
        next_starting_point = self.find_unsearched_point()
        while next_starting_point is not None:
            basin = self.find_basin_points(next_starting_point)
            basins.append(basin)
            next_starting_point = self.find_unsearched_point()
        return basins


if __name__ == "__main__":
    input_list = get_input_list_from_day(9)
    lava_df = LavaGrid(data=[convert_list_to_type(list(input_), int) for input_ in input_list])
    risk_levels = lava_df.find_risk_levels()
    print(f"Part 1: {sum(risk_levels)}")
    basins = lava_df.find_basins()
    basin_sizes = [len(basin) for basin in basins]
    ordered_basin_sizes = sorted(basin_sizes)
    print(ordered_basin_sizes)
    print(f"Part 2: {prod(ordered_basin_sizes[-3:])}")
