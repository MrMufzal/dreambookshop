from typing import List
from interfaces.i_analyser import IAnalyser
from repository.data_repository import DataRepository
from analysers.publication_trend_analyser import PublicationTrendAnalyser
from analysers.top_authors_analyser import TopAuthorsAnalyser
from analysers.language_distribution_analyser import LanguageDistributionAnalyser
from analysers.publisher_analyser import PublisherAnalyser
from analysers.missing_isbn_analyser import MissingISBNAnalyser
from analysers.language_year_analyser import LanguageYearAnalyser
class AnalyserFactory:
    """Creates and returns all IAnalyser instances for the application.
    Each analyser receives the shared DataRepository as a dependency. """

    def __init__(self, repository: DataRepository) -> None:
        """ Initialises the factory with the shared DataRepository.
        Args:
            repository (DataRepository): The data store all analysers
                                          will read from. """
        self._repository = repository

    def create_all(self) -> List[IAnalyser]:
        """Instantiates and returns all six required analyser objects
        in the order they will be executed by the ApplicationController.
        Returns:
            List[IAnalyser]: All concrete analyser instances."""
        return [
            PublicationTrendAnalyser(self._repository),
            TopAuthorsAnalyser(self._repository),
            LanguageDistributionAnalyser(self._repository),
            PublisherAnalyser(self._repository),
            MissingISBNAnalyser(self._repository),
            LanguageYearAnalyser(self._repository), ]
