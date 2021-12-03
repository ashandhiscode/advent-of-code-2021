from utils import get_input_list_from_day


def get_most_common_bit_at_position(binary_list, position: int, equality_inclusive=None):
    bits = [binary[position] for binary in binary_list]
    if bits.count('1') > len(binary_list) / 2:
        return '1'
    elif bits.count('1') == len(binary_list) / 2 and equality_inclusive:
        return '1'
    elif bits.count('1') == len(binary_list) / 2 and ~equality_inclusive:
        return '0'
    elif bits.count('1') == len(binary_list) / 2:
        raise Exception("This case has not been properly considered.")
    else:
        return '0'


def invert_bit(bit: str) -> str:
    if bit == '1':
        return '0'
    elif bit == '0':
        return '1'


def invert_binary(binary_str: str) -> str:
    inverted_binary_str = ""
    for bit in binary_str:
        inverted_binary_str += invert_bit(bit)
    return inverted_binary_str


def get_least_common_bit_at_position(binary_list, position: int, equality_inclusive=None):
    if equality_inclusive is None:
        most_common_bit = get_most_common_bit_at_position(binary_list, position)
    else:
        most_common_bit = get_most_common_bit_at_position(binary_list, position, ~equality_inclusive)
    return invert_bit(most_common_bit)


def get_gamma_rate(binary_list):
    number_of_bits = len(binary_list[0])
    gamma_rate = ""
    for position in range(number_of_bits):
        most_common_bit = get_most_common_bit_at_position(binary_list, position)
        gamma_rate += most_common_bit
    return gamma_rate


def get_power_consumption(binary_list):
    gamma_rate = get_gamma_rate(binary_list)
    epsilon_rate = invert_binary(gamma_rate)
    power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
    return power_consumption


def get_oxygen_generator_rating(binary_list):
    number_of_bits = len(binary_list[0])
    remaining_options = binary_list.copy()
    position = 0
    while len(remaining_options) > 1:
        most_common_bit = get_most_common_bit_at_position(remaining_options, position, equality_inclusive=True)
        remaining_options = [option for option in remaining_options if option[position] == most_common_bit]
        position = (position + 1) % number_of_bits
    oxygen_generator_rating = remaining_options[0]
    return oxygen_generator_rating


def get_c02_scrubber_rating(binary_list):
    number_of_bits = len(binary_list[0])
    remaining_options = binary_list.copy()
    position = 0
    while len(remaining_options) > 1:
        least_common_bit = get_least_common_bit_at_position(remaining_options, position, equality_inclusive=True)
        remaining_options = [option for option in remaining_options if option[position] == least_common_bit]
        position = (position + 1) % number_of_bits
    c02_scrubber_rating = remaining_options[0]
    return c02_scrubber_rating


def get_life_support_rating(binary_list):
    oxygen_generator_rating = get_oxygen_generator_rating(binary_list)
    c02_scrubber_rating = get_c02_scrubber_rating(binary_list)
    life_support_rating = int(oxygen_generator_rating, 2) * int(c02_scrubber_rating, 2)
    return life_support_rating


if __name__ == "__main__":
    input_list = get_input_list_from_day(3, str)
    print(f"Part 1: {get_power_consumption(input_list)}")
    print(f"Part 2: {get_life_support_rating(input_list)}")
