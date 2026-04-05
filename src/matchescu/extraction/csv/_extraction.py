from pathlib import Path
from typing import Iterable, Callable

from matchescu.extraction import RecordExtraction, single_record, Traits
from matchescu.typing import Record, EntityReferenceIdentifier as RefId

from ._file import CsvFile


class CsvRecordExtraction(RecordExtraction):
    def __init__(
        self,
        fpath: str | Path,
        traits: Traits,
        id_attr: str | int = 0,
        source_attr: str | int | None = None,
        has_header: bool = True,
        source_finder: (
            Callable[[Record, str | int | None, str | None], str] | None
        ) = None,
    ):
        self.__fpath = Path(fpath).absolute()
        self.__source_attr = source_attr
        self.__id_attr = id_attr
        self.__source_finder = source_finder or self._get_source
        self.__ds = CsvFile(self.__fpath, list(traits), has_header=has_header)
        super().__init__(self.__ds, self._id_factory, single_record)

    def _get_source(
        self, r: Record, source_attr: str | int | None, source_fallback: str | None
    ) -> str:
        try:
            return r[source_attr]
        except ValueError:
            return source_fallback if source_fallback is not None else self.__ds.name

    def _id_factory(self, records: Iterable[Record]) -> RefId:
        record = next(iter(records))
        try:
            label = record[self.__id_attr]
        except ValueError:
            label = record[0]
        source = self.__source_finder(record, self.__source_attr, self.__ds.name)
        return RefId(label=label, source=source)

    @property
    def data_source(self) -> CsvFile:
        return self.__ds
