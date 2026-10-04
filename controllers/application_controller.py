from typing import List
from interfaces.i_data_loader import IDataLoader
from interfaces.i_analyser import IAnalyser
from interfaces.i_visualizer import IVisualizer
from repository.data_repository import DataRepository
from output.cli_output_handler import CLIOutputHandler
# Path to the BNB dataset — could be made configurable via args or config file
DEFAULT_DATASET_PATH = "data/bnb_dataset.csv"

class ApplicationController:
    """Central orchestrator for the Dream Book Shop CLI application.
    Coordinates loading, analysis, visualisation, and CLI output."""
    def __init__(
        self,
        loader: IDataLoader,
        repository: DataRepository,
        analysers: List[IAnalyser],
        visualizers: List[IVisualizer],
        output_handler: CLIOutputHandler,
        file_path: str = DEFAULT_DATASET_PATH,
    ) -> None:
        if len(analysers) != len(visualizers):
            raise ValueError(
                f"[ApplicationController] Mismatch: {len(analysers)} analysers "
                f"but {len(visualizers)} visualizers. They must be equal."
            )

        self._loader = loader
        self._repository = repository
        self._analysers = analysers
        self._visualizers = visualizers
        self._output_handler = output_handler
        self._file_path = file_path

    def run(self) -> None:
        self._output_handler.print_header("Dream Book Shop — Data Analysis Report")

        # --- Step 1: Load data ---
        self._output_handler.print_section("Loading Dataset")
        self._loader.load(self._file_path)
        self._output_handler.print_info(
            f"Dataset loaded: {self._repository.count()} records found."
        )

        if self._repository.is_empty():
            self._output_handler.print_error(
                "No data was loaded. Please check the dataset file and try again."
            )
            return

        # --- Step 2: Run each analyser and render corresponding visualizer ---
        for analyser, visualizer in zip(self._analysers, self._visualizers):
            title = analyser.get_title()
            self._output_handler.print_section(title)
            # Run analysis
            result = analyser.analyse()
            # Print textual summary
            self._output_handler.print_result(result)
            # Render chart
            visualizer.render(data=result, title=title)
        # --- Step 3: Done ---
        self._output_handler.print_header("Analysis Complete")
