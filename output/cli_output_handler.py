from typing import Any
SEPARATOR = "=" * 60
THIN_LINE = "-" * 60
class CLIOutputHandler:
    """Formats and prints structured output to the terminal.
    Called by ApplicationController after each analysis step."""
    def print_header(self, title: str) -> None:
        """Prints a prominent header block."""
        print(f"\n{SEPARATOR}")
        print(f"  {title.upper()}")
        print(f"{SEPARATOR}\n")
    def print_section(self, title: str) -> None:
        """Prints a section heading for each analysis."""
        print(f"\n{THIN_LINE}")
        print(f"  {title}")
        print(f"{THIN_LINE}")
    def print_info(self, message: str) -> None:
        """Prints a general informational message."""
        print(f"[INFO]  {message}")
    def print_error(self, message: str) -> None:
        """Prints an error message."""
        print(f"[ERROR] {message}")
    def print_result(self, result: Any) -> None:
        """Prints the analysis result as a readable textual summary.
        Handles dict, list, and tuple result types returned by analysers.
        Args: result (Any): The structured result from an IAnalyser.analyse() call."""
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"  {key}: {value}")
        elif isinstance(result, list):
            for index, item in enumerate(result, start=1):
                print(f"  {index}. {item}")
        elif isinstance(result, tuple) and len(result) == 2:
            # Handles (labels, values) tuple format from some analysers
            labels, values = result
            for label, value in zip(labels, values):
                print(f"  {label}: {value}")
        else:
            print(f"  {result}")
