from unittest.mock import MagicMock

import pytest

from matchescu.data_sources import Record, CsvDataSource
from matchescu.extraction import Traits
from matchescu.typing import EntityReferenceIdentifier, RecordAdapter


class EntityReferenceStub(Record):
    id: EntityReferenceIdentifier


@pytest.fixture
def traits():
    return list(
        Traits()
        .int(["id"])
        .string(["name", "description", "manufacturer"])
        .currency(["price"])
    )


@pytest.fixture
def data_source(csv_path, traits):
    return CsvDataSource(csv_path, traits).read()


@pytest.fixture
def record_adapter(data_source):
    mock = MagicMock(name="RecordAdapterMock", spec=RecordAdapter)
    def mock_body(record: Record) -> EntityReferenceStub:
        result = EntityReferenceStub(record)
        result.id = EntityReferenceIdentifier(
            label=record["id"],
            source=data_source.name
        )
        return result
    mock.side_effect = mock_body
    return mock
