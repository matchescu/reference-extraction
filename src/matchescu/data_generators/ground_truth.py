from typing import Callable

import pandas
from matchescu.data_generators.typing import GroundTruthBuilder
from matchescu.adt.entity_resolution_result import EntityResolutionResult
from matchescu.adt.types import Record


class PandasGroundTruthBuilder(GroundTruthBuilder):
    def __init__(self, data_sources: list[pandas.DataFrame]):
        self.__data_sources = data_sources
        self.__record_count = min(len(ds) for ds in self.__data_sources)
        self.__truth = EntityResolutionResult()

    def fsm(self) -> GroundTruthBuilder:
        fsm = []
        for i in range(self.__record_count):
            matching_rows = []
            for data_source in self.__data_sources:
                row = data_source.iloc[i, :]
                row = tuple(item for item in row)
                matching_rows.append(row)
            ground_truth_item = tuple(row for row in matching_rows)
            fsm.append(ground_truth_item)
        self.__truth.fsm = fsm
        return self

    def serf(self, merge_function: Callable[[Record, Record], Record]) -> GroundTruthBuilder:
        serf = []
        if len(self.__data_sources) != 2:
            raise ValueError("the SERF model supports only 2 data sources")
        for i in range(self.__record_count):
            row0 = [value for value in self.__data_sources[0].iloc[i, :]]
            row1 = [value for value in self.__data_sources[1].iloc[i, :]]
            serf.append(tuple(value for value in merge_function(row0, row1)))
        self.__truth.serf = serf
        return self

    def algebraic(self) -> "GroundTruthBuilder":
        partition = {}
        for i in range(self.__record_count):
            partition_subset = {
                tuple(value for value in source.iloc[i, :]): None
                for source in self.__data_sources
            }
            partition[tuple(v for v in partition_subset)] = None
        self.__truth.algebraic = [
            [item for item in partition_row]
            for partition_row in partition
        ]
        return self

    @property
    def ground_truth(self) -> EntityResolutionResult:
        return self.__truth

