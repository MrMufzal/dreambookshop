"""
tests/test_csv_data_loader.py
------------------------------
Unit tests for CSVDataLoader: covers TL01 through TL07.
"""

import pytest
from loaders.csv_data_loader import CSVDataLoader
from repository.data_repository import DataRepository
from models.book import Book

VALID_CSV_CONTENT = """book,author,publication date,language,book publisher,ISBN,BNB id
World Politics,Jeffrey Haynes,2023,English,SAGE,1529613827,GBC315766
World Music,Terry Miller,2022,English,Routledge,,GBC397766
Reflections,John Smith,2021,French,,1448308019,GBC2M0828
"""

MISSING_COLUMN_CSV = """title,author,publication date,language
World Politics,Jeffrey Haynes,2023,English
"""


@pytest.fixture
def repository():
    return DataRepository()


@pytest.fixture
def valid_csv(tmp_path):
    f = tmp_path / "test_dataset.csv"
    f.write_text(VALID_CSV_CONTENT)
    return str(f)


@pytest.fixture
def missing_column_csv(tmp_path):
    f = tmp_path / "bad_dataset.csv"
    f.write_text(MISSING_COLUMN_CSV)
    return str(f)


# TL01
def test_load_validFilePath_returnsListOfBooks(repository, valid_csv):
    loader = CSVDataLoader(repository)
    result = loader.load(valid_csv)
    assert isinstance(result, list)
    assert len(result) == 3
    assert all(isinstance(b, Book) for b in result)


# TL02
def test_load_validFilePath_booksHaveCorrectAttributes(repository, valid_csv):
    loader = CSVDataLoader(repository)
    books = loader.load(valid_csv)
    first = books[0]
    assert first.title == "World Politics"
    assert first.author == "Jeffrey Haynes"
    assert first.publication_year == 2023
    assert first.language == "English"
    assert first.publisher == "SAGE"
    assert first.isbn == "1529613827"
    assert first.bnb_id == "GBC315766"


# TL03
def test_load_missingFilePath_raisesFileNotFoundError(repository):
    loader = CSVDataLoader(repository)
    with pytest.raises(FileNotFoundError):
        loader.load("nonexistent/path/dataset.csv")


# TL04
def test_load_csvWithMissingISBN_bookHasEmptyIsbn(repository, valid_csv):
    loader = CSVDataLoader(repository)
    books = loader.load(valid_csv)
    assert books[1].isbn == ""
    assert not books[1].has_isbn()


# TL05
def test_load_csvWithMissingPublisher_bookHasEmptyPublisher(repository, valid_csv):
    loader = CSVDataLoader(repository)
    books = loader.load(valid_csv)
    assert books[2].publisher == ""


# TL06
def test_load_validFile_populatesDataRepository(repository, valid_csv):
    loader = CSVDataLoader(repository)
    loader.load(valid_csv)
    assert repository.count() == 3
    assert not repository.is_empty()


# TL07
def test_load_csvMissingRequiredColumn_raisesValueError(repository, missing_column_csv):
    loader = CSVDataLoader(repository)
    with pytest.raises(ValueError):
        loader.load(missing_column_csv)