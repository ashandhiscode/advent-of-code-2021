from utils import get_input_list_from_day

import pandas as pd


def get_line_endpoints(input_str):
    start, end = input_str.split(' -> ')
    x_start, y_start = start.split(',')
    x_end, y_end = end.split(',')
    return (int(x_start), int(y_start)), (int(x_end), int(y_end))


def sort_lexicographically(two_points):
    coordinates1, coordinates2 = two_points
    x1, y1 = coordinates1
    x2, y2 = coordinates2
    if x2 > x1:
        return coordinates1, coordinates2
    elif x1 > x2:
        return coordinates2, coordinates1
    else:
        if y2 > y1:
            return coordinates1, coordinates2
        else:
            return coordinates2, coordinates1


def get_line_points(start_point, end_point, diagonal=False):
    start_point, end_point = sort_lexicographically((start_point, end_point))
    x1, y1 = start_point
    x2, y2 = end_point
    if x1 == x2:
        return [(x1, y) for y in range(y1, y2 + 1)]
    elif y1 == y2:
        return [(x, y1) for x in range(x1, x2 + 1)]
    elif abs(x2 - x1) == abs(y2 - y1) and diagonal:
        return get_diagonal_line_points(start_point, end_point)
    elif abs(x2 - x1) == abs(y2 - y1):
        # diagonal in 45 degrees
        return []
    else:
        raise Exception("We only consider 45 degree diagonal cases.")


def get_diagonal_line_points(start_point, end_point):
    x1, y1 = start_point
    x2, y2 = end_point
    distance = abs(x1 - x2)
    if y1 < y2:
        # then ascend
        return [(x1+i, y1+i) for i in range(distance+1)]
    elif y2 < y1:
        # then descend
        return [(x1+i, y1-i) for i in range(distance+1)]


class Grid(pd.DataFrame):
    def __init__(self, height, width):
        data = [[0 for _ in range(width)] for _ in range(height)]
        super().__init__(data)

    def total_overlapping_points(self):
        total = 0
        for col in self.columns:
            for row in self.index:
                if self.loc[col, row] > 1:
                    total += 1
        return total

    def lay_vent(self, point):
        x, y = point
        self.iloc[y, x] += 1


if __name__ == "__main__":
    input_list = get_input_list_from_day(5)
    grid = Grid(1000, 1000)
    for vent in input_list:
        end_points = get_line_endpoints(vent)
        points = get_line_points(*end_points, diagonal=False)
        for point in points:
            grid.lay_vent(point)
    print(f"Part 1: there are {grid.total_overlapping_points()} overlapping points.")
    grid = Grid(1000, 1000)
    for vent in input_list:
        end_points = get_line_endpoints(vent)
        points = get_line_points(*end_points, diagonal=True)
        for point in points:
            grid.lay_vent(point)
    print(f"Part 2: there are {grid.total_overlapping_points()} overlapping points.")
