from typing import Dict
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository


class PublicationTrendAnalyser(IAnalyser):
    """Counts the number of books published in each year.
    Records with a publication year of 0 (unparseable) are excluded. """

    def __init__(self, repository: DataRepository) -> None:
        """Args:
            repository (DataRepository): Shared data store providing Book objects."""
        self._repository = repository

    def get_title(self) -> str:
        return "Publication Trends Over Time"

    def analyse(self) -> Dict[int, int]:
        """Groups books by publication year and counts each group.

        Returns:
            Dict[int, int]: Year mapped to book count, sorted ascending."""
        books = self._repository.get_books()
        if not books:
            return {}
        year_counts: Dict[int, int] = {}
        for book in books:
            year = book.publication_year
            # Exclude records where year could not be parsed (stored as 0)
            if year == 0:
                continue
            year_counts[year] = year_counts.get(year, 0) + 1
        # Return sorted by year ascending for chronological display
        return dict(sorted(year_counts.items()))
