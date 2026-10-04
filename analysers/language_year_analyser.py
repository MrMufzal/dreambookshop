from typing import Dict
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository
# Number of languages to display individually — rest grouped as 'Other'
TOP_LANGUAGE_LIMIT = 5
# Label used for all languages outside the top N
OTHER_LABEL = "Other"
class LanguageYearAnalyser(IAnalyser):
    """Groups books by publication year and language.
    Only the top TOP_LANGUAGE_LIMIT languages are shown individually;
    all others are aggregated under 'Other'.
    Records with year == 0 are excluded. """
    def __init__(self, repository: DataRepository) -> None:
        """Args: repository (DataRepository): Shared data store providing Book objects."""
        self._repository = repository
    def get_title(self) -> str:
        return "Books per Year Categorised by Language"
    def analyse(self) -> Dict[int, Dict[str, int]]:
        """Builds a nested dict of year → language → count.
        Languages outside the top N are merged into 'Other'.
        Returns:
            Dict[int, Dict[str, int]]: Nested year/language count structure,
                                       sorted by year ascending."""
        books = self._repository.get_books()
        if not books:
            return {}
        # --- Step 1: Identify top languages by total book count ---
        top_languages = self._get_top_languages(books)

        # --- Step 2: Build nested year → language → count structure ---
        year_language_counts: Dict[int, Dict[str, int]] = {}

        for book in books:
            year = book.publication_year
            language = book.language.strip()
            # Exclude unparseable years
            if year == 0 or not language:
                continue

            if year not in year_language_counts:
                year_language_counts[year] = {}

            # Assign to named language or 'Other'
            label = language if language in top_languages else OTHER_LABEL
            year_language_counts[year][label] = (
                year_language_counts[year].get(label, 0) + 1
            )
        # --- Step 3: Return sorted by year ascending ---
        return dict(sorted(year_language_counts.items()))
    def _get_top_languages(self, books) -> set:
        """Determines the top TOP_LANGUAGE_LIMIT languages by total book count.
        Args: books (List[Book]): All books from the repository.
        Returns: set: The names of the top N languages."""
        language_totals: Dict[str, int] = {}
        for book in books:
            language = book.language.strip()
            if language:
                language_totals[language] = language_totals.get(language, 0) + 1
        top = sorted(language_totals.items(), key=lambda x: x[1], reverse=True)[
            :TOP_LANGUAGE_LIMIT
        ]
        return {lang for lang, _ in top}