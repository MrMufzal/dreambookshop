from abc import ABC, abstractmethod
from typing import Any


class IVisualizer(ABC):
    """ Abstract interface for all chart visualizer implementations.
    Concrete visualizers must implement render(). """

    @abstractmethod
    def render(self, data: Any, title: str) -> None:
        pass