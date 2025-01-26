import re
from typing import List, Optional

import pandas as pd


def caption_to_label(caption: str) -> str:
    """Convert a caption to a valid LaTeX label format."""
    return f"tab:{re.sub(r'[^a-z0-9_]', '_', caption.lower()).strip('_')}"


def print_latex_table(
    df: pd.DataFrame,
    value_cols: List[str],
    caption: str,
    label: Optional[str] = None,
    float_format: str = "%.2f",
) -> None:
    """
    Create and print a LaTeX table from a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    value_cols : List[str]
        List of columns to include [year_col, value_col, return_col]
    caption : str
        Table caption
    label : Optional[str]
        Table label (if None, will be generated from caption)
    float_format : str
        Format for floating point numbers
    """
    if label is None:
        label = caption_to_label(caption)

    print(
        df[value_cols]
        .to_latex(
            index=False,
            float_format=float_format,
            caption=caption,
            label=label,
            column_format="l" + "r" * len(value_cols),
        )
        .replace("\\begin{table}", "\\begin{table}[H]\n\\centering")
    )


def print_summary_statistics(df, columns=None):
    """Create summary statistics table with mode and median."""
    if columns is None:
        columns = df.select_dtypes(include=["float64", "int64"]).columns

    stats = []
    for col in columns:
        col_stats = {
            "Statistic": col,
            "Mean": df[col].mean(),
            "Median": df[col].median(),
            "Mode": df[col].mode().iloc[0],
            "Std Dev": df[col].std(),
            "Min": df[col].min(),
            "Max": df[col].max(),
        }
        stats.append(col_stats)

    stats_df = pd.DataFrame(stats).set_index("Statistic")

    return print_latex_table(
        stats_df.round(2),
        value_cols=["Mean", "Median", "Mode", "Std Dev", "Min", "Max"],
        caption="Summary Statistics",
        label="tab:summary_stats",
        # column_format="lrrrrrr"
    )
