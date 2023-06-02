from dataclasses import dataclass


@dataclass
class Clustering:
    col_clusters: list[tuple[str]]
    rows: list[list[tuple]]