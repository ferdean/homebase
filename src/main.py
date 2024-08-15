from pathlib import Path
from plotter import plot_country_values, plot_top_cities_over_time
from data_processor import ExtendedDatabase


def main():
    db = ExtendedDatabase(Path("data") / "ferran.csv")

    # Generate and plot country values
    # countries_data = db.get_countries_days_lived()
    # plot_country_values(countries_data["country"], countries_data["total_days_lived"])

    # Plot top 10 cities with most days lived over time
    df = db._get_dataframe()  # Using the internal method to get the raw data
    plot_top_cities_over_time(df, top_n=15, cumulative=False)


if __name__ == "__main__":
    main()
