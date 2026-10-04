import pandas as pd

from interfaces.i_data_loader import IDataLoader
from models.book import Book
from repository.data_repository import DataRepository
from typing import List

# Expected CSV columns — used to validate the file before processing
REQUIRED_COLUMNS = {
    "book",
    "author",
    "publication date",
    "language",
    "book publisher",
    "ISBN",
    "BNB id",
}
# Maximum rows to load — keeps prototype processing manageable
MAX_ROWS = 5000
class CSVDataLoader(IDataLoader):
    """Loads and parses the BNB dataset from a CSV file.
    Stores the resulting Book objects in the provided DataRepository. """
    def __init__(self, repository: DataRepository) -> None:
        # Dependency injected — CSVDataLoader does not create the repository itself
        self._repository = repository

    def load(self, file_path: str) -> List[Book]:
        # --- Step 1: Load CSV with pandas ---
        try:
            df = pd.read_csv(file_path, nrows=MAX_ROWS, dtype={"ISBN": str})
        except FileNotFoundError:
            raise FileNotFoundError(
                f"[CSVDataLoader] Dataset not found at: {file_path}")
        # --- Step 2: Validate columns ---
        missing_cols = REQUIRED_COLUMNS - set(df.columns)
        if missing_cols:
            raise ValueError(
                f"[CSVDataLoader] Missing expected columns: {missing_cols}")
        # --- Step 3: Clean data ---
        # Fill missing publisher and ISBN with empty string (not NaN)
        # so Book.has_isbn() and analyser logic work consistently
        df["book publisher"] = df["book publisher"].fillna("")
        df["ISBN"] = df["ISBN"].fillna("")
        # Ensure publication date is integer where possible; coerce errors to 0
        df["publication date"] = pd.to_numeric(
            df["publication date"], errors="coerce" ).fillna(0).astype(int)
        # --- Step 4: Map rows to Book objects ---
        books: List[Book] = []
        for _, row in df.iterrows():
            book = Book(
                title=str(row["book"]).strip(),
                author=str(row["author"]).strip(),
                publication_year=int(row["publication date"]),
                language=str(row["language"]).strip(),
                publisher=str(row["book publisher"]).strip(),
                isbn=str(row["ISBN"]).strip(),
                bnb_id=str(row["BNB id"]).strip(),)
            books.append(book)
        # --- Step 5: Store in repository ---
        self._repository.set_books(books)
        print(f"[CSVDataLoader] Loaded {len(books)} books from '{file_path}'.")
        return books
