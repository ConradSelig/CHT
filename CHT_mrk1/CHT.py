from CHT_mrk1 import output, hashing, classes

'''
    This file serves as the front-end interface for users importing the package.
    The only class in here is the CHT_mrk1 class itself, which should be the only class a user would typically want
    access to.
'''


class CHT:
    """
        CHT_mrk1 holds both the raw table data (built into classes) and the compiled cubic hash table itself.
    """

    def __init__(self, keys):
        self.keys = keys + ["__words__"]
        self.rows = []
        self.words = []
        self.hash_map_dict = {key: [] for key in keys}

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.rows[key]
        return self.hash_map_dict[key]

    def __setitem__(self, key, value):
        self.hash_map_dict[key] = value
        return

    def __len__(self):
        return len(self.rows)

    def get_keys(self):
        return self.keys

    def do_hash(self, show_print=False):

        if show_print:
            print("Building Cubic Hash Table...")
        # for key in CHT_mrk1
        for i, key in enumerate(self.keys):
            if show_print:
                output.progress_bar(i, len(self.keys))
            # build that keys hash table
            self.hash_map_dict[key] = hashing.build_hash_table(self, key)
        if show_print:
            output.progress_bar(len(self.keys), len(self.keys))

        return

    def add_row(self, row, do_hash=True, show_print=False):
        self.add_rows([row], do_hash, show_print)
        return

    def add_rows(self, rows, do_hash=True, show_print=False):
        # for each row in new data
        for row in rows:
            # create a new Row object with the table keys
            temp_row = classes.Row(self.keys)
            # build the new row object with the table data
            temp_row.build_from_table(row)
            # append to row to the CHT_mrk1
            self.rows.append(temp_row)
            # for each word in the new row
            for new_word in temp_row.get_words():
                # append each word to the CHT_mrk1 as a Word object
                self.words.append(classes.Word(new_word, temp_row.get("id")))
        # for each row in the CHT_mrk1 raw rows
        for row in self.rows:
            # if an ID was not found in the row or a blank ID was givin
            if row.get("id") == -1 or row.get("id") == "":
                # re-id the entire CHT_mrk1, this operation is usually overkill but the CHT_mrk1 *requires* unique IDs and this
                # is the best way to ensure that
                for new_id, id_row in enumerate(self.rows):
                    id_row.set_id(new_id)
                break
        # if a new hash needs to be made
        if do_hash:
            self.do_hash(show_print)

        return

    def get_map(self):
        return self.hash_map_dict
