"""
tests/test_data_repository.py
------------------------------
Unit tests for DataRepository: covers TR01 through TR05.
"""

import pytest
from repository.data_repository import DataRepository
from models.book import Book


def make_book(title="Test Book", author="Test Author", year=2023,
              language="English", publisher="Test Pub", isbn="1234567890", bnb_id="BNB001"):
    return Book(title, author, year, language, publisher, isbn, bnb_id)


@pytest.fixture
def repo():
    return DataRepository()


@pytest.fixture
def sample_books():
    return [make_book(title=f"Book {i}", bnb_id=f"BNB00{i}") for i in range(3)]


# TR01
def test_isEmpty_onInit_returnsTrue(repo):
    assert repo.is_empty() is True


# TR02
def test_setBooks_withValidList_countMatchesListLength(repo, sample_books):
    repo.set_books(sample_books)
    assert repo.count() == 3


# TR03
def test_getBooks_afterSetBooks_returnsExactSameBooks(repo, sample_books):
    repo.set_books(sample_books)
    result = repo.get_books()
    assert result == sample_books


# TR04
def test_isEmpty_afterSetBooks_returnsFalse(repo, sample_books):
    repo.set_books(sample_books)
    assert repo.is_empty() is False


# TR05
def test_setBooks_withEmptyList_countReturnsZero(repo):
    repo.set_books([])
    assert repo.count() == 0
    assert repo.is_empty() is True