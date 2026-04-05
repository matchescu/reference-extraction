from collections.abc import Sequence, Iterator
from os import PathLike
from pathlib import Path
from typing import Iterable

import polars as pl

from matchescu.typing import Trait

from matchescu.data import Record
from matchescu.typing import DataSource


class CsvFile(DataSource):
    def __init__(
        self,
        file_path: str | PathLike,
        traits: Sequence[Trait],
        has_header: bool = True,
    ):
        file_path = Path(file_path)
        self.name = file_path.name.replace(file_path.suffix, "")
        self.traits = traits

        self.__file_path = file_path
        self.__header = has_header
        try:
            self.__df = pl.read_csv(
                self.__file_path, ignore_errors=True, has_header=self.__header
            )
        except pl.NoDataError:
            self.__df = pl.DataFrame()

    @property
    def has_header(self) -> bool:
        return self.__header

    @property
    def path(self) -> Path:
        return self.__file_path

    @property
    def columns(self) -> Iterable[str]:
        return self.__df.columns

    def __getitem__(self, idx: int) -> Record:
        if not isinstance(idx, int):
            raise ValueError("only integer indexing is supported")
        return Record(self.__df.row(idx, named=True))

    def __iter__(self) -> Iterator[Record]:
        if self.__df is None:
            return iter([])
        return iter(map(Record, self.__df.iter_rows(named=True)))

    def __len__(self) -> int:
        return self.__df.shape[0] if self.__df is not None else 0
