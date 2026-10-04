class Book:
    """A plain data model class representing one row from the BNB dataset. Holds data only """
    def __init__(
        self,
        title: str,
        author: str,
        publication_year: int,
        language: str,
        publisher: str,
        isbn: str,
        bnb_id: str,
    ) -> None:
        """ Initialises a Book instance with all fields from the BNB dataset. """
        self._title = title
        self._author = author
        self._publication_year = publication_year
        self._language = language
        self._publisher = publisher
        self._isbn = isbn
        self._bnb_id = bnb_id
    # ------------------------------------------------------------------ #
    # Getters: controlled read-only access to private fields             #
    # ------------------------------------------------------------------ #
    @property
    def title(self) -> str:
        """Returns the book title."""
        return self._title
    @property
    def author(self) -> str:
        """Returns the author name."""
        return self._author
    @property
    def publication_year(self) -> int:
        """Returns the publication year."""
        return self._publication_year
    @property
    def language(self) -> str:
        """Returns the language of the book."""
        return self._language
    @property
    def publisher(self) -> str:
        """Returns the publisher name."""
        return self._publisher
    @property
    def isbn(self) -> str:
        """Returns the ISBN. May be an empty string if missing in the dataset."""
        return self._isbn
    @property
    def bnb_id(self) -> str:
        """Returns the unique BNB identifier."""
        return self._bnb_id
    # ------------------------------------------------------------------ #
    # Utility                                                             #
    # ------------------------------------------------------------------ #
    def has_isbn(self) -> bool:
        """Returns True if the book has a non-empty ISBN value. Used by MissingISBNAnalyser to identify incomplete records. """
        return bool(self._isbn and self._isbn.strip())
    def __repr__(self) -> str:
        return (
            f"Book(title={self._title!r}, author={self._author!r}, "
            f"year={self._publication_year}, language={self._language!r}, "
            f"publisher={self._publisher!r}, isbn={self._isbn!r}, "
            f"bnb_id={self._bnb_id!r})" )
