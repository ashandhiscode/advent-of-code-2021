from utils import get_input_list_from_day, shave, string_intersection


def convert_from_length_if_known(length):
    map_dict = {2: 1, 4: 4, 3: 7, 7: 8}
    if length in map_dict:
        return map_dict.get(length)
    else:
        return None


def translate_segments_to_number(segments: set) -> int:
    # 0
    if segments == {'T', 'B', 'UR', 'BR', 'UL', 'BL'}:
        return 0
    # 1
    elif segments == {'UR', 'BR'}:
        return 1
    # 2
    elif segments == {'T', 'B', 'UR', 'BL', 'M'}:
        return 2
    # 3
    elif segments == {'T', 'UR', 'BR', 'M', 'B'}:
        return 3
    # 4
    elif segments == {'UR', 'UL', 'M', 'BR'}:
        return 4
    # 5
    elif segments == {'T', 'M', 'B', 'UL', 'BR'}:
        return 5
    # 6
    elif segments == {'T', 'M', 'B', 'BR', 'BL', 'UL'}:
        return 6
    # 7
    elif segments == {'T', 'UR', 'BR'}:
        return 7
    # 8
    elif segments == {'T', 'M', 'B', 'UR', 'UL', 'BR', 'BL'}:
        return 8
    # 9
    elif segments == {'T', 'M', 'B', 'UR', 'UL', 'BR'}:
        return 9
    else:
        print(segments)
        raise Exception("No clear mapping.")


def convert_string_to_segments(string, segment_key):
    segments = set()
    for char in string:
        segments.add(segment_key[char])
    return segments


def convert_string_to_number(string, segment_key):
    return translate_segments_to_number(
        convert_string_to_segments(string, segment_key=segment_key)
    )


def get_quantity_dictionary(output_list):
    quantity_dict = {1: 0, 4: 0, 7: 0, 8: 0}
    output_lengths = [list(map(len, output)) for output in output_list]
    output_values = [list(map(convert_from_length_if_known, lengths)) for lengths in output_lengths]
    for output in output_values:
        for num in [1, 4, 7, 8]:
            quantity_dict[num] += output.count(num)
    return quantity_dict


def infer_map_dict_from_strings(input_strings):
    map_dict = {}

    # we start by finding the string that represents 1 and 'subtracting it' from the string representing 7
    # we then see that we can see which letter represents 'T' (top)
    def get_number_from_strings(n, strings):
        if n == 1:
            length = 2
        elif n == 4:
            length = 4
        elif n == 7:
            length = 3
        elif n == 8:
            length = 7
        elif n in (0, 6, 9):
            length = 6
        elif n in (2, 3, 5):
            length = 5
        else:
            raise Exception("Not possible.")
        filtered_numbers = [string for string in strings if len(string) == length]
        if len(filtered_numbers) == 1:
            return filtered_numbers[0]
        else:
            return filtered_numbers

    number_dict = {}
    for number in [1, 4, 7, 8]:
        number_dict[number] = get_number_from_strings(number, input_strings)
    t_letter = shave(number_dict[7], number_dict[1])
    # change the name to account for conceptual shift
    ur_br_pair = number_dict[1]
    m_ul_pair = shave(number_dict[4], number_dict[1])
    b_bl_pair = shave("abcdefg", (number_dict[4], t_letter))
    numbers_2_3_4_trio = get_number_from_strings(2, input_strings)
    t_m_b_trio = string_intersection(*numbers_2_3_4_trio)
    m_letter = shave(t_m_b_trio, (t_letter, b_bl_pair))
    ul_letter = shave(m_ul_pair, m_letter)
    b_letter = shave(t_m_b_trio, (t_letter, m_letter))
    bl_letter = shave(b_bl_pair, b_letter)
    numbers_0_6_9_trio = get_number_from_strings(6, input_strings)
    br_letter = shave(string_intersection(*numbers_0_6_9_trio), (t_letter, b_letter, ul_letter))
    ur_letter = shave(ur_br_pair, br_letter)
    map_dict[t_letter] = 'T'
    map_dict[ur_letter] = 'UR'
    map_dict[ul_letter] = 'UL'
    map_dict[b_letter] = 'B'
    map_dict[m_letter] = 'M'
    map_dict[br_letter] = 'BR'
    map_dict[bl_letter] = 'BL'
    assert all([char in map_dict.keys() for char in 'abcdefg'])
    assert all([len(key) == 1 for key in map_dict.keys()])
    return map_dict


if __name__ == "__main__":
    input_list = get_input_list_from_day(8)
    input_output_pairs = [input_.split(' | ') for input_ in input_list]
    input_list = [input_output_pair[0].split(' ') for input_output_pair in input_output_pairs]
    output_list = [input_output_pair[-1].split(' ') for input_output_pair in input_output_pairs]
    quantity_dict = get_quantity_dictionary(output_list)
    print(f"Part 1: {sum(quantity_dict.values())}")
    total = 0
    for input_strings, output_strings in zip(input_list, output_list):
        map_dict = infer_map_dict_from_strings(input_strings)
        numbers = list(map(lambda string: str(convert_string_to_number(string, map_dict)), output_strings))
        number = int("".join(numbers))
        total += number
    print(f"Part 2: {total}")
