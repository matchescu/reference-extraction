import pytest

from matchescu.data_generators.tables import SplitTableRandomly


@pytest.fixture
def random_sub_tables(request):
    count = request.param if hasattr(request, "param") and isinstance(request.param, int) else 2
    return SplitTableRandomly(count, ["a"])


def test_split_table_keeps_common_column(random_sub_tables, sample_table):
    result = random_sub_tables(sample_table)

    assert len(result) == 2
    other_columns = {"a"}
    for table in result:
        assert len(table) == 1, "expected output with a single row"
        assert "a" in table.columns, "expected fixed attr to be in every output data source"

        columns_besides_a = set(col for col in table.columns if col != "a")
        assert len(columns_besides_a) == len(table.columns) - 1, "did not expect duplicate column names"
        assert all(col not in other_columns for col in columns_besides_a), "did not expect column names from other tables"
        other_columns |= columns_besides_a


@pytest.mark.parametrize("random_sub_tables", [1, 3], indirect=True)
def test_split_table_output_count_out_of_range(sample_table, random_sub_tables):
    with pytest.raises(ValueError) as err_proxy:
        random_sub_tables(sample_table)

    assert str(err_proxy.value) == "output count out of range"
