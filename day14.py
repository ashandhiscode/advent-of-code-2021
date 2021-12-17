from utils import get_input_list_from_day


def get_insertions_dict(insertions_list):
    insertions_dict = {}
    for insertion in insertions_list:
        pair, letter_to_insert = insertion.split(' -> ')
        insertions_dict[pair] = letter_to_insert
    return insertions_dict


def apply_round_of_insertions(string, insertions_dict):
    orig_string = string
    for index in range(len(orig_string) - 1):
        substr = orig_string[index:index + 2]
        letter_to_insert = insertions_dict[substr]
        string = string[:2 * index + 1] + letter_to_insert + string[2 * index + 1:]
    return string


def apply_n_rounds_of_insertions(start_string, insertions_dict, rounds=10):
    string = start_string
    for _ in range(rounds):
        string = apply_round_of_insertions(string, insertions_dict)
    return string


def count_characters(string):
    count_dict = {}
    for char in set(string):
        count_dict[char] = string.count(char)
    return count_dict


def get_pairs_dict(string):
    pairs_dict = {}
    for index in range(len(string) - 1):
        substr = string[index:index + 2]
        if substr in pairs_dict.keys():
            pairs_dict[substr] += 1
        else:
            pairs_dict[substr] = 1
    return pairs_dict


def get_insertions_growth_dict(insertions_dict):
    insertions_growth_dict = {}
    for key, value in insertions_dict.items():
        first_letter, second_letter = key
        insertions_growth_dict[key] = [f"{first_letter}{value}", f"{value}{second_letter}"]
    return insertions_growth_dict


def apply_round_of_insertions_to_pairs_dict(pairs_dict, insertions_growth_dict):
    new_pair_dict = {}
    for pair, quantity in pairs_dict.items():
        new_pairs = insertions_growth_dict[pair]
        for new_pair in new_pairs:
            if new_pair in new_pair_dict.keys():
                new_pair_dict[new_pair] += quantity
            else:
                new_pair_dict[new_pair] = quantity
    return new_pair_dict


def apply_n_rounds_of_insertions_to_pairs_dict(pairs_dict, insertions_growth_dict, rounds=40):
    for _ in range(rounds):
        pairs_dict = apply_round_of_insertions_to_pairs_dict(pairs_dict, insertions_growth_dict)
    return pairs_dict


def get_quantity_dict_from_pairs_dict(pairs_dict, original_string):
    first_letter = original_string[0]
    last_letter = original_string[-1]
    quantity_dict = {}
    for pair, quantity in pairs_dict.items():
        for letter in pair:
            if letter in quantity_dict.keys():
                quantity_dict[letter] += quantity
            else:
                quantity_dict[letter] = quantity
    final_quantity_dict = {}
    for letter, quantity in quantity_dict.items():
        letter_is_first_or_last = (letter == first_letter) | (letter == last_letter)
        final_quantity_dict[letter] = int(letter_is_first_or_last) + (quantity - int(letter_is_first_or_last)) / 2
    return final_quantity_dict


if __name__ == "__main__":
    input_list = get_input_list_from_day(14)
    char_string = input_list[0]
    insertions_dict = get_insertions_dict(input_list[2:])
    insertions_growth_dict = get_insertions_growth_dict(insertions_dict)
    char_string_after_10_rounds = apply_n_rounds_of_insertions(char_string, insertions_dict, 10)
    quantity_dict = count_characters(char_string_after_10_rounds)
    print(f"Part 1: {max(quantity_dict.values()) - min(quantity_dict.values())}")
    pairs_dict = get_pairs_dict(char_string)
    pairs_dict_after_10_rounds = apply_n_rounds_of_insertions_to_pairs_dict(pairs_dict, insertions_growth_dict, 10)
    quantity_dict = get_quantity_dict_from_pairs_dict(pairs_dict_after_10_rounds, char_string)
    print(f"Part 1 efficiently: {int(max(quantity_dict.values()) - min(quantity_dict.values()))}")
    pairs_dict_after_40_rounds = apply_n_rounds_of_insertions_to_pairs_dict(pairs_dict_after_10_rounds,
                                                                            insertions_growth_dict,
                                                                            30)
    quantity_dict = get_quantity_dict_from_pairs_dict(pairs_dict_after_40_rounds, char_string)
    print(f"Part 2 efficiently: {int(max(quantity_dict.values()) - min(quantity_dict.values()))}")
