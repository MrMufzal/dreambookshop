"""
tests/test_language_distribution_analyser.py
----------------------------------------------
Unit tests for LanguageDistributionAnalyser: covers TLD01 through TLD04.
"""

import pytest
from repository.data_repository import DataRepository
from analysers.language_distribution_analyser import LanguageDistributionAnalyser
from models.book import Book


def make_book(language):
    return Book("Title", "Author", 2023, language, "Publisher", "1234567890", "BNB001")


@pytest.fixture
def repo():
    return DataRepository()


# TLD01
def test_analyse_knownDataset_returnsCorrectLanguageCounts(repo):
    repo.set_books([
        make_book("English"), make_book("English"), make_book("English"),
        make_book("French"), make_book("French"),
        make_book("Arabic"),
    ])
    result = LanguageDistributionAnalyser(repo).analyse()
    assert result["English"] == 3
    assert result["French"] == 2
    assert result["Arabic"] == 1


# TLD02
def test_analyse_emptyRepository_returnsEmptyDict(repo):
    repo.set_books([])
    result = LanguageDistributionAnalyser(repo).analyse()
    assert result == {}


# TLD03
def test_analyse_singleLanguage_returnsSingleEntry(repo):
    repo.set_books([make_book("English")] * 5)
    result = LanguageDistributionAnalyser(repo).analyse()
    assert result == {"English": 5}


# TLD04
def test_analyse_knownDataset_resultIsSortedDescending(repo):
    repo.set_books([
        make_book("Arabic"),
        make_book("English"), make_book("English"), make_book("English"),
        make_book("French"), make_book("French"),
    ])
    result = LanguageDistributionAnalyser(repo).analyse()
    counts = list(result.values())
    assert counts == sorted(counts, reverse=True)