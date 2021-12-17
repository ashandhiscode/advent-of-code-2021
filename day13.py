from utils import get_input_list_from_day, convert_list_to_type
from pathlib import Path

import pandas as pd
import numpy as np


class FoldingDataFrame(pd.DataFrame):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def fold(self, line, axis, layer_func=lambda x, y: x * y):
        vectorized_layer_func = np.vectorize(layer_func)
        if axis == 1:
            # fold vertically
            upper_half = self.values[:line, :].copy()
            lower_half = self.values[line+1:, :].copy()
            lower_half = lower_half[::-1, :]
            new_array = vectorized_layer_func(upper_half, lower_half)
        elif axis == 0:
            left_half = self.values[:, :line]
            right_half = self.values[:, line+1:]
            right_half = right_half[:, ::-1]
            new_array = vectorized_layer_func(left_half, right_half)
        else:
            raise Exception("Axis parameter should be 0 or 1.")
        self.__init__(new_array)

    def get_hash_view(self):
        return self.applymap(lambda bool_value: '#' if bool_value else '.')

    def print_hash_view(self):
        print(self.get_hash_view())

    def __repr__(self):
        return self.get_hash_view()


def translate_fold_command(fold_command):
    axis_str, line_pos_str = fold_command.split('=')
    axis = int(axis_str[-1] == 'y')
    line_pos = int(line_pos_str)
    return axis, line_pos


def get_boolean_grid(list_of_coordinates):
    max_x = max([x for x, y in list_of_coordinates])
    max_y = max([y for x, y in list_of_coordinates])
    array = [[[x, y] in list_of_coordinates for x in range(max_x+1)] for y in range(max_y+1)]
    return array


if __name__ == "__main__":
    input_list = get_input_list_from_day(13)
    split_point = input_list.index('')
    coordinates = [
        convert_list_to_type(coordinate_pair.split(','), int) for coordinate_pair in input_list[:split_point]
    ]
    folds_to_perform = [
        translate_fold_command(fold_str) for fold_str in input_list[split_point + 1:]
    ]
    folding_df = FoldingDataFrame(data=get_boolean_grid(coordinates))
    for index, fold in enumerate(folds_to_perform):
        if index == 1:
            print(f"Part 1: {folding_df.apply(sum).sum()}")
        axis, line = fold
        folding_df.fold(line, axis, lambda bool1, bool2: bool1 or bool2)
    folding_df.get_hash_view().to_csv(Path.cwd() / 'day13_pt2_code.csv', index=False)
    print(f"Part 2: look in the generated CSV for the corresponding code. "
          f"Some conditional formatting in excel will help.")
