from typing import (NamedTuple, Any, Hashable, Optional, Iterator,
 ItemsView, KeysView, ValuesView)

class Item(NamedTuple):
    key: Hashable
    value: Any

NoDefault = object()

class HashTable():
    """dict clone"""

    def __init__(self, seed=None, **kwargs) -> None:
        # Prep. input
        if seed is None:
            seed = {}
        elif type(seed) not in (HashTable, dict):
            seed = dict(seed)
        seed.update(kwargs)
        # Prep. self
        self._capacity = round(8/3 * len(seed)) or 2
        # With lazy rehashing: 2 * len(seed) or 2        
        self.clear()
        self.update(seed)

    # High-level functions
    def copy(self) -> 'HashTable':
        return (self.__class__)(self)

    def clear(self) -> None:
        self._item_list = [None] * self._capacity
        
    def update(self, dictionary: dict) -> None:
        for key, value in dictionary.items():
            self[key] = value

    @classmethod
    def fromkeys(cls, keys: Iterator[Hashable], value=None) -> 'HashTable':
        new = cls()
        for key in keys:
            new[key] = value
        return new

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def setdefault(self, key:Hashable, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

    def pop(self, key: Hashable, default: Optional[Any] = NoDefault) -> Any:
        try:
            value = self[key]
            del self[key]
        except KeyError as err:
            if default is NoDefault:
                raise err
            else:
                value = default
        return value

    def items(self) -> ItemsView:
        yield from [item for item in self._item_list if item]

    def keys(self) -> KeysView:
        yield from [item.key for item in self.items()]

    def values(self) -> ValuesView:
        yield from [item.value for item in self.items()]
    
    # Overload methods
    def __setitem__(self, key: Hashable, value: Any) -> None:
        self._eager_rehash()
        index = self._find_open_or_index(key)
        self._item_list[index] = Item(key, value)
  
    def __getitem__(self, key: Hashable) -> Any:
        index = self._find_index(key)
        return self._item_list[index].value
            
    def __delitem__(self, key: Hashable) -> None:
        index = self._find_index(key)
        self._item_list[index] = False

    def __or__(self, other: Any) -> "HashTable":
        copy = self.copy()
        copy.update(other)
        return copy

    def __ror__(self, other: Any) -> "HashTable":
        copy = other.copy()
        copy.update(self)
        return copy

    def __ior__(self, other: Any) -> None:
        self.update(other)

    def __eq__(self, other: object) -> bool:
        try:
            return {*self.items()} == {*other.items()}
        except AttributeError:
            return False

    def __gt__(self, other: object) -> bool:
        return {*self.items()} > {*other.items()}
        
    def __lt__(self, other: object) -> bool:
        return {*self.items()} < {*other.items()}
        
    def __contains__(self, key: Any) -> bool:
        return key in self.keys()

    def __len__(self) -> int:
        return len([*self.items()])

    def __iter__(self) -> Iterator:
        yield from self.keys()

    def __str__(self) -> str:
        item_list = [f"{key!r}: {value!r}" for key, value in self.items()]
        return "{" + ", ".join(item_list) + "}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    # Internals
    def _find_open_or_index(self, key: Hashable) -> int:
        for index in self._loop(key):
            item = self._item_list[index]
            if item is False:       # i.e. cleared
                continue            # don't overwrite, to avoid duplicates
            if (item is None        # i.e. unused
             or item.key == key):   # Existing key to update
                return index
        self._rehash()      # Lazy rehashing
        return self._find_open_or_index(key)              
  
    def _find_index(self, key: Hashable) -> int:
        for index in self._loop(key):
            item = self._item_list[index]
            if item is None:        # Does not exist
                break
            if item is False:       # Deleted index
                continue 
            if item.key == key:
                return index
        raise KeyError(key)

    def _loop(self, key: Hashable) -> Iterator[int]:
        start = hash(key) % self._capacity
        for index in range(start, start + self._capacity):
            yield index % self._capacity

    def _eager_rehash(self) -> None:
        used_places = [item for item in self._item_list
                       if item is not None]
        if len(used_places) / self._capacity >= .75:
            self._rehash()

    def _rehash(self) -> None:
        copy = self.copy()   # with twice the capacity of current list
        self._item_list = copy._item_list
        self._capacity = copy._capacity
