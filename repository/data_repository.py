from typing import List
from models.book import Book


class DataRepository:
    """ Stores and provides controlled access to the loaded Book dataset.
    Populated by CSVDataLoader after the CSV is parsed. """
    def __init__(self) -> None:
        """Initialises an empty repository."""
        # Private list — external classes cannot manipulate it directly
        self._books: List[Book] = []
    def set_books(self, books: List[Book]) -> None:
        """Populates the repository with a list of Book objects.
        Called by CSVDataLoader once parsing is complete.
        Args: books (List[Book]): The full list of parsed Book objects."""
        self._books = books
    def get_books(self) -> List[Book]:
        """Returns the full list of loaded Book objects.
        Called by analyser classes to retrieve the dataset.
        Returns: List[Book]: All Book objects currently in the repository."""
        return self._books
    def count(self) -> int:
        """Returns the total number of books in the repository.
        Returns: int: Number of Book records loaded."""
        return len(self._books)
    def is_empty(self) -> bool:
        """ Returns True if no books have been loaded yet. Useful for defensive checks in analyser classes.
        Returns: bool: True if the repository contains no books."""
        return len(self._books) == 0
    def __repr__(self) -> str:
        return f"DataRepository(books={len(self._books)} records)"
