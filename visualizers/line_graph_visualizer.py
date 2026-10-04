import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Any
from interfaces.i_visualizer import IVisualizer
OUTPUT_DIR = "output/charts/"
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)
class LineGraphVisualizer(IVisualizer):
    """Renders a line graph using matplotlib.
    Expects a flat Dict[int, int] with years as keys and counts as values."""
    def render(self, data: Any, title: str) -> None:
        """Renders a line graph from year/count data and saves it as a PNG.
        Args:
            data  (Any): Dict[int, int] from PublicationTrendAnalyser.
            title (str): Chart title from IAnalyser.get_title()."""
        if not data:
            print(f"[LineGraphVisualizer] No data to render for: {title}")
            return
        years = [str(k) for k in data.keys()]
        counts = list(data.values())
        fig, ax = plt.subplots(figsize=(12, 6))
        # Draw line with circular markers at each data point
        ax.plot(
            years,
            counts,
            color="#2E75B6",
            linewidth=2.5,
            marker="o",
            markersize=7,
            markerfacecolor="#1F4E79",
            markeredgecolor="white",
            markeredgewidth=1.5, )
        # Shade area under the line for visual emphasis
        ax.fill_between(years, counts, alpha=0.12, color="#2E75B6")
        # Annotate each point with its count value
        for x, y in zip(years, counts):
            ax.annotate(
                str(y),
                xy=(x, y),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                color="#1F4E79", )
        ax.set_title(title, fontsize=13, fontweight="bold", pad=15)
        ax.set_xlabel("Publication Year", fontsize=11)
        ax.set_ylabel("Number of Books", fontsize=11)
        ax.set_ylim(bottom=0)
        ax.tick_params(axis="x", rotation=45)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        plt.tight_layout()
        filename = self._safe_filename(title)
        plt.savefig(f"{OUTPUT_DIR}{filename}.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[LineGraphVisualizer] Chart saved: {OUTPUT_DIR}{filename}.png")
    @staticmethod
    def _safe_filename(title: str) -> str:
        """Converts a chart title to a safe filename string."""
        return title.lower().replace(" ", "_").replace("/", "_").replace(":", "")