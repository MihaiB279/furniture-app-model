import glob
import re

import numpy as np
import pandas as pd


def change_currency(x):
    if type(x) is float:
        print(x)
    elif not x[0].isdigit():
        x = x[1:]
    x = x.replace(',', '')
    return round(int(x) * 0.055 * 1.5)


def modify_list_bar(items):
    items[:len(items) - 1] = [s + '\'' for s in items[:len(items) - 1]]
    items[0] = '[\'Material: ' + items[0]
    del items[1]
    items[-1] = '\'Delivery condition: ' + items[-1]
    return ','.join(items)


def modify_list_recliner(items):
    items[:len(items) - 1] = [s + '\'' for s in items[:len(items) - 1]]
    items_1 = items[1].split(' ')
    items[1] = ' \'' + items_1[1] + ' ' + items_1[2][:len(items_1[2]) - 1] + ': ' + items_1[0] + '\''
    return ','.join(items)


def modify_list_kitchen(items):
    items[:len(items) - 1] = ['\'' + s + '\'' for s in items[:len(items) - 1]]
    items[len(items) - 1] = '\'Delivery condition: ' + items[len(items) - 1] + '\''

    return '[' + ','.join(items) + ']'


def modify_list_sofabed(items):
    items[:len(items) - 1] = [s + '\'' for s in items[:len(items) - 1]]
    if 'Shape' not in items[0]:
        items.insert(0, '[\'Shape: not specified\'')
        items[1] = items[1][1:]
    return ','.join(items)


def modify_list_tv_unit(items):
    items[:len(items)] = ['\'' + s + '\'' for s in items[:len(items)]]
    items[3] = items[3].replace(", ", "', '")
    return '[' + ','.join(items) + ']'


def delete_duplicates(csv):
    duplicate_rows = []
    for index1, row1 in csv.iterrows():
        for index2, row2 in csv.iterrows():
            if index1 not in duplicate_rows:
                if index1 != index2 and row1['furniture_type'] == row2['furniture_type'] and row1['name'] \
                        == row2['name'] and row1['company'] == row2['company']:
                    duplicate_rows.append(index2)

    return duplicate_rows


def delete_dining(csv):
    to_delete_rows = []
    for index, row in csv.iterrows():
        if 'Table Top Material' not in row['product_details']:
            to_delete_rows.append(index)

    return to_delete_rows


def delete_bed(csv):
    to_delete_rows = []
    for index, row in csv.iterrows():
        if 'Recommended Mattress Size' in row['product_details']:
            to_delete_rows.append(index)

    return to_delete_rows


def repair_details(name, csv):
    duplicated_rows = delete_duplicates(csv)
    csv.drop(duplicated_rows, inplace=True)

    filtered_list = None
    if name == 'bar':
        filtered_list = list(map(lambda x: modify_list_bar(x), csv['product_details']))
    if name == 'kitchen':
        filtered_list = list(map(lambda x: modify_list_kitchen(x), csv['product_details']))
    if name == 'recliner':
        filtered_list = list(map(lambda x: modify_list_recliner(x), csv['product_details']))
    if name == 'sofabed':
        filtered_list = list(map(lambda x: modify_list_sofabed(x), csv['product_details']))
    if name == 'bed':
        delete_rows = delete_bed(csv)
        csv.drop(delete_rows, inplace=True)
    if name == 'dining':
        delete_rows = delete_bed(csv)
        csv.drop(delete_rows, inplace=True)
    if name == 'tvunit':
        filtered_list = list(map(lambda x: modify_list_tv_unit(x), csv['product_details']))

    if filtered_list is not None:
        csv['product_details'] = filtered_list


def main():
    companies = ['Dedeman', 'Jysk', 'Ikea', 'Casa Rusu', 'Mobila Casa', 'Mob Expert', 'Casa Magica', 'FurnitureForYou']
    path = "cvs/*.csv"
    for file in glob.glob(path):
        csv_input = pd.read_csv(file)
        csv_input['company'] = np.random.choice(companies, size=len(csv_input), replace=True)
        reg_str = "<li class=\"_21Ahn-\">(.*?)</li>"
        csv_input['product_details'] = csv_input['product_details'].apply(lambda x: re.findall(reg_str, x))
        repair_details(file.split('\\')[1].split('.csv')[0], csv_input)
        csv_input['discounted_price'] = csv_input['discounted_price'].apply(lambda x: change_currency(x))
        csv_input['original_price'] = csv_input['original_price'].apply(lambda x: change_currency(x[1:]))
        csv_input.to_csv(file, index=False)


if __name__ == "__main__":
    main()
