"""
tests/test_language_year_analyser.py
--------------------------------------
Unit tests for LanguageYearAnalyser: covers TLY01 through TLY05.
"""

import pytest
from repository.data_repository import DataRepository
from analysers.language_year_analyser import LanguageYearAnalyser
from models.book import Book


def make_book(year, language):
    return Book("Title", "Author", year, language, "Publisher", "1234567890", "BNB001")


@pytest.fixture
def repo():
    return DataRepository()


# TLY01
def test_analyse_knownDataset_returnsCorrectNestedStructure(repo):
    repo.set_books([
        make_book(2021, "English"), make_book(2021, "English"),
        make_book(2021, "French"),
        make_book(2022, "English"),
    ])
    result = LanguageYearAnalyser(repo).analyse()
    assert 2021 in result
    assert 2022 in result
    assert result[2021]["English"] == 2
    assert result[2021]["French"] == 1
    assert result[2022]["English"] == 1


# TLY02
def test_analyse_emptyRepository_returnsEmptyDict(repo):
    repo.set_books([])
    result = LanguageYearAnalyser(repo).analyse()
    assert result == {}


# TLY03
def test_analyse_manyLanguages_groupsSmallLanguagesAsOther(repo):
    # 6 languages — top 5 kept, 6th grouped as Other
    languages = ["English", "French", "German", "Arabic", "Russian", "Japanese"]
    books = []
    for i, lang in enumerate(languages):
        books += [make_book(2022, lang)] * (10 - i)
    repo.set_books(books)
    result = LanguageYearAnalyser(repo).analyse()
    year_data = result[2022]
    assert "Other" in year_data
    assert "Japanese" not in year_data


# TLY04
def test_analyse_knownDataset_resultIsSortedByYearAscending(repo):
    repo.set_books([
        make_book(2023, "English"),
        make_book(2019, "English"),
        make_book(2021, "English"),
    ])
    result = LanguageYearAnalyser(repo).analyse()
    assert list(result.keys()) == sorted(result.keys())


# TLY05
def test_analyse_booksWithYearZero_excludesYearZero(repo):
    repo.set_books([make_book(0, "English"), make_book(2022, "English")])
    result = LanguageYearAnalyser(repo).analyse()
    assert 0 not in result
    assert 2022 in result