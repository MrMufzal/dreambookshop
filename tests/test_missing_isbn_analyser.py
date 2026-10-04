"""
tests/test_missing_isbn_analyser.py
-------------------------------------
Unit tests for MissingISBNAnalyser: covers TM01 through TM06.
"""

import pytest
from repository.data_repository import DataRepository
from analysers.missing_isbn_analyser import MissingISBNAnalyser
from models.book import Book


def make_book(isbn):
    return Book("Title", "Author", 2023, "English", "Publisher", isbn, "BNB001")


@pytest.fixture
def repo():
    return DataRepository()


# TM01
def test_analyse_knownDataset_returnsCorrectMissingCount(repo):
    repo.set_books([make_book("1234567890"), make_book(""), make_book("")])
    result = MissingISBNAnalyser(repo).analyse()
    assert result["Missing ISBN"] == 2


# TM02
def test_analyse_knownDataset_returnsCorrectPresentCount(repo):
    repo.set_books([make_book("1234567890"), make_book(""), make_book("")])
    result = MissingISBNAnalyser(repo).analyse()
    assert result["With ISBN"] == 1


# TM03
def test_analyse_knownDataset_percentageIsCorrect(repo):
    repo.set_books([make_book("")] * 1 + [make_book("1234567890")] * 9)
    result = MissingISBNAnalyser(repo).analyse()
    assert result["Missing (%)"] == 10.0


# TM04
def test_analyse_emptyRepository_returnsZeroCounts(repo):
    repo.set_books([])
    result = MissingISBNAnalyser(repo).analyse()
    assert result["With ISBN"] == 0
    assert result["Missing ISBN"] == 0
    assert result["Missing (%)"] == 0.0


# TM05
def test_analyse_allMissingISBN_returns100Percent(repo):
    repo.set_books([make_book("")] * 5)
    result = MissingISBNAnalyser(repo).analyse()
    assert result["Missing (%)"] == 100.0
    assert result["With ISBN"] == 0


# TM06
def test_analyse_noMissingISBN_returns0Percent(repo):
    repo.set_books([make_book("1234567890")] * 5)
    result = MissingISBNAnalyser(repo).analyse()
    assert result["Missing (%)"] == 0.0
    assert result["Missing ISBN"] == 0