import pytest

from matchescu.extraction import Traits
from matchescu.typing import EntityReferenceIdentifier, EntityReference

from matchescu.extraction.csv._file import CsvFile


@pytest.fixture
def csv_traits():
    return list(
        Traits().string(["name", "description", "manufacturer"]).currency(["price"])
    )


@pytest.fixture
def csv_data_source(csv_path, csv_traits):
    return CsvFile(csv_path, csv_traits)


@pytest.fixture
def entity_reference(csv_data_source, request) -> EntityReference:
    ref_id = request.param if hasattr(request, "param") else 1
    return EntityReference(
        EntityReferenceIdentifier(ref_id, csv_data_source.name), {"id": ref_id}
    )


@pytest.fixture
def id_factory(csv_data_source):
    return lambda rows: EntityReferenceIdentifier(rows[0]["id"], csv_data_source.name)
