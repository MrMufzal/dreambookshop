from typing import Dict
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository
# Named constant — avoids magic number and makes the limit easy to change
TOP_AUTHOR_LIMIT = 5
class TopAuthorsAnalyser(IAnalyser):
    """Ranks authors by their total book count and returns the top N.
    Authors with an empty or whitespace-only name are excluded."""
    def __init__(self, repository: DataRepository) -> None:
        """Args:
            repository (DataRepository): Shared data store providing Book objects."""
        self._repository = repository
    def get_title(self) -> str:
        return f"Top {TOP_AUTHOR_LIMIT} Most Prolific Authors"
    def analyse(self) -> Dict[str, int]:
        """Counts books per author and returns the top TOP_AUTHOR_LIMIT authors.
        Returns:
            Dict[str, int]: Author name mapped to book count,
                            sorted descending by count."""
        books = self._repository.get_books()
        if not books:
            return {}
        author_counts: Dict[str, int] = {}
        for book in books:
            author = book.author.strip()
            # Skip records with no meaningful author name
            if not author:
                continue
            author_counts[author] = author_counts.get(author, 0) + 1
        # Sort by count descending and take the top N
        ranked = dict(
            sorted(author_counts.items(), key=lambda item: item[1], reverse=True)[
                :TOP_AUTHOR_LIMIT ] )
        return ranked
