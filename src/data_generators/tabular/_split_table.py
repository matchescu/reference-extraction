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


def _compute_out_col_count(fixed_count: int, min_count: int, max_count: int) -> int:
    lo = fixed_count
    if lo < min_count:
        lo = min_count
    hi = max_count
    if hi < fixed_count:
        hi = fixed_count
    return randint(lo, hi)


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
    avail_columns = table_col_set - fixed_col_set
    result: list[Table] = []
    current = sub_table_count
    while current > 0:
        out_table_col_count = _compute_out_col_count(
            fixed_col_count, min_out_table_cols, max_out_table_cols
        ) - fixed_col_count
        out_table_cols = list(fixed_columns)
        out_table_cols.extend(
            _select_unique_columns(
                list(avail_columns), fixed_col_set.copy(), out_table_col_count
            )
        )
        result.append(input_table.sub_table(*out_table_cols))
        current -= 1
    return result
