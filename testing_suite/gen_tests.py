from CHT_mrk1 import output, hashing, classes
from CHT_mrk1.CHT import CHT
import CHT


def initialize_test():

    print("=" * 100)
    print("\nInitialize Test")
    test_CHT = CHT.CHT()
    if type(test_CHT) is CHT.CHT:
        print("Passed Test")
    else:
        print("FAILED TEST")

    return


def add_row_test():

    print("=" * 100)
    print("\nAdd Row Test")
    test_CHT = CHT.CHT()
    # test_CHT.set_debug_mode(True)
    test_CHT.add("Hello", "World", "HelloWorld")

    if test_CHT.hash_table == [[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [(0, 0)], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]]:
        print("Passed Test")
    else:
        print("FAILED TEST")

    return


def add_many_rows_test():

    print("=" * 100)
    print("\nAdd Many Rows Test")
    test_CHT = CHT.CHT()
    # test_CHT.set_debug_mode(True)
    test_CHT.add("Hello", "World", "val")
    test_CHT.add("New", "Value", "new")
    test_CHT.add("New2", "Value2", "second new")
    test_CHT.add("Hello", "Value3", "one nest")
    test_CHT.add("New", "Value2", "twice nest")

    print("Table Size:", test_CHT.cells_filled, "(Expected Size: 5)")

    if test_CHT.hash_table == [[[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [(0, 0)], [], [], [], [], [], [(0, 3)]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [(2, 2)], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [(1, 2)], [(1, 1)]], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]]\
            and test_CHT.cells_filled == 5:
        print("Passed Test")
    else:
        print("FAILED TEST")

    return


def get_value_test():

    print("=" * 100)
    print("\nGet Value Test")
    test_CHT = CHT.CHT()

    test_CHT.add("Hello", "World", "HelloWorld!")
    return_val = test_CHT.get("Hello", "World")

    if return_val == "HelloWorld!":
        print("Passed Test")
    else:
        print("FAILED TEST")

    return


def conflict_test():

    print("=" * 100)
    print("\nConflict Test")
    test_CHT = CHT.CHT()

    test_CHT.add("Row 1", "Col 1", "val1")
    test_CHT.add("Row 2", "Col 1", "val2")

    test_CHT.hash_table[2][10].insert(0, (1, 0))

    if test_CHT.get("Row 1", "Col 1") == "val1":
        print("Passed Test")
    else:
        print("FAILED TEST")

    return


def hash_overwrite_test():

    print("=" * 100)
    print("\nHash Overwrite Test")
    test_CHT = CHT.CHT()

    test_CHT.add("Row 1", "Col 1", "val1")
    test_CHT.add("Row 2", "Col 1", "val2")

    test_CHT.hash_table[2][10].insert(0, (1, 0))
    test_CHT.hash_table[2][10].insert(0, (2, 0))

    if test_CHT.get("Row 1", "Col 1") == "val1":
        print("Passed Test")
    else:
        print("FAILED TEST")

    return


def overwrite_value_test():

    print("=" * 100)
    print("\nOverwrite Value Test")
    test_CHT = CHT.CHT()

    test_CHT.add("Row 1", "Col 1", "val1")
    test_CHT.add("Row 1", "Col 1", "overwritten")

    if test_CHT.get("Row 1", "Col 1") == "overwritten":
        print("Passed Test")
    else:
        print("FAILED TEST")

    return
