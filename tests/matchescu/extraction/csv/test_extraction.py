import os

import pytest
from pathlib import Path

from matchescu.extraction import Traits
from matchescu.extraction.csv._extraction import CsvRecordExtraction


@pytest.fixture
def csv_headers(request):
    default_headers = ["id", "name", "source"]
    return getattr(request, "param", default_headers)


@pytest.fixture
def csv_contents(request):
    default_contents = [["1", "John", "src1"]]
    return getattr(request, "param", default_contents)


@pytest.fixture
def csv_name(request):
    return getattr(request, "param", "test.csv")


@pytest.fixture
def csv_path(tmp_path: Path, csv_headers, csv_contents, csv_name) -> Path:
    fpath = tmp_path / csv_name
    file_contents = csv_contents
    if csv_headers is not None:
        csv_contents.insert(0, csv_headers)
    with open(fpath, "w") as f:
        lines = [",".join(line) + os.linesep for line in file_contents]
        f.writelines(lines)
    return fpath


@pytest.fixture
def traits(request):
    default = Traits().string(["name", "source"])
    return getattr(request, "param", default)


@pytest.fixture
def id_attr(request):
    return getattr(request, "param", "id")


@pytest.fixture
def source_attr(request):
    return getattr(request, "param", "source")


def test_extraction_with_id_source_and_headers(csv_path, traits, id_attr, source_attr):
    extract = CsvRecordExtraction(csv_path, traits, id_attr, source_attr, True, None)
    refs = list(extract())

    assert refs[0].id.label == 1
    assert refs[0].id.source == "src1"
    assert len(refs) == 1


def test_extraction_with_default_source(csv_path, traits, id_attr):
    extractor = CsvRecordExtraction(csv_path, traits, id_attr)
    refs = list(extractor())

    assert refs[0].id.label == 1
    assert refs[0].id.source == "test"


def test_extraction_with_default_attrs(csv_path, traits):
    extractor = CsvRecordExtraction(csv_path, traits)
    refs = list(extractor())

    assert refs[0].id.label == 1
    assert refs[0].id.source == "test"


@pytest.mark.parametrize("csv_headers", [None], indirect=True)
def test_extraction_without_header(csv_path, traits, csv_headers):
    extractor = CsvRecordExtraction(csv_path, traits, has_header=False)
    refs = list(extractor())

    assert refs[0].id.label == 1
    assert refs[0].id.source == "test"


@pytest.mark.skip(reason="must implement __contains__ in matchescu.data.Record")
@pytest.mark.parametrize("id_attr", ["something-non-existent"], indirect=True)
def test_id_attr_missing_uses_first_element(csv_path, traits, id_attr):
    extract = CsvRecordExtraction(csv_path, traits, id_attr=id_attr)
    refs = list(extract())

    assert refs[0].id.label == 1


@pytest.mark.parametrize("csv_headers", [None], indirect=True)
def test_no_headers_with_index_attrs(csv_path, traits, csv_headers):
    extract = CsvRecordExtraction(
        csv_path, traits, id_attr=0, source_attr=1, has_header=False
    )

    ref_id = list(extract())[0].id

    assert ref_id.label == 1
    assert ref_id.source == "John"
