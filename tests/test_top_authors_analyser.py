"""
tests/test_top_authors_analyser.py
------------------------------------
Unit tests for TopAuthorsAnalyser: covers TA01 through TA05.
"""

import pytest
from repository.data_repository import DataRepository
from analysers.top_authors_analyser import TopAuthorsAnalyser
from models.book import Book


def make_book(author):
    return Book("Title", author, 2023, "English", "Publisher", "1234567890", "BNB001")


@pytest.fixture
def repo():
    return DataRepository()


# TA01
def test_analyse_knownDataset_returnsTop5Authors(repo):
    books = (
        [make_book("Alice")] * 10 +
        [make_book("Bob")] * 8 +
        [make_book("Carol")] * 6 +
        [make_book("Dave")] * 4 +
        [make_book("Eve")] * 2 +
        [make_book("Frank")] * 1
    )
    repo.set_books(books)
    result = TopAuthorsAnalyser(repo).analyse()
    assert len(result) == 5
    assert "Alice" in result
    assert "Frank" not in result


# TA02
def test_analyse_emptyRepository_returnsEmptyDict(repo):
    repo.set_books([])
    result = TopAuthorsAnalyser(repo).analyse()
    assert result == {}


# TA03
def test_analyse_fewerThan5Authors_returnsAllAuthors(repo):
    repo.set_books([make_book("Alice"), make_book("Bob"), make_book("Alice")])
    result = TopAuthorsAnalyser(repo).analyse()
    assert len(result) == 2
    assert "Alice" in result
    assert "Bob" in result


# TA04
def test_analyse_tiedCounts_doesNotCrash(repo):
    repo.set_books([make_book("Alice"), make_book("Bob"), make_book("Carol")])
    try:
        TopAuthorsAnalyser(repo).analyse()
    except Exception as e:
        pytest.fail(f"analyse() raised an exception on tied counts: {e}")


# TA05
def test_analyse_knownDataset_firstEntryIsHighestCount(repo):
    repo.set_books([make_book("Alice")] * 5 + [make_book("Bob")] * 3)
    result = TopAuthorsAnalyser(repo).analyse()
    first_count = list(result.values())[0]
    assert first_count == 5