"""
tests/test_application_controller.py
--------------------------------------
Unit tests for ApplicationController: covers TC01 through TC05.
Uses unittest.mock to inject mock dependencies, testing orchestration
logic in full isolation from real loaders, analysers, and visualizers.
"""

import pytest
from unittest.mock import MagicMock, patch, call
from controllers.application_controller import ApplicationController
from repository.data_repository import DataRepository
from models.book import Book


def make_book():
    return Book("Title", "Author", 2023, "English", "Publisher", "1234567890", "BNB001")


def make_mock_analyser(title="Test Analysis", result={"key": 1}):
    """Creates a mock IAnalyser with controlled return values."""
    analyser = MagicMock()
    analyser.get_title.return_value = title
    analyser.analyse.return_value = result
    return analyser


def make_mock_visualizer():
    """Creates a mock IVisualizer."""
    return MagicMock()


def make_mock_loader(repo, books=None):
    """Creates a mock IDataLoader that populates the repo."""
    if books is None:
        books = [make_book()]

    def load_side_effect(path):
        repo.set_books(books)
        return books

    loader = MagicMock()
    loader.load.side_effect = load_side_effect
    return loader


def make_controller(repo, loader, analysers, visualizers):
    output = MagicMock()
    return ApplicationController(
        loader=loader,
        repository=repo,
        analysers=analysers,
        visualizers=visualizers,
        output_handler=output,
        file_path="dummy/path.csv",
    ), output


# TC01
def test_run_validData_callsAnalyseOnEachAnalyser():
    repo = DataRepository()
    analysers = [make_mock_analyser(f"Analysis {i}") for i in range(3)]
    visualizers = [make_mock_visualizer() for _ in range(3)]
    loader = make_mock_loader(repo)
    controller, _ = make_controller(repo, loader, analysers, visualizers)

    controller.run()

    for analyser in analysers:
        analyser.analyse.assert_called_once()


# TC02
def test_run_validData_callsRenderOnEachVisualizer():
    repo = DataRepository()
    analysers = [make_mock_analyser(f"Analysis {i}") for i in range(3)]
    visualizers = [make_mock_visualizer() for _ in range(3)]
    loader = make_mock_loader(repo)
    controller, _ = make_controller(repo, loader, analysers, visualizers)

    controller.run()

    for visualizer in visualizers:
        visualizer.render.assert_called_once()


# TC03
def test_run_emptyRepository_stopsAfterLoadWithoutAnalysing():
    repo = DataRepository()
    analyser = make_mock_analyser()
    visualizer = make_mock_visualizer()

    # Loader that leaves the repo empty
    loader = MagicMock()
    loader.load.side_effect = lambda path: repo.set_books([]) or []

    controller, _ = make_controller(repo, loader, [analyser], [visualizer])
    controller.run()

    analyser.analyse.assert_not_called()
    visualizer.render.assert_not_called()


# TC04
def test_init_mismatchedAnalyserVisualiserCount_raisesValueError():
    repo = DataRepository()
    loader = MagicMock()
    output = MagicMock()

    with pytest.raises(ValueError):
        ApplicationController(
            loader=loader,
            repository=repo,
            analysers=[make_mock_analyser(), make_mock_analyser()],
            visualizers=[make_mock_visualizer()],
            output_handler=output,
        )


# TC05
def test_run_validData_passesCorrectTitleToVisualizer():
    repo = DataRepository()
    analyser = make_mock_analyser(title="Publication Trends Over Time", result={2023: 10})
    visualizer = make_mock_visualizer()
    loader = make_mock_loader(repo)
    controller, _ = make_controller(repo, loader, [analyser], [visualizer])

    controller.run()

    visualizer.render.assert_called_once_with(
        data={2023: 10},
        title="Publication Trends Over Time"
    )