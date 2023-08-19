from typing import Collection, Set, Callable, Optional

import pandas
from matchescu.data_generators.ground_truth import PandasGroundTruthBuilder

from matchescu.data_generators.typing import DataSource, GroundTruth
from matchescu.typing import Record


class SplitTableRandomly:
    def __init__(
        self,
        output_table_count: int,
        common_columns: list[str],
        merge_function: Optional[Callable[[Record, Record], Record]] = None
    ) -> None:
        self.__count = output_table_count
        self.__fixed = set(common_columns)
        self.__data = pandas.DataFrame()
        self.__truth = GroundTruth()
        self.__merge = merge_function

    def __non_fixed_generator(self):
        non_fixed_cols = self.__data.loc[:, ~self.__data.columns.isin(self.__fixed)]
        col_count = non_fixed_cols.shape[1] // self.__count
        for i in range(self.__count):
            result = non_fixed_cols.sample(n=col_count, axis=1)
            yield result
            non_fixed_cols.drop(result.columns, axis=1, inplace=True)

    def __call__(self, input_data: DataSource) -> Collection[DataSource]:
        self.__data = pandas.DataFrame(input_data)
        n = self.__data.shape[1]
        if self.__count < 2 or self.__count > n-len(self.__fixed):
            raise ValueError("output count out of range")

        fixed_cols = self.__data.loc[:, self.__data.columns.isin(self.__fixed)]
        result = [
            pandas.concat([fixed_cols, df], axis=1)
            for df in self.__non_fixed_generator()
        ]
        ground_truth_builder = PandasGroundTruthBuilder(result).algebraic().fsm()
        if self.__merge is not None:
            ground_truth_builder = ground_truth_builder.serf(self.__merge)
        self.__truth = ground_truth_builder.ground_truth
        return result

    @property
    def ground_truth(self) -> GroundTruth:
        return self.__truth
