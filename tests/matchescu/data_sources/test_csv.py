import pytest

from matchescu.data_sources._csv import CsvDataSource


@pytest.fixture
def sut(csv_path):
    return CsvDataSource(csv_path, [])


def test_empty_source(sut):
    assert sut.name == "test"
    assert sut.traits == []
    assert len(sut) == 0
    assert len(list(sut)) == 0


def test_load_csv_data(sut):
    sut.read()

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
