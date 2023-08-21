from abc import abstractmethod
from typing import Protocol, Iterable, Collection, Callable

from matchescu.entity_resolution_result import EntityResolutionResult
from matchescu.types import Record


class DataSource(Iterable[Record], Protocol):
    """A data source iterates over information records."""


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
    def ground_truth(self) -> EntityResolutionResult:
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
