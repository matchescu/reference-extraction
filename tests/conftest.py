from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def tests_dir():
    return Path(__file__).parent


@pytest.fixture(scope="session")
def data_dir(tests_dir):
    return tests_dir / "data"


@pytest.fixture(scope="session")
def csv_path(data_dir, request):
    if hasattr(request, "param") and isinstance(request.param, (str, Path)):
        return data_dir / request.param
    return data_dir / "test.csv"
