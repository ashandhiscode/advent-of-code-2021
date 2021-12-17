from utils import get_input_list_from_day


def get_connections_dict(connections_list):
    connections = {}
    for connection in connections_list:
        first, second = connection.split('-')
        if first in connections.keys():
            connections[first].append(second)
        else:
            connections[first] = [second]
        if second in connections.keys():
            connections[second].append(first)
        else:
            connections[second] = [first]
    return connections


def get_number_of_previous_visits_to_small_caves(path):
    prev_visits_dict = {}
    for point in set(path):
        if point.isupper():
            continue
        prev_visits_dict[point] = path.count(point)
    return prev_visits_dict


def create_possible_pathways(
        current_paths: list[list[str]],
        choices_for_next_step: list[list[str]],
        number_small_caves_twice=0
) -> list[list[str]]:
    possibilities = []
    for path, options in zip(current_paths, choices_for_next_step):
        if path[-1] == 'end':
            # ie this path is complete! cannot continue
            possibilities.append(path)
            continue
        prev_visits = get_number_of_previous_visits_to_small_caves(path)
        for option in options:
            if option == 'start':
                continue
            elif option.islower() and option in prev_visits.keys():
                if prev_visits[option] >= 2:
                    continue
                if len([visits for visits in prev_visits.values() if visits >= 2]) >= number_small_caves_twice:
                    continue
                else:
                    possibility = path + [option]
                    possibilities.append(possibility)
            else:
                possibility = path + [option]
                possibilities.append(possibility)
    return possibilities


def find_paths(connections, number_of_small_caves_twice_visited=0):
    paths = [['start']]
    while not all([path[-1] == 'end' for path in paths]):
        possible_next_steps = [connections[path[-1]] for path in paths]
        paths = create_possible_pathways(paths, possible_next_steps, number_of_small_caves_twice_visited)
    return paths


if __name__ == "__main__":
    input_list = get_input_list_from_day(12)
    connections_dict = get_connections_dict(input_list)
    pathways = find_paths(connections_dict)
    print(f"Part 1: there are {len(pathways)} paths.")
    pathways = find_paths(connections_dict, number_of_small_caves_twice_visited=1)
    print(f"Part 2: there are {len(pathways)} paths.")
