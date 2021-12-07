from utils import get_input_list_from_day, read_numbers_line, sum_numbers_from_1_to

import pandas as pd
import numpy as np


def find_best_midpoint_with_min_fuel(coordinates_series, fuel_function=lambda x: x):
    max_num = coordinates_series.max()
    min_num = coordinates_series.min()
    best_position = min_num
    min_fuel = np.abs(coordinates_series - min_num).apply(fuel_function).sum()
    for position in range(min_num, max_num + 1):
        total_fuel = np.abs(coordinates_series - position).apply(fuel_function).sum()
        if total_fuel < min_fuel:
            min_fuel = total_fuel
            best_position = position
    return best_position, min_fuel


if __name__ == "__main__":
    input_list = get_input_list_from_day(7)
    input_list = read_numbers_line(input_list[0])
    crab_coordinates = pd.Series(input_list)
    best_position, min_fuel = find_best_midpoint_with_min_fuel(crab_coordinates)
    print(f"Part 1: the optimal position is {best_position}, with total fuel {min_fuel} consumed.")
    best_position, min_fuel = find_best_midpoint_with_min_fuel(
        crab_coordinates,
        fuel_function=lambda n: sum_numbers_from_1_to(n)
    )
    print(f"Part 2: the optimal position is {best_position}, with total fuel {min_fuel} consumed.")
