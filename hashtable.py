from typing import NamedTuple, Any, Hashable, Iterator, ItemsView, KeysView, ValuesView

class Item(NamedTuple):
    key: Hashable
    value: Any

class HashTable():
    """dict clone"""

    def __init__(self, dictonary: dict = {}, **kwargs) -> None:
        if type(dictonary) not in (HashTable, dict):
            dictonary = dict(dictonary)
        dictonary.update({**kwargs})
        capacity = round(8/3 * len(dictonary)) or 2
        self._item_list = [None] * capacity
        self.update(dictonary)

    def update(self, dictionary: dict) -> None:
        for key in dictionary:
            self[key] = dictionary[key]

    def _loop(self, key) -> Iterator[int]:
        length = len(self._item_list)
        start = hash(key) % length
        for index in range(start, start + length):
            yield index % length

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if (sum([1 for item in self._item_list if item is not None])
          / len(self._item_list) >= .75):
            copy = HashTable(self.items())   # with twice the current capacity
            self._item_list = copy._item_list
        for index in self._loop(key):
            item = self._item_list[index]
            if item is False:       # i.e. cleared
                continue            # don't overwrite, to avoid duplicates
            if item is None or item.key == key:
                self._item_list[index] = Item(key, value)
                return
    
    def __getitem__(self, key) -> Any:
        for index in self._loop(key):
            item = self._item_list[index]
            if item is None:
                break
            if item and item.key == key:
                return item.value
        raise KeyError(key, 'Key does not exist')
    
    def get(self, key, default=None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key) -> None:
        for index in self._loop(key):
            item = self._item_list[index]
            if item is None:
                break
            if item and item.key == key:
                self._item_list[index] = False
                return
        raise KeyError(key, 'Key does not exist')

    def __contains__(self, key) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False

    def items(self) -> ItemsView:
        yield from [item for item in self._item_list if item]

    def keys(self) -> KeysView:
        yield from [item.key for item in self.items()]

    def values(self) -> ValuesView:
        yield from [item.value for item in self.items()]

    def __eq__(self, other: object) -> bool:
        try:
            return {*self.items()} == {*other.items()}
        except AttributeError:
            return False

    def __len__(self) -> int:
        return len([*self.items()])

    def __iter__(self) -> Iterator:
        yield from self.keys()
    
    def __str__(self) -> str:
        item_list = []
        for key, value in self.items():
            item_list.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(item_list) + "}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"