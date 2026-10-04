import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Any

from interfaces.i_visualizer import IVisualizer

OUTPUT_DIR = "output/charts/"

# Slices representing less than this % of the total are merged into 'Other'
MIN_SLICE_PERCENTAGE = 2.0
# Keys to exclude from pie chart (summary fields from MissingISBNAnalyser)
EXCLUDE_KEYS = {"Total Records", "Missing (%)"}
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)
class PieChartVisualizer(IVisualizer):
    """Renders a pie chart using matplotlib.
    Merges small slices below MIN_SLICE_PERCENTAGE into an 'Other' segment.
    Filters out non-count summary keys (e.g. 'Total Records', 'Missing (%)')."""
    def render(self, data: Any, title: str) -> None:
        """Renders a pie chart from label/count data and saves it as a PNG.
        Args:
            data  (Any): Dict[str, int] from an IAnalyser.
            title (str): Chart title from IAnalyser.get_title()."""
        if not data:
            print(f"[PieChartVisualizer] No data to render for: {title}")
            return
        # Filter out non-count summary keys (e.g. 'Total Records', 'Missing (%)')
        filtered = {
            k: v for k, v in data.items()
            if k not in EXCLUDE_KEYS and isinstance(v, (int, float)) and v > 0
        }
        if not filtered:
            print(f"[PieChartVisualizer] No plottable data for: {title}")
            return
        # Merge small slices into 'Other' to avoid visual clutter
        labels, values = self._merge_small_slices(filtered)
        fig, ax = plt.subplots(figsize=(10, 7))
        # Explode the largest slice slightly for emphasis
        explode = [0.04 if i == 0 else 0 for i in range(len(labels))]
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,          # Labels handled by legend for readability
            autopct="%1.1f%%",
            startangle=140,
            explode=explode,
            colors=plt.cm.tab20.colors[:len(labels)],
            wedgeprops={"edgecolor": "white", "linewidth": 1.5},
            pctdistance=0.82,
        )
        # Style percentage text
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color("white")
            autotext.set_fontweight("bold")
        # Legend outside the chart — cleaner than crowded slice labels
        ax.legend(
            wedges,
            [f"{l} ({v:,})" for l, v in zip(labels, values)],
            title="Category",
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            fontsize=9,
            title_fontsize=10, )
        ax.set_title(title, fontsize=13, fontweight="bold", pad=20)
        plt.tight_layout()
        filename = self._safe_filename(title)
        plt.savefig(f"{OUTPUT_DIR}{filename}.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[PieChartVisualizer] Chart saved: {OUTPUT_DIR}{filename}.png")
    def _merge_small_slices(self, data: dict) -> tuple:
        """Merges slices below MIN_SLICE_PERCENTAGE of the total into 'Other'.
        Args:
            data (dict): Filtered {label: count} dict.
        Returns:
            tuple: (labels list, values list) with small slices merged."""
        total = sum(data.values())
        labels, values, other = [], [], 0
        for label, count in data.items():
            if (count / total * 100) >= MIN_SLICE_PERCENTAGE:
                labels.append(label)
                values.append(count)
            else:
                other += count
        if other > 0:
            labels.append("Other")
            values.append(other)
        return labels, values
    @staticmethod
    def _safe_filename(title: str) -> str:
        """Converts a chart title to a safe filename string."""
        return title.lower().replace(" ", "_").replace("/", "_").replace(":", "")