from abc import ABC, abstractmethod
from typing import Any


class IAnalyser(ABC):
    """ Abstract interface for all data analyser implementations.
        Concrete analysers must implement analyse() and get_title(). """
    @abstractmethod
    def analyse(self) -> Any:
        pass

    @abstractmethod
    def get_title(self) -> str:
        pass