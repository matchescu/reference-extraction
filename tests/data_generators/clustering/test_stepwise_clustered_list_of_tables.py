from abstractions.data_structures import Table
from data_generators.clustering import stepwise_clustered_list_of_tables


def test_basic_input():
    t1 = Table("a", "b")
    t1.load_sequence([[1, 2], [3, 4]])
    t2 = Table("c", "d")
    t2.load_sequence([[5, 6], [7, 8]])

    result = stepwise_clustered_list_of_tables([t1, t2])

    assert result.col_clusters == [("a", "b"), ("c", "d")]
    assert result.rows == [
        [(1, 2), (5, 6)],
        [(3, 4), (7, 8)],
    ]
