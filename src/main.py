"""Main module.

Collects tests and proofs-of-concept.
"""

from pathlib import Path
from data_processor import ExtendedDatabase
from plotter import (
    plot_country_values,
    plot_top_cities_over_time,
    plot_city_distribution,
    plot_country_distribution,
)
from typing import Final

_EXAMPLE_DATA_PATH: Final[Path] = Path("data") / "ferran.csv"


def main(file_path: Path = _EXAMPLE_DATA_PATH):
    """Main routine."""

    db = ExtendedDatabase(file_path)

    # Generate and print basic statistics
    stats = db.get_basic_stats()
    print(f"Basic Statistics:\n{stats}\n")

    # Generate and print city summary for a specific city (note that "Castelló" is not well written)
    city_summary = db.get_location_summary("Castello", exact_match=False)
    print(f"City Summary for Castelló:\n{city_summary}\n")

    # Generate and print country summary for a specific country
    country_summary = db.get_country_summary("Spain")
    print(f"Country Summary for Spain:\n{country_summary}\n")

    # Generate and print year summary for a specific year
    year_summary = db.get_year_summary(2023)
    print(f"Year Summary for 2023:\n{year_summary}\n")

    # Generate and plot country values
    countries_data = db.get_countries_days_lived()
    plot_country_values(
        countries_data["country"],
        countries_data["total_days_lived"],
    )

    # Plot top 10 cities with most days lived over time, excluding the first most important one
    df = db._get_dataframe()  # Using the internal method to get the raw data
    plot_top_cities_over_time(
        df, top_n=10, cumulative=True, exclude_top=1, log_scale=False
    )

    # Plot the distribution of days lived across different cities
    plot_city_distribution(df, log_scale=True)

    # Plot the distribution of days lived across different countries
    plot_country_distribution(df, log_scale=True)


if __name__ == "__main__":
    main()
