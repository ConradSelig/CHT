from pandas import DataFrame


def get_val_from_index(table: DataFrame, indexes: tuple):
    return table.values[indexes[0]][indexes[1]]


def get_row_from_index(table: DataFrame, index: int):
    return table.iloc[index].name


def get_col_from_index(table: DataFrame, index: int):
    return table.keys()[index]


def get_col_keys(table: DataFrame):
    return table.keys()


def get_row_keys(table: DataFrame):
    return list(table.index.values)


def get_index_from_row(table: DataFrame, key):
    for i, k in enumerate(get_row_keys(table)):
        if k == key:
            return i
    return -1


def get_index_from_col(table: DataFrame, key):
    for i, k in enumerate(get_col_keys(table)):
        if k == key:
            return i
    return -1
