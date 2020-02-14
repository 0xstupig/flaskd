from models.base import db


def replace_array(array1: list, array2: list, comparator, is_delete=False):
    existed_table = {comparator(item): item for item in array1}
    new_table = {comparator(item): item for item in array2}

    for item in array1:
        key = comparator(item)

        if new_table.get(key):
            continue

        array1.remove(item)
        if is_delete:
            db.session.delete(item)

    for item in array2:
        key = comparator(item)

        if existed_table.get(key):
            continue

        existed_table[key] = item
        array1.append(item)
