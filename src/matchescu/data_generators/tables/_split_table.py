from typing import Collection

import pandas

from matchescu.data_generators.typing import DataSource


class SplitTableRandomly:
    def __init__(self, output_table_count: int, common_columns: list[str]):
        self.__count = output_table_count
        self.__fixed = set(common_columns)
        self.__data = pandas.DataFrame()

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

        return [
            pandas.concat([fixed_cols, df], axis=1)
            for df in self.__non_fixed_generator()
        ]
