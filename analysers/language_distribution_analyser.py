from typing import Dict
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository

class LanguageDistributionAnalyser(IAnalyser):
    """Counts the number of books per language.
    Records with an empty or whitespace-only language field are excluded."""

    def __init__(self, repository: DataRepository) -> None:
        """Args:
            repository (DataRepository): Shared data store providing Book objects."""
        self._repository = repository
    def get_title(self) -> str:
        return "Language Distribution of Books"
    def analyse(self) -> Dict[str, int]:
        """Groups books by language and counts each group.
        Returns:
            Dict[str, int]: Language mapped to book count,
                            sorted descending by count. """
        books = self._repository.get_books()

        if not books:
            return {}
        language_counts: Dict[str, int] = {}
        for book in books:
            language = book.language.strip()
            # Skip records with no meaningful language value
            if not language:
                continue
            language_counts[language] = language_counts.get(language, 0) + 1
        # Sort by count descending — most represented languages shown first
        return dict(
            sorted(language_counts.items(), key=lambda item: item[1], reverse=True)
        )
