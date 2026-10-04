"""
tests/test_publisher_analyser.py
----------------------------------
Unit tests for PublisherAnalyser: covers TPB01 through TPB04.
"""

import pytest
from repository.data_repository import DataRepository
from analysers.publisher_analyser import PublisherAnalyser
from models.book import Book


def make_book(publisher):
    return Book("Title", "Author", 2023, "English", publisher, "1234567890", "BNB001")


@pytest.fixture
def repo():
    return DataRepository()


# TPB01
def test_analyse_knownDataset_returnsCorrectPublisherCounts(repo):
    repo.set_books([
        make_book("Routledge"), make_book("Routledge"),
        make_book("SAGE"),
        make_book("Springer"), make_book("Springer"), make_book("Springer"),
    ])
    result = PublisherAnalyser(repo).analyse()
    assert result["Routledge"] == 2
    assert result["SAGE"] == 1
    assert result["Springer"] == 3


# TPB02
def test_analyse_emptyRepository_returnsEmptyDict(repo):
    repo.set_books([])
    result = PublisherAnalyser(repo).analyse()
    assert result == {}


# TPB03
def test_analyse_booksWithEmptyPublisher_excludesMissingPublishers(repo):
    repo.set_books([make_book("SAGE"), make_book(""), make_book("")])
    result = PublisherAnalyser(repo).analyse()
    assert "" not in result
    assert result == {"SAGE": 1}


# TPB04
def test_analyse_knownDataset_resultIsSortedDescending(repo):
    repo.set_books([
        make_book("SAGE"),
        make_book("Springer"), make_book("Springer"), make_book("Springer"),
        make_book("Routledge"), make_book("Routledge"),
    ])
    result = PublisherAnalyser(repo).analyse()
    counts = list(result.values())
    assert counts == sorted(counts, reverse=True)