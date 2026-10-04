import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — renders to file without a display
import matplotlib.pyplot as plt
import numpy as np
from typing import Any

from interfaces.i_visualizer import IVisualizer

# Maximum bars to display for large datasets (e.g. 1,189 publishers)
MAX_BARS = 20

# Output directory for saved chart images
OUTPUT_DIR = "output/charts/"

import os
os.makedirs(OUTPUT_DIR, exist_ok=True)


class BarChartVisualizer(IVisualizer):
    """Renders bar charts using matplotlib.
    Automatically detects flat vs nested dict and renders accordingly."""

    def render(self, data: Any, title: str) -> None:
        """Renders a bar chart from the provided data and saves it as a PNG.

        Args:
            data  (Any): Dict result from an IAnalyser. Either flat or nested.
            title (str): Chart title from IAnalyser.get_title()."""
        if not data:
            print(f"[BarChartVisualizer] No data to render for: {title}")
            return

        # Detect nested dict (LanguageYearAnalyser output)
        first_value = next(iter(data.values()))
        if isinstance(first_value, dict):
            self._render_stacked(data, title)
        else:
            self._render_flat(data, title)

    def _render_flat(self, data: dict, title: str) -> None:
        """Renders a standard bar chart for flat {label: count} dicts.
        Slices to MAX_BARS for very large datasets (e.g. publishers)."""
        # Slice to top MAX_BARS entries — data is already sorted descending
        items = list(data.items())[:MAX_BARS]
        labels = [str(k) for k, _ in items]
        values = [v for _, v in items]

        # Use horizontal bars for long label strings (authors, publishers)
        horizontal = any(len(label) > 10 for label in labels)

        fig, ax = plt.subplots(figsize=(12, 6))

        if horizontal:
            # Reverse so highest value appears at top
            ax.barh(labels[::-1], values[::-1], color="#2E75B6", edgecolor="white")
            ax.set_xlabel("Number of Books", fontsize=11)
            ax.set_ylabel("")
            # Add value labels at end of each bar
            for i, v in enumerate(values[::-1]):
                ax.text(v + 0.5, i, str(v), va="center", fontsize=9)
        else:
            ax.bar(labels, values, color="#2E75B6", edgecolor="white")
            ax.set_ylabel("Number of Books", fontsize=11)
            ax.set_xlabel("")
            ax.tick_params(axis="x", rotation=45)
            # Add value labels above each bar
            for i, v in enumerate(values):
                ax.text(i, v + 0.5, str(v), ha="center", fontsize=9)

        # Subtitle note if dataset was sliced
        subtitle = f"(Top {MAX_BARS} shown)" if len(data) > MAX_BARS else ""
        ax.set_title(f"{title}\n{subtitle}", fontsize=13, fontweight="bold", pad=15)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()
        filename = self._safe_filename(title)
        plt.savefig(f"{OUTPUT_DIR}{filename}.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[BarChartVisualizer] Chart saved: {OUTPUT_DIR}{filename}.png")

    def _render_stacked(self, data: dict, title: str) -> None:
        """Renders a stacked bar chart for nested {year: {language: count}} dicts."""
        years = [str(y) for y in data.keys()]

        # Collect all language labels across all years
        all_languages: set = set()
        for lang_counts in data.values():
            all_languages.update(lang_counts.keys())

        # Sort: named languages first, 'Other' always last
        languages = sorted(
            [l for l in all_languages if l != "Other"]
        ) + (["Other"] if "Other" in all_languages else [])

        # Build a 2D array: languages x years
        counts = np.zeros((len(languages), len(years)), dtype=int)
        for col_idx, year_data in enumerate(data.values()):
            for row_idx, lang in enumerate(languages):
                counts[row_idx][col_idx] = year_data.get(lang, 0)

        # Colour palette — one per language
        colours = plt.cm.tab10.colors

        fig, ax = plt.subplots(figsize=(14, 7))
        bottoms = np.zeros(len(years))

        for row_idx, lang in enumerate(languages):
            colour = colours[row_idx % len(colours)]
            ax.bar(
                years,
                counts[row_idx],
                bottom=bottoms,
                label=lang,
                color=colour,
                edgecolor="white",
                width=0.6,
            )
            bottoms += counts[row_idx]

        ax.set_title(title, fontsize=13, fontweight="bold", pad=15)
        ax.set_xlabel("Publication Year", fontsize=11)
        ax.set_ylabel("Number of Books", fontsize=11)
        ax.legend(title="Language", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()
        filename = self._safe_filename(title)
        plt.savefig(f"{OUTPUT_DIR}{filename}.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"[BarChartVisualizer] Stacked chart saved: {OUTPUT_DIR}{filename}.png")

    @staticmethod
    def _safe_filename(title: str) -> str:
        """Converts a chart title to a safe filename string."""
        return title.lower().replace(" ", "_").replace("/", "_").replace(":", "")