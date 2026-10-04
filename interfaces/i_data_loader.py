from abc import ABC, abstractmethod
from typing import List

from models.book import Book


class IDataLoader(ABC):
    """
    Abstract interface for all data loader implementations.
    Concrete loaders (e.g. CSVDataLoader) must implement load().
    """

    @abstractmethod
    def load(self, file_path: str) -> List[Book]:
        pass