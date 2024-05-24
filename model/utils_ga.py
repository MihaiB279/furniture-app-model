from model.clustering import cluster_item
from model.utils import check_all_no_preference, get_list

INF = float('inf')


def evaluation(furniture, positions, budget):
    budget_furniture = 0
    for i in range(len(positions)):
        furniture_add = furniture[list(furniture.keys())[i]][positions[i]]
        budget_furniture = budget_furniture + float(furniture_add['Price'])
    score = abs(budget - budget_furniture)
    return score


def get_furniture_size(dimensions):
    dim_cm = dimensions.split('(')[0]
    split_dim = dim_cm.split(' x ')
    split_dim_numbers = [value.replace(' ', '').replace('cm', '') for value in split_dim]
    return split_dim_numbers


def get_right_furniture(furniture_details):
    furniture = {}
    for single_furniture in furniture_details:
        name = single_furniture.furnitureType
        details_as_dict = get_list(single_furniture.details)
        furniture_available = cluster_item(name, details_as_dict)
        for item in furniture_available:
            is_good = True
            for attribute_name, attribute_value in details_as_dict.items():
                if attribute_name not in item[0].keys() or attribute_value != "No preferences" and attribute_value != \
                        item[0][attribute_name]:
                    is_good = False
                    break
            if is_good:
                furniture[name] = item
                break
        if name not in furniture:
            if check_all_no_preference(details_as_dict):
                furniture[name] = furniture_available[0]
            else:
                return name
    return furniture
