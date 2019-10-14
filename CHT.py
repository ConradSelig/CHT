import prime_math
from pandas import DataFrame
from DataFrame_utils import *
import warnings
import time


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

    def add(self, row_key, col_key, val, check_table_size=True):
        """
        Add a single value to the CHT.
        :param row_key: string - key delineating the row
        :param col_key: string - key delineating the column
        :param val: any type - value to store in the table
        :param check_table_size: boolean - default is True and should only be set to False for bulk data adds.
        :return: bool - True for data added and False when a failure occurs.
        """

        # If debugging, print 3 newlines so this block of statements is easily distinguished from other blocks.
        if self.debug_mode:
            print("\n\n\n")

        # get the index of the keys from the raw table data. These functions return -1 if the row/col was not found.
        row_index = get_index_from_row(self.raw_table, row_key)
        col_index = get_index_from_col(self.raw_table, col_key)

        # check if the given keys are for a new value, if not that means an old value is being overwritten.
        if row_index == -1 or col_index == -1:
            if self.debug_mode:
                print("Cell not already known, incrementing cells_filled count.")
            # the cells_filled value is used to determine when the size of the table needs to be increased.
            self.cells_filled += 1
        else:
            if self.debug_mode:
                print("Cell value was overwritten.")
            # change the value and return. Overwriting values does not require any additional processing as the keys
            # have not changed and therefor hashes do not need to be done.
            self.raw_table.at[row_key, col_key] = val
            return True

        # set the raw table value. The raw_table is a DataFrame and will create the row/columns automatically as needed.
        self.raw_table.at[row_key, col_key] = val
        if self.debug_mode:
            print("'" + str(val) + "' has been added to the raw data table.")

        # hash the row and column. This will be used to determine the index of the item in the hash table
        hash_row = self._hash_string(str(row_key), self.table_size)
        hash_col = self._hash_string(str(col_key), self.table_size)
        if self.debug_mode:
            print("'" + str(row_key) + "' hashed to " + str(hash_row))
            print("'" + str(col_key) + "' hashed to " + str(hash_col))

        # append the index coordinates of the value in the raw table as a tuple into the hash table at the indexes
        # determined by the hashed version of the keys. The get_index_from_*() functions are called again here as
        # at least one is still -1 (item not in table) and the item does exist in the raw table now.
        self.hash_table[hash_row][hash_col].append(
                                                    (get_index_from_row(self.raw_table, row_key),
                                                     get_index_from_col(self.raw_table, col_key))
                                                  )

        if self.debug_mode:
            print("Indexes added to hash table.")
            # only print out the entire table if there are less than 10 rows and columns. This prevents very large
            # tables from being printed.
            if len(get_col_keys(self.raw_table)) < 10 and len(get_row_keys(self.raw_table)) < 10:
                print("Current raw table:")
                print(self.raw_table)
                print()
                print("Current hash table:")
                print(self.hash_table)

        return True

    def get(self, row_key, col_key):
        """
        Retrieve a single value from the CHT. This function does perform the hash requests necessary to achieve O(1).
        :param row_key: A key delineating the row
        :param col_key: A key delineating the column.
        :return: The value in the table delineated by the given row and column or None if the value could not be found.
        """

        # Hash the given keys to get the index of the value in the hash table
        row_index = self._hash_string(str(row_key), self.table_size)
        col_index = self._hash_string(str(col_key), self.table_size)

        if self.debug_mode:
            print("\n\nGetting value with row key '" + str(row_key) + "' and col key '" + str(col_key) + "'.")
            print("\tRow index =", row_index)
            print("\tCol index =", col_index)

        # For each possible value in the hash table at the hashed index
        for index_tuple in self.hash_table[row_index][col_index]:
            try:
                # get the row and col keys from the raw table at the indexes provided in the hash table
                raw_row_key = get_row_from_index(self.raw_table, index_tuple[0])
                raw_col_key = get_col_from_index(self.raw_table, index_tuple[1])
            # This error can catch if values are manually added to the hash table instead of with CHT.add()
            except IndexError:
                raw_row_key = None
                raw_col_key = None
                warnings.warn("An index error has occurred, was an index pair manually added to the hash table?",
                              UserWarning)
                # this ensures that the warning prints in the console at the correct place.
                time.sleep(0.1)
                continue

            if self.debug_mode:
                print("Checking next index tuple...")
                print("\t", index_tuple)
                print("\tRaw row key =", raw_row_key)
                print("\tRaw col key =", raw_col_key)

            # if the row and col keys from the hash table indexes match the keys given to this function
            if get_row_from_index(self.raw_table, index_tuple[0]) == row_key and \
                    get_col_from_index(self.raw_table, index_tuple[1]) == col_key:
                if self.debug_mode:
                    print("Matching value found. Value =", self.raw_table.iloc[index_tuple[0], index_tuple[1]])
                # return the value found in the raw table at the indexes provided from the hash table. The indexes must
                # be used instead of the keys otherwise a linear lookup would be performed by the DataFrame.
                return self.raw_table.iloc[index_tuple[0], index_tuple[1]]

        if self.debug_mode:
            print("No matching value found.")

        # no value was found in the table matching the given keys. Return None
        return None

    def check_table_size(self):
        return

    def re_hash(self):
        return

    @staticmethod
    def _hash_string(string, mod_val):
        """
        Return a hash index for a given key
        :param string: key to be hashed
        :param mod_val: size of the hash table. A prime should be used to avoid conflicts.
        :return: integer index for the given key based on the table size
        """
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
