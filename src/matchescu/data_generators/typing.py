from abc import abstractmethod
from dataclasses import dataclass, Field
from typing import Protocol, Iterable, Collection, Generator, Set, Callable

from matchescu.typing import Record


class DataSource(Iterable[Record], Protocol):
    """A data source iterates over information records."""


class GroundTruth:
    """Ground truth is expressed in terms of one or more mathematical models."""

    def __init__(self):
        self.__fsm = set()
        self.__serf = set()
        self.__algebraic = set()

    @property
    def fsm(self) -> Set[tuple[tuple]]:
        """Ground truth expressed in terms of the Fellegi-Sunter probabilistic model.

        The Fellegi-Sunter model is the oldest mathematical model for entity resolution. Its origins
        can be traced back to the paper written by Ivan Fellegi and Alan Sunter:
        `A Theory for Record Linkage<https://www.tandfonline.com/doi/abs/10.1080/01621459.1969.10501049>`_.
        """
        return self.__fsm

    @fsm.setter
    def fsm(self, value: Set[tuple[tuple]]) -> None:
        self.__fsm = value

    @property
    def serf(self) -> Set[tuple]:
        """Ground truth expressed in terms of the SERF functional model.

        The SERF (Standard Entity Resolution Framework) mathematical model proposes a way of looking
        at entity resolution as if it were the result of applying two types of functions (match
        functions and merge functions) over two data sources with unique records (a data set). The model
        builds new information records from pairs of existing information records by using a "domination"
        relationship. The "dominating" information records take the place of the "dominated" information
        records until there aren't any more records in the two data sets that can create new "dominating"
        records. The information records obtained by this process make up a data set that is said to be
        the entity resolution over the two initial data sources. The SERF ground truth depends on which
        ``merge`` function is used.

        It was proposed by Omar Benjelloun et al. in the paper
        `Swoosh: a generic approach to entity resolution<https://link.springer.com/article/10.1007/s00778-008-0098-x>`_.
        """
        return self.__serf

    @serf.setter
    def serf(self, value: Set[tuple]) -> None:
        self.__serf = value

    @property
    def algebraic(self) -> Set[tuple[tuple]]:
        """Ground truth expressed in terms of the Algebraic model.

        The algebraic model for entity resolution views entity resolution as an equivalence algebraic
        relation between elements of the same data source with the properties of reflexivity, symmetry
        and distributivity. Such a relation partitions the original data source in a unique way.
        Therefore, in this model, the entity resolution over a data source is the partitioning of
        equivalent elements over the same data source. This model was proposed by John R. Talburt in
        the book
        `Entity Resolution and Information Quality<https://books.google.ro/books?id=tIB0IZYR8V8C&dq=john+r.+talburt>`_.
        """
        return self.__algebraic

    @algebraic.setter
    def algebraic(self, value: Set[tuple[tuple]]) -> None:
        self.__algebraic = value


class GroundTruthBuilder(Protocol):
    """Build ground truth for a generator."""

    def fsm(self) -> "GroundTruthBuilder":
        """Builds the ground truth specific to the Fellegi-Sunter model."""

    def serf(self, merge_function: Callable[[Record, Record], Record]) -> "GroundTruthBuilder":
        """Builds the ground truth specific to the SERF model.

        :param merge_function: the merge function used in SERF-compatible ER process
        """

    def algebraic(self) -> "GroundTruthBuilder":
        """Builds the ground truth specific to the Algebraic model."""

    @property
    @abstractmethod
    def ground_truth(self) -> GroundTruth:
        """The finished product: the ground truth."""


class DataGenerator(Protocol):
    """A data generator transforms one data source into multiple data sources.

    A data source is an iterable sequence of records.
    A generator returns a collection of data sources.
    """

    def __call__(self, input_data: DataSource) -> Collection[DataSource]:
        """Generate a collection of data sources.

        :return: a collection of iterable sequences of ``Record`` items.
        """

    def update_ground_truth(self, builder: GroundTruthBuilder) -> None:
        """Update ground truth using a builder."""
