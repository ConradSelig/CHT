from CHT_mrk1 import output, hashing, classes
from CHT_mrk1.CHT import CHT


def run_tests():

    test_keys = ["Col0", "Col1", "Col2"]
    test_rows = [["Row 0", 1, 2],
                 ["Row 1", 3, 4],
                 ["Row 2", 5, 6]]
    my_cht = CHT(test_keys)

    my_cht.add_row(test_rows[0], do_hash=False)
    my_cht.add_rows(test_rows[1:], do_hash=True)

    print(my_cht.get_map())
    print(my_cht[hashing.lookup_hash("Col2", 6, my_cht)[0]].get_values())

    return
