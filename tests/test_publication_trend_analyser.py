"""
tests/test_publication_trend_analyser.py
-----------------------------------------
Unit tests for PublicationTrendAnalyser: covers TP01 through TP05.
"""

import pytest
from repository.data_repository import DataRepository
from analysers.publication_trend_analyser import PublicationTrendAnalyser
from models.book import Book


def make_book(year):
    return Book("Title", "Author", year, "English", "Publisher", "1234567890", "BNB001")


@pytest.fixture
def repo():
    return DataRepository()


# TP01
def test_analyse_knownDataset_returnsCorrectYearCounts(repo):
    repo.set_books([
        make_book(2021), make_book(2021),
        make_book(2022),
        make_book(2023), make_book(2023), make_book(2023),
    ])
    result = PublicationTrendAnalyser(repo).analyse()
    assert result == {2021: 2, 2022: 1, 2023: 3}


# TP02
def test_analyse_emptyRepository_returnsEmptyDict(repo):
    repo.set_books([])
    result = PublicationTrendAnalyser(repo).analyse()
    assert result == {}


# TP03
def test_analyse_booksWithYearZero_excludesYearZero(repo):
    repo.set_books([make_book(0), make_book(0), make_book(2022)])
    result = PublicationTrendAnalyser(repo).analyse()
    assert 0 not in result
    assert result == {2022: 1}


# TP04
def test_analyse_singleBook_returnsSingleEntry(repo):
    repo.set_books([make_book(2020)])
    result = PublicationTrendAnalyser(repo).analyse()
    assert result == {2020: 1}


# TP05
def test_analyse_multipleYears_resultIsSortedAscending(repo):
    repo.set_books([make_book(2023), make_book(2019), make_book(2021)])
    result = PublicationTrendAnalyser(repo).analyse()
    assert list(result.keys()) == sorted(result.keys())