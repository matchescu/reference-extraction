from collections.abc import Iterable
from typing import Any, Iterator


class Record:
    def __init__(self, value: Iterable, source: str | None = None) -> None:
        self.__source = source or ""
        tuples = list(self.__init_data(value))
        self.__values = tuple(x[1] for x in tuples)
        self.__attr_names = {x[0]: i for i, x in enumerate(tuples)}

    @property
    def source(self) -> str:
        return self.__source

    @staticmethod
    def __get_attr_key(key: str | int) -> str:
        return f"column_{key}" if isinstance(key, int) else key

    def __init_data(self, value: Iterable) -> Iterable[tuple]:
        if isinstance(value, dict):
            return ((self.__get_attr_key(k), v) for k, v in value.items())
        elif isinstance(value, (tuple, list, set)):
            return ((self.__get_attr_key(i), v) for i, v in enumerate(value, start=1))
        raise ValueError(f"can't initialize data record from '{type(value)}' values")

    def __getitem__(self, key: str | int) -> Any:
        if isinstance(key, str):
            return (
                self.__values[self.__attr_names[key]]
                if key in self.__attr_names
                else None
            )
        elif isinstance(key, int):
            return self.__values[key]
        raise ValueError(f"can't get data record using '{type(key)}' keys")

    def __len__(self) -> int:
        return len(self.__values)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.__values)
