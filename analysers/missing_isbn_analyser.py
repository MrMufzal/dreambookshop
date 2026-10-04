from typing import Dict, Union
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository
# Rounding precision for percentage display
PERCENTAGE_DECIMAL_PLACES = 2
class MissingISBNAnalyser(IAnalyser):
    """Counts records with and without a valid ISBN value. Uses Book.has_isbn() to determine presence consistently."""
    def __init__(self, repository: DataRepository) -> None:
        """Args: repository (DataRepository): Shared data store providing Book objects."""
        self._repository = repository
    def get_title(self) -> str:
        return "Missing ISBN Analysis"
    def analyse(self) -> Dict[str, Union[int, float]]:
        """Counts books with and without ISBNs, and calculates the missing percentage.
        Returns: Dict[str, Union[int, float]]: Summary of ISBN presence across the dataset."""
        books = self._repository.get_books()
        total = len(books)
        if total == 0:
            return {
                "With ISBN": 0,
                "Missing ISBN": 0,
                "Total Records": 0,
                "Missing (%)": 0.0, }
        missing_count = self._count_missing(books)
        present_count = total - missing_count
        missing_percentage = round(
            (missing_count / total) * 100, PERCENTAGE_DECIMAL_PLACES )
        return {
            "With ISBN": present_count,
            "Missing ISBN": missing_count,
            "Total Records": total,
            "Missing (%)": missing_percentage,}
    def _count_missing(self, books) -> int:
        """Counts the number of Book objects where has_isbn() returns False.
        Args:books (List[Book]): The full list of Book objects from the repository.
        Returns: int: Number of books with a missing or empty ISBN."""
        return sum(1 for book in books if not book.has_isbn())