from os import PathLike
from pathlib import Path
import pytest
from abstractions.data_structures import Table


TEST_DIR = Path(__file__).parent


@pytest.fixture
def sample_csv_file_path() -> str | PathLike:
    return TEST_DIR / "sample.csv"


@pytest.fixture
def sample_table(sample_csv_file_path):
    return Table.load_csv(sample_csv_file_path)
