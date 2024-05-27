import re


def get_list(string):
    input_string = string.strip("[]")
    input_list = re.split(r"',\s*'", input_string)

    result_dict = {}
    for item in input_list:
        try:
            key, value = item.strip("'").split(':', 1)
            result_dict[key.strip()] = value.strip()
        except ValueError as ex:
            print(ex)

    return result_dict


def check_all_no_preference(data):
    if not all(value == 'No preferences' for value in data.values()):
        return False
    return True


def get_index_off_generated(generated, available):
    list_indexes = []
    for single_list in generated:
        single_list_index = []
        for index_gen, furniture_generated in enumerate(single_list):
            for index, furniture_available in enumerate(available[index_gen]):
                if furniture_available['Name'] == furniture_generated.name and \
                        furniture_available['Company'] == furniture_generated.company:
                    single_list_index.append(index)
                    break
        if len(single_list_index) == len(single_list):
            list_indexes.append(single_list_index)
    return list_indexes

