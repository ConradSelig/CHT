from cht import hashing
from cht import output
import re


class CHT:
    """
        CHT holds both the raw table data (built into classes) and the compiled cubic hash table itself.
    """

    def __init__(self, keys, values):
        self.keys = keys + ["__words__"]
        self.raw_values = values
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
        # for key in CHT
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
            temp_row = Row(self.keys)
            # build the new row object with the table data
            temp_row.build_from_table(row)
            # append to row to the CHT
            self.rows.append(temp_row)
            # for each word in the new row
            for new_word in temp_row.get_words():
                # append each word to the CHT as a Word object
                self.words.append(Word(new_word, temp_row.get("id")))
        # for each row in the CHT raw rows
        for row in self.rows:
            # if an ID was not found in the row or a blank ID was givin
            if row.get("id") == -1 or row.get("id") == "":
                # re-id the entire CHT, this operation is usually overkill but the CHT *requires* unique IDs and this
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


class Word:
    """
     The word class is only used in the __words__ array where the row index is no longer associated with the word itself
        and therefor that index must be stored with the word.
    """

    def __init__(self, word, word_id):
        self.word = word
        self.id = word_id

    # this function is an override of the getattr() function that allows for use as a class function
    def get(self, attr):
        return getattr(self, attr)


class Row:
    """
    The row class holds RAW data only, hash requests cannot be made to the row class.
    For the hashed version of the row class see the HashMapVal class.
    """

    def __init__(self, attrs):
        self.attrs = attrs
        for key in attrs:
            setattr(self, key, "")
        self.id = -1

    def __dir__(self):
        return self.attrs

    def compare(self, other):
        local = [str(getattr(self, key)) for key in [attr for attr in self.attrs if "__" not in attr]]
        foreign = [str(getattr(other, key)) for key in [attr for attr in self.attrs if "__" not in attr]]
        return local == foreign

    def build_from_table(self, values):
        for index, key in enumerate(self.attrs):
            try:
                if key == "id":
                    try:
                        setattr(self, key, int(values[index]))
                    except ValueError:
                        setattr(self, key, -1)
                else:
                    setattr(self, key, values[index])
            except IndexError:
                setattr(self, key, "")
        return

    def print_all(self):
        for attr in self.attrs:
            print(attr, " = ", getattr(self, attr))
        return

    def print_filled(self):
        for attr in self.attrs:
            if getattr(self, attr) != "":
                print(attr, " = ", getattr(self, attr))
        return

    def get_values(self):
        values = []
        for attr in [attr for attr in self.attrs if "__" not in attr]:
            values.append(getattr(self, attr))
        return values

    def get_csv_list(self, w):
        # create the formatting string here, as it cannot be done in-place
        format_string = '{:>' + str(w) + '}'

        str_vals = []
        for val in self.get_values():
            val = str(val)
            if len(val) > w - 10:
                val = val[:w - 10] + "..."
            str_vals.append(format_string.format(val))
        return "".join(str_vals)

    def set_id(self, new_id):
        self.id = new_id
        return

    def get(self, attr):
        return getattr(self, attr)

    def get_words(self):
        words = ""
        for attr in self.attrs:
            words += str(getattr(self, attr)) + " "
        words = re.sub("[!\"#$%&'()*+,\\-./:;<=>?@[\\]^_`{|}~]", "", words)
        return words.split()


class HashMapValue:
    """
    The CHT is built out of instances of this class. Hash requests should never be made to this class and should always
    be made through the CHT holding this classes objects.
    """

    def __init__(self):
        self.key = ""
        self.values = []

    def __str__(self):
        if self.key is not "":
            return str(self.key) + ": " + str(self.values)
        else:
            return "Null: [Null]"

    def set_key(self, key):
        self.key = key

    def add_val(self, value):
        self.values.append(value)
        return

    def get_key(self):
        return self.key

    def get_values(self):
        return self.values
