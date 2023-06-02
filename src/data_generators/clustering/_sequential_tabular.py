from typing import Iterable

from abstractions.data_structures import Table
from ._adt import Clustering


def stepwise_clustered_list_of_tables(tables: Iterable[Table]) -> Clustering:
    min_table_size = min(map(len, tables))
    return Clustering(
        col_clusters=[
            tuple(map(lambda c: str(c.name), table.columns)) for table in tables
        ],
        rows=[
            [tuple(table[i].values) for table in tables]
            for i in range(min_table_size)
        ]
    )
