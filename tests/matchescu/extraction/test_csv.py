import pytest

from matchescu.extraction import CsvEntityReferenceExtraction


@pytest.fixture
def sut(data_source, record_adapter):
    return CsvEntityReferenceExtraction(data_source, record_adapter)


def test_extraction_returns_expected_number_of_references(sut):
    refs = list(sut())

    assert len(refs) == 10


def test_extracted_refs_have_expected_attributes(sut):
    refs = list(sut())

    assert all(
        hasattr(ref, "id")
        and hasattr(ref, "name")
        and hasattr(ref, "description")
        and hasattr(ref, "manufacturer")
        and hasattr(ref, "price")
        for ref in refs
    )
