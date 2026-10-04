from typing import Dict
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository

class PublisherAnalyser(IAnalyser):
    """Counts books grouped by publisher name.
    Records with a missing or empty publisher are excluded."""

    def __init__(self, repository: DataRepository) -> None:
        """Args:
            repository (DataRepository): Shared data store providing Book objects."""
        self._repository = repository
    def get_title(self) -> str:
        return "Books Published by Each Publisher"

    def analyse(self) -> Dict[str, int]:
        """Groups books by publisher and counts each group.
        Returns:
            Dict[str, int]: Publisher name mapped to book count,
                            sorted descending by count."""
        books = self._repository.get_books()
        if not books:
            return {}
        publisher_counts: Dict[str, int] = {}
        for book in books:
            publisher = book.publisher.strip()
            # Exclude the 73 records where publisher was null in the CSV
            if not publisher:
                continue
            publisher_counts[publisher] = publisher_counts.get(publisher, 0) + 1
        # Sort by count descending
        return dict(
            sorted(publisher_counts.items(), key=lambda item: item[1], reverse=True)
        )
