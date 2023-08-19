from typing import Protocol, Iterable, Collection, Generator

from matchescu.typing import Record


class DataSource(Iterable[Record], Protocol):
    """A data source iterates over information records."""


class DataGenerator(Protocol):
    """A data generator transforms one data source into multiple data sources.

    A data source is an iterable sequence of records.
    A generator returns a collection of data sources.
    """
    def __call__(self, input_data: DataSource) -> Collection[DataSource]:
        """Generate a collection of data sources.

        :return: a collection of iterable sequences of ``Record`` items.
        """
