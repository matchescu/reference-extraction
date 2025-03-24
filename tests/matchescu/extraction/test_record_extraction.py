import pytest

from matchescu.extraction import RecordExtraction, single_record


@pytest.fixture
def sut(csv_data_source, record_adapter) -> RecordExtraction:
    return RecordExtraction(csv_data_source, record_adapter, single_record)


def test_number_of_references(sut, csv_data_source):
    refs = list(sut())

    assert len(refs) == len(csv_data_source)


def test_extracted_attributes(sut, csv_data_source):
    assert all(
        hasattr(r, "id")
        and hasattr(r, "name")
        and hasattr(r, "description")
        and hasattr(r, "manufacturer")
        and hasattr(r, "price")
        for r in sut()
    )


def test_extracted_references_have_expected_source(sut, csv_data_source):
    assert all(r.id.source == csv_data_source.name for r in sut())
