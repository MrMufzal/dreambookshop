import argparse
import sys
from repository.data_repository import DataRepository
from loaders.csv_data_loader import CSVDataLoader
from factories.analyser_factory import AnalyserFactory
from factories.visualizer_factory import VisualizerFactory
from output.cli_output_handler import CLIOutputHandler
from controllers.application_controller import ApplicationController

DEFAULT_DATASET_PATH = "data/bnb_dataset.csv"
def parse_args() -> argparse.Namespace:
    """ Parses command-line arguments.
    Returns: argparse.Namespace: Parsed arguments with a 'file' attribute. """
    parser = argparse.ArgumentParser(
        description="Dream Book Shop: BNB Data Analysis CLI Application" )
    parser.add_argument(
        "--file",
        type=str,
        default=DEFAULT_DATASET_PATH,
        help=f"Path to the BNB CSV dataset (default: {DEFAULT_DATASET_PATH})",
    )
    return parser.parse_args()
def main() -> None:
    """Bootstraps and runs the Dream Book Shop data analysis application.
    All dependencies are constructed here and injected, no component
    creates its own dependencies internally."""
    args = parse_args()
    # --- Step 1: Shared data store ---
    repository = DataRepository()
    # --- Step 2: Data loader (depends on repository) ---
    loader = CSVDataLoader(repository)
    # --- Step 3: Analysers (all depend on repository) ---
    analyser_factory = AnalyserFactory(repository)pip install coverage
coverage run -m pytest tests/
coverage report -m
    analysers = analyser_factory.create_all()
    # --- Step 4: Visualizers (paired by index with analysers) ---
    visualizer_factory = VisualizerFactory()
    visualizers = visualizer_factory.create_all()
    # --- Step 5: CLI output handler ---
    output_handler = CLIOutputHandler()
    # --- Step 6: Controller (depends on all abstractions) ---
    controller = ApplicationController(
        loader=loader,
        repository=repository,
        analysers=analysers,
        visualizers=visualizers,
        output_handler=output_handler,
        file_path=args.file, )
    # --- Step 7: Run ---
    try:
        controller.run()
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("Please check the dataset path and try again.")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()