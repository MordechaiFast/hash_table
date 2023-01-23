import pytest
from hashtable import HashTable, Item

# Create an empty table
def test_create_hashtable():
    assert HashTable() is not None

# Values() method is needed for other tests
def test_values_method():
    table = HashTable()
    table._item_list = [Item('this', str), Item(512, int), Item(True, bool)]
    # not hashed, and not added by the setitem method
    assert str  in table.values()
    assert int  in table.values()
    assert bool in table.values()

# Don't have the table prevent itself from holding None
def test_new_table_does_not_contain_None():
    table = HashTable()
    assert None not in table.values()

def test_can_accept_None_value():
    table = HashTable()
    table[0] = None
    assert None in table.values()

# Create data, a key-value, in the existing table
@pytest.fixture
def hash_table():
    table = HashTable()
    table[512]    = int
    table['this'] = str
    table[True]   = bool
    return table

def test_insert_values(hash_table):
    assert str  in hash_table.values()
    assert int  in hash_table.values()
    assert bool in hash_table.values()

def test_hash_collision(hash_table):
    assert len(hash_table) == 3
    hash_table[2] = 0
    # Has the same hash as 512
    assert len(hash_table) == 4

# Read the value for an existing key
def test_read_value_for_key(hash_table):
    assert hash_table['this'] is str
    assert hash_table[512]    is int
    assert hash_table[True]   is bool

def test_raises_KeyError_for_missing_key(hash_table):
    with pytest.raises(KeyError) as err:
        hash_table['key']
    assert 'key' in err.value.args

# Check for the existance of a key
def test_find_existance_of_key(hash_table):
    assert 'this' in hash_table
    assert 512    in hash_table
    assert True   in hash_table

def test_find_nonexistance_of_key(hash_table):
    assert 'key' not in hash_table

# .get function to return value for existing key
# and None or specified default for nonexistant key

def test_get_value_for_key(hash_table):
    assert hash_table.get('this') is str
    assert hash_table.get(512)    is int
    assert hash_table.get(True)   is bool

def test_get_returns_None_for_missing_key(hash_table):
    assert hash_table.get('key') is None

def test_get_returns_default_for_missing_key(hash_table):
    assert hash_table.get('key', 'default') == 'default'

def test_get_value_for_key_with_default(hash_table):
    assert hash_table.get('this', 'default') is str
    assert hash_table.get(512,    'default') is int
    assert hash_table.get(True,   'default') is bool

# Change the value of an existing key
def test_change_keys_value(hash_table):
    assert hash_table['this'] is str
    hash_table['this'] = 'that'
    assert hash_table['this'] == 'that'
    assert hash_table.get('this') ==  'that'

# Delete a key-value
def test_delete_key(hash_table):
    assert 'this' in hash_table
    assert hash_table['this'] is str
    del hash_table['this']
    assert 'this' not in hash_table
    with pytest.raises(KeyError) as err:
        hash_table['this']
    assert 'this' in err.value.args

def test_delete_value(hash_table):
    assert str in hash_table.values()
    del hash_table['this']
    assert str not in hash_table.values()

def test_delete_item(hash_table):
    assert len(hash_table) == 3
    del hash_table['this']
    assert len(hash_table) == 2
    assert 'this' not in hash_table.keys()

def test_delete_missing_key(hash_table):
    assert 'key' not in hash_table
    with pytest.raises(KeyError) as err:
        del hash_table['key']
    assert 'key' in err.value.args

def test_retrevial_after_deletion_of_hash_collision():
    table = HashTable(((4,0), (8,0)))
    assert hash(4) % 4 == hash(8) % 4
    del table[4]
    assert table[8] == 0

def test_del_hash_collision_dosent_allow_for_duplicate_keys():
    table = HashTable(((4,0), (8,0)))
    assert hash(4) % 4 == hash(8) % 4
    del table[4]
    table[8] = 10
    assert 0 not in table.values()

# Access a list of key-value pairs, keys, or values
def test_item_retrieval(hash_table):
    assert ('this', str) in hash_table.items()
    assert (512,    int) in hash_table.items()
    assert (True,  bool) in hash_table.items()

def test_items_doesnt_return_Nones(hash_table):
    assert None not in hash_table.items()

def test_key_retrieval(hash_table):
    assert 'this' in hash_table.keys()
    assert 512    in hash_table.keys()
    assert True   in hash_table.keys()

def test_values_returns_repeates(hash_table):
    hash_table[True] = int
    assert len([*hash_table.values()]) == 3

def test_items_returns_copy(hash_table):
    assert [*hash_table.items()] is not [*hash_table.items()]
    assert [*hash_table.items()] == [*hash_table.items()]

def test_keys_returns_copy(hash_table):
    assert [*hash_table.keys()] is not [*hash_table.keys()]
    assert [*hash_table.keys()] == [*hash_table.keys()]

def test_values_returns_copy(hash_table):
    assert [*hash_table.values()] is not [*hash_table.values()]
    assert [*hash_table.values()] == [*hash_table.values()]

# The length should report the number of items filled in the table
def test_length_is_only_filled_key_values(hash_table):
    assert len(hash_table) == 3

# table itself should be iterable
def test_instance_is_iterable(hash_table):
    for key in hash_table:
        assert key in ['this', 512, True]

# Convert to a dictionary
def test_dict_comprehention(hash_table):
    dictionary = dict(hash_table.items())
    assert {*dictionary.keys() } == {*hash_table.keys() }
    assert {*dictionary.items()} == {*hash_table.items()}
    assert all((value in hash_table.values()) for value in dictionary.values())
    assert all((value in dictionary.values()) for value in hash_table.values())

# Representation
def test_table_string_conversion(hash_table):
    assert str(hash_table) in {
        "{'this': <class 'str'>, 512: <class 'int'>, True: <class 'bool'>}",
        "{'this': <class 'str'>, True: <class 'bool'>, 512: <class 'int'>}",
        "{512: <class 'int'>, 'this': <class 'str'>, True: <class 'bool'>}",
        "{512: <class 'int'>, True: <class 'bool'>, 'this': <class 'str'>}",
        "{True: <class 'bool'>, 'this': <class 'str'>, 512: <class 'int'>}",
        "{True: <class 'bool'>, 512: <class 'int'>, 'this': <class 'str'>}",
    }

# Update with dictionary
def test_update_with_dict(hash_table):
    hash_table.update({'that': str, 1: int, 2: int})
    assert hash_table['that'] == str
    assert len(hash_table) == 5
    # 1 replaces True

def test_create_from_dict():
    table = HashTable({'this': str, 512: int, True: bool})
    assert table['this'] is str
    assert table[512]    is int
    assert table[True]   is bool

def test_create_from_items(hash_table):
    new = HashTable(hash_table)
    assert new['this'] is str
    assert new[512]    is int
    assert new[True]   is bool

# Equality
def test_equals_self(hash_table):
    assert hash_table == hash_table

def test_equals(hash_table):
    other = HashTable()
    other['this'] = str
    other[512] = int
    other[True] = bool

    assert other is not hash_table
    assert other == hash_table

def test_equals_different_order(hash_table):
    other = HashTable()
    other[True] = bool
    other['this'] = str
    other[512] = int

    assert other is not hash_table
    assert other == hash_table

def test_equals_dict(hash_table):
    assert hash_table == {'this': str, 512: int, True: bool}
    
def test_not_equals(hash_table):
    other = HashTable()
    other['that'] = str

    assert other != hash_table

def test_not_equals_different_type(hash_table):
    assert hash_table != ['this', 512, True]