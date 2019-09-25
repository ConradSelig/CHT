import prime_math


class CHT:

    def __init__(self):
        # (17, 17) are arbitrary primes chosen as a min-size.
        self.min_table_size = (17, 17)
        # Tuple holding X, Y size of table. This is used instead of the len() because the table is sized to be the
        # smallest primes larger than len().
        self.table_size = self.min_table_size

        # raw table that holds all of the actual data.
        self.raw_table = []
        # 2D hash_table holding all of the locations for the data in the raw_table
        self.hash_table = [[None for _ in range(self.table_size[0])] for _ in range(self.table_size[1])]
        # When the size of the hash_table is increased, all of the data is copied into this variable before being
        # re-hashed into the actual hash_table.
        self.temp_table = []

        # row keys and col keys. These are used to re-hash the table when the size changes, as well as verify hash
        # requests
        self.row_keys = [None] * self.table_size[0]
        self.col_keys = [None] * self.table_size[0]

        # Integer count of the number of values in the hash_table. This is used to determine when the table
        # needs to be expanded.
        self.cells_filled = 0
        self.cell_count = self.table_size[0] * self.table_size[1]

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

        # check for row_key in rows
        for i, key in enumerate(self.row_keys):
            if key == row_key:
                raw_row_index = i
                break
        else:
            raw_row_index = -1

        # check for col_key in cols
        for i, key in enumerate(self.col_keys):
            if key == col_key:
                raw_col_index = i
                break
        else:
            raw_col_index = -1

        if raw_row_index == -1 or raw_col_index == -1:
            # if adding new data increment cells_filled
            self.cells_filled += 1

        # add new row/col/row+col to row and col lists
        if raw_row_index == -1:
            self.row_keys.append(row_key)
            raw_row_index = len(self.row_keys)
        if raw_col_index == -1:
            self.col_keys.append(col_key)
            raw_col_index = len(self.col_keys)

        # add new val to raw_table
        self.raw_table[raw_row_index][raw_col_index] = val

        # hash the two values to get the table indexes
        row_index = self._hash_string(row_key, self.table_size[0])
        col_index = self._hash_string(col_key, self.table_size[1])

        return

    def old_add_val(self, row_key, col_key, val, check_table_size=True):

        # hash the two values to get the table indexes
        row_index = self._hash_string(row_key, self.table_size[0])
        col_index = self._hash_string(col_key, self.table_size[1])

        if self.debug_mode:
            print("Row key hashed:", row_key, "=>", row_index)
            print("Column key hashed:", col_key, "=>", col_index)

        # if there is no value in the target cell (ie target cell is NOT being updated)
        if self.debug_mode:
            print(self.table[row_index][col_index])
        if self.table[row_index][col_index] is None:
            # update the cells filled count
            self.cells_filled += 1

            if self.debug_mode:
                print("Value added to new cell. Cells Filled value updated.")
        else:
            if self.debug_mode:
                print("Cell value updated. Cells Filled goes unchanged.")

        # set the target cell of the table to the given value
        self.table[row_index][col_index] = val
        # add the keys to their respective lists
        self.row_keys[row_index] = row_key
        self.col_keys[col_index] = col_key

        # Check the hash state
        if check_table_size:

            if self.debug_mode:
                print("Checking the size of the hash table.")

            self.check_table_size()

        if self.debug_mode:
            print(self.table)
            print("\n")

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
    def _hash_string(self, string, mod_val):
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
