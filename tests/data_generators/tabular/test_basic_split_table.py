import pytest

from matchescu.data_generators.tables import SplitTableRandomly


@pytest.fixture
def random_split(request):
    count = request.param if hasattr(request, "param") and isinstance(request.param, int) else 2
    return SplitTableRandomly(count, ["a"])


def test_random_split_output(random_split, sample_table):
    result = random_split(sample_table)

    assert len(result) == 2
    other_columns = {"a"}
    for table in result:
        assert len(table) == 1, "expected output with a single row"
        assert "a" in table.columns, "expected fixed attr to be in every output data source"

        columns_besides_a = set(col for col in table.columns if col != "a")
        assert len(columns_besides_a) == len(table.columns) - 1, "did not expect duplicate column names"
        assert all(
            col not in other_columns for col in columns_besides_a), "did not expect column names from other tables"
        other_columns |= columns_besides_a


@pytest.mark.parametrize("random_split", [1, 3], indirect=True)
def test_random_split_count_range(sample_table, random_split):
    with pytest.raises(ValueError) as err_proxy:
        random_split(sample_table)

    assert str(err_proxy.value) == "output count out of range"


def test_random_split_fsm_ground_truth(sample_table, random_split):
    tables = random_split(sample_table)

    assert random_split.ground_truth.fsm is not None
    assert len(random_split.ground_truth.fsm) == 1
    assert random_split.ground_truth.fsm == [
        (
            (tables[0].iloc[0, 0], tables[0].iloc[0, 1]),
            (tables[1].iloc[0, 0], tables[1].iloc[0, 1])
        )
    ]


def test_random_split_serf_ground_truth(sample_table):
    splitter = SplitTableRandomly(
        2,
        ["a"],
        merge_function=lambda x, y: tuple(
            x[i] + y[i]
            for i in range(min(map(len, [x, y])))
        )
    )
    splitter(sample_table)

    assert splitter.ground_truth.serf is not None
    assert splitter.ground_truth.serf == [(2, 5)]


def test_random_split_algebraic_ground_truth(sample_table, random_split):
    tables = random_split(sample_table)

    assert random_split.ground_truth.algebraic is not None
    assert len(random_split.ground_truth.algebraic) == 1
    assert random_split.ground_truth.algebraic == [[
        (tables[0].iloc[0, 0], tables[0].iloc[0, 1]),
        (tables[1].iloc[0, 0], tables[1].iloc[0, 1])
    ]]
