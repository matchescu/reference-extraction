from typing import Collection, Set, Callable, Optional

import pandas
from matchescu.data_generators.ground_truth import PandasGroundTruthBuilder

from matchescu.data_generators.typing import DataSource
from matchescu.adt.entity_resolution_result import EntityResolutionResult
from matchescu.adt.types import Record


class SplitTable:
    def __init__(
        self,
        column_lists:list[list],
        merge_function: Optional[Callable[[Record, Record], Record]] = None
    ) -> None:
        self.__column_lists = column_lists
        self.__data = pandas.DataFrame()
        self.__truth = EntityResolutionResult()
        self.__merge = merge_function

    def __call__(self, input_data: DataSource) -> Collection[DataSource]:
        self.__data = pandas.DataFrame(input_data)

        result = [
            self.__data[col_list]
            for col_list in self.__column_lists
        ]

        ground_truth_builder = PandasGroundTruthBuilder(result).algebraic().fsm()
        if self.__merge is not None:
            ground_truth_builder = ground_truth_builder.serf(self.__merge)
        self.__truth = ground_truth_builder.ground_truth
        return result

    @property
    def ground_truth(self) -> EntityResolutionResult:
        return self.__truth
