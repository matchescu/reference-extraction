from random import randint, choice
from typing import Generator

from abstractions.data_structures import Table


def _select_unique_columns(available_names: list[str], taken_names: set[str], count: int) -> Generator[str, None, None]:
    current = count
    if current > len(available_names):
        raise ValueError("there aren't enough available names")
    while current > 0:
        candidate = choice(available_names)
        while candidate in taken_names:
            candidate = choice(available_names)

        yield candidate

        taken_names.add(candidate)
        current -= 1


def random_sub_tables(
    input_table: Table,
    sub_table_count: int,
    min_out_table_cols: int,
    max_out_table_cols: int,
    *fixed_columns: str
) -> list[Table]:
    fixed_col_count = len(fixed_columns)
    if min_out_table_cols < fixed_col_count:
        raise ValueError(f"min columns too small ({min_out_table_cols}<{fixed_col_count})")
    if max_out_table_cols > len(input_table.columns):
        raise ValueError(f"max columns too large ({max_out_table_cols}>{len(input_table.columns)})")
    fixed_col_set = set(fixed_columns)
    table_col_set = set(map(lambda c: c.name, input_table.columns))
    result: list[Table] = []
    current = sub_table_count
    avail_columns = table_col_set - fixed_col_set
    while current > 0 and len(avail_columns) > 0:
        out_table_col_count = randint(1, len(avail_columns)) if len(avail_columns) > 1 else 1
        out_table_cols = list(fixed_columns)
        out_table_cols.extend(
            _select_unique_columns(
                list(avail_columns), fixed_col_set, out_table_col_count
            )
        )
        result.append(input_table.sub_table(*out_table_cols))
        avail_columns = table_col_set - fixed_col_set
        current -= 1
    if current > 0:
        raise ValueError("random generators tend to burp.")
    return result
