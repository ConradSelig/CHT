import prime_math
from pandas import DataFrame
from DataFrame_utils import *


class CHT:

    def __init__(self):
        # 17 is an arbitrary primes chosen as a min-size.
        self.table_size = 17

        # raw table that holds all of the actual data.
        self.raw_table = DataFrame()
        # 2D hash_table holding all of the locations for the data in the raw_table
        self.hash_table = [[[] for _ in range(self.table_size)] for _ in range(self.table_size)]
        # When the size of the hash_table is increased, all of the data is copied into this variable before being
        # re-hashed into the actual hash_table.
        self.temp_table = []

        # Integer count of the number of values in the hash_table. This is used to determine when the table
        # needs to be expanded.
        self.cells_filled = 0
        self.cell_count = self.table_size * self.table_size

        # boolean value, if True debug text is printing throughout class. If False the CHT does not print anything.
        self.debug_mode = False

    def set_debug_mode(self, new_mode):
        self.debug_mode = new_mode
        return

    def add_val(self, row_key, col_key, val, check_table_size=True):
        """
        :param row_key: string - key delimiting the row
        :param col_key: string - key delimiting the column
        :param val: any type - value to store in the table
        :param check_table_size: boolean - default is True and should only be set to False for bulk data adds.
        :return: bool - True for data added and False when a failure occurs.
        """

        if self.debug_mode:
            print("\n\n\n")

        row_index = get_index_from_row(self.raw_table, row_key)
        col_index = get_index_from_row(self.raw_table, col_key)

        # check if the given keys are for a new value, if not that means an old value is being overwritten.
        if row_index == -1 or col_index == -1:
            if self.debug_mode:
                print("Cell not already known, incrementing cells_filled count.")
            self.cells_filled += 1

        self.raw_table.at[row_key, col_key] = val
        if self.debug_mode:
            print("'" + str(val) + "' has been added to the raw data table.")

        hash_row = self._hash_string(str(row_key), self.table_size)
        hash_col = self._hash_string(str(col_key), self.table_size)
        if self.debug_mode:
            print("'" + str(row_key) + "' hashed to " + str(hash_row))
            print("'" + str(col_key) + "' hashed to " + str(hash_col))

        self.hash_table[hash_row][hash_col].append(
                                                    (get_index_from_row(self.raw_table, row_key),
                                                     get_index_from_col(self.raw_table, col_key))
                                                  )
        if self.debug_mode:
            print("Indexes added to hash table.")

            if len(get_col_keys(self.raw_table)) < 15:
                print("Current raw table:")
                print(self.raw_table)
                print()
                print("Current hash table:")
                print(self.hash_table)

        return

    def check_table_size(self):
        if self.cells_filled * 1.33 > self.cell_count:
            current_prime = self.table_size[0]
            # use the prime_math file to get the next prime larger than the current prime.
            next_prime = prime_math.next_prime(current_prime)

            if self.debug_mode:
                print("Table size checked. Increasing size.")
                print("\tLast Size:", current_prime, "x", current_prime)
                print("\tNext Size:", next_prime, "x", next_prime)

            # update the class functions
            self.table_size = (next_prime, next_prime)
            self.cell_count = next_prime * next_prime

            # re-hash the table
            self.re_hash()
        else:
            if self.debug_mode:
                print("Table size checked. No size change required.")
        return

    def re_hash(self):
        # set the temp_table to the current table so no data is lost
        self.temp_table = self.table
        # reset the table to an empty table
        self.hash_table = [[None for _ in range(self.table_size[0])] for _ in range(self.table_size[1])]

        for row_index, row in enumerate(self.temp_table):
            for col_index, val in enumerate(row):
                self.add_val(self.row_keys[row_index], self.col_keys[col_index], val, check_table_size=False)

        # reset the temp_table so that storage space is not being used
        self.temp_table = []
        return

    @staticmethod
    def _hash_string(string, mod_val):
        # set the index value to 0 as a baseline
        next_index_value = 0
        # for each character in the string
        for char in str(string):
            # add that characters value to the total
            next_index_value += ord(char)
        # mod that value by the table size
        next_index_value %= mod_val
        # return the generated hash value
        return next_index_value
