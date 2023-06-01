import pytest
from abstractions.data_structures import Table

from data_generators.tabular import split_table


def test_split_table_keeps_common_column(sample_table):
    result = split_table(sample_table, 2, 2, 3, "a")

    assert len(result) == 2
    for table in result:
        assert "a" in set(map(lambda c: c.name, table.columns))


def test_split_table_max_columns_too_large(sample_table):
    with pytest.raises(ValueError) as err_proxy:
        split_table(sample_table, 1, 4, 4, "a", "b")

    assert str(err_proxy.value) == "max columns too large (4>3)"


def test_split_table_min_columns_too_small(sample_table):
    with pytest.raises(ValueError) as err_proxy:
        split_table(sample_table, 1, 1, 3, "a", "b")

    assert str(err_proxy.value) == "min columns too small (1<2)"
