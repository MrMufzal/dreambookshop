from typing import List

from interfaces.i_visualizer import IVisualizer
from visualizers.bar_chart_visualizer import BarChartVisualizer
from visualizers.line_graph_visualizer import LineGraphVisualizer
from visualizers.pie_chart_visualizer import PieChartVisualizer


class VisualizerFactory:
    """
    Creates and returns all IVisualizer instances for the application,
    paired in order with the analysers created by AnalyserFactory.
    """

    def create_all(self) -> List[IVisualizer]:
        """
        Instantiates and returns all visualizer objects in the order
        that corresponds to the analyser list from AnalyserFactory.

        Returns:
            List[IVisualizer]: All concrete visualizer instances.
        """
        return [
            LineGraphVisualizer(),    # Publication trends over time
            BarChartVisualizer(),     # Top 5 most prolific authors
            PieChartVisualizer(),     # Language distribution
            BarChartVisualizer(),     # Books per publisher
            PieChartVisualizer(),     # Missing ISBN analysis
            BarChartVisualizer(),     # Books per year by language
        ]
