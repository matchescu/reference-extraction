import pytest

from matchescu.extraction.csv._file import CsvFile


@pytest.fixture
def empty_csv(tmp_path):
    file_path = tmp_path / "empty.csv"
    with open(file_path, "w") as f:
        f.writelines([""])
    return file_path


@pytest.fixture
def only_headers(tmp_path):
    file_path = tmp_path / "only_headers.csv"
    with open(file_path, "w") as f:
        f.writelines(["column1,column2"])
    return file_path


@pytest.fixture
def sut(csv_path):
    return CsvFile(csv_path, [])


def test_empty_source(empty_csv):
    sut = CsvFile(empty_csv, [], has_header=False)
    assert sut.name == "empty"
    assert sut.traits == []
    assert len(sut) == 0
    assert len(list(sut)) == 0


def test_only_headers(only_headers):
    sut = CsvFile(only_headers, [], has_header=True)
    assert sut.name == "only_headers"
    assert sut.traits == []
    assert list(sut.columns) == ["column1", "column2"]
    assert len(sut) == 0
    assert len(list(sut)) == 0


def test_load_csv_data(sut):
    assert len(sut) == 10
    records = list(sut)
    assert records[0]["id"] == 10221960
    assert records[0][0] == 10221960
    assert records[0]["name"] == "Netgear ProSafe FS105 Ethernet Switch - FS105NA"
    assert records[0][1] == "Netgear ProSafe FS105 Ethernet Switch - FS105NA"
    assert (
        records[0]["description"]
        == "NETGEAR FS105 Prosafe 5 Port 10/100 Desktop Switch"
    )
    assert records[0][2] == "NETGEAR FS105 Prosafe 5 Port 10/100 Desktop Switch"
    assert records[0]["manufacturer"] == "Netgear"
    assert records[0][3] == "Netgear"
    assert records[0]["price"] is None
    assert records[0][4] is None


def test_get_item(sut):
    assert sut[0]["id"] == 10221960
    assert sut[0][0] == 10221960
