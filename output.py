def print_table_data(CHT, width: int):

    # create the formatting string here, as it cannot be done in-place
    format_string = '{:>' + str(width) + '}'

    # if there is no data, output that
    if not CHT.raw_values:
        print('No data found.')
    # else data exists
    else:
        # for each column of data
        for col in CHT.keys:
            # output the header row
            print(format_string.format(col + ":"), end="")
        # output newline
        print("")
        # for each line of each event
        for row in CHT.raw_values:
            # for each column in that events data
            for col in row:
                # output with the same formatting as the header row
                if len(col) > width-5:
                    col = col[:width - 5] + "..."
                print(format_string.format(col), end="")
            # output newline
            print("")
    return


def progress_bar(marks: int, total: int):
    print("Current Progress: " + str(marks) + " / " + str(total))
    print("[", end="")
    if total > 0:
        for mark in range(marks - 1):
            print("=", end="")
        if marks > 0 and marks != total:
            print(">", end="")
        elif marks == total:
            print("=", end="")
        for dot in range(total - marks):
            print(".", end="")
    print("]")
    return


def get_cht_efficiency(CHT):
    big_o = 0  # Worst
    omega = ""  # Best
    theta = 0  # Average
    total_hashed_lists = 0
    total_hashed_words = 0

    # for each of the columns
    for key in CHT.keys:
        # for each of the index list in that column
        for hash_map_val in CHT.hash_map_dict[key]:
            # if there are more indexes in that list than the last worst case
            if len(hash_map_val.values) > big_o:
                # set new big O
                big_o = len(hash_map_val.values)
            # if one of the following:
                # omega has not been set yet
                # length of indexes is less than omega and list of index is not empty
            if isinstance(omega, str) or (len(hash_map_val.values) < omega and len(hash_map_val.values) != 0):
                omega = len(hash_map_val.values)

    # for each index in the words list
    for hash_map_val in CHT.hash_map_dict["__words__"]:
        # if there are more than 0 words
        if len(hash_map_val.values) > 0:
            total_hashed_lists += 1
            total_hashed_words += len(hash_map_val.values)

    try:
        theta = total_hashed_words / total_hashed_lists
    # divides by zero if the table is empty
    except ZeroDivisionError:
        theta = 0

    # omega is 0 if the table is empty, however omega as a concept cannot be less than 1 (instant lookup)
    if omega == 0:
        omega = 1

    return big_o, omega, theta
