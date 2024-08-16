from pathlib import Path
from data_processor import ExtendedDatabase
from plotter import (
    plot_country_values,
    plot_top_cities_over_time,
    plot_city_distribution,
    plot_country_distribution,
    plot_visited_countries_map,
)
from typing import Final

_EXAMPLE_DATA_PATH: Final[Path] = Path("data") / "ferran.csv"

db = ExtendedDatabase(_EXAMPLE_DATA_PATH)
df = db._get_dataframe()
countries_data = db.get_countries_days_lived()
cities_data = db.get_cities_days_lived()

# Generate and print basic statistics
stats = db.get_basic_stats()
print(f"Basic Statistics:\n{stats}\n")

# Generate and print city summary for a specific city (using an approximate match)
city_summary = db.get_location_summary("Lucern", exact_match=False)
print(f"City Summary for Luzern:\n{city_summary}\n")

# Generate and print country summary for a specific country
country_summary = db.get_country_summary("Italy")
print(f"Country Summary for Italy:\n{country_summary}\n")

# Generate and print year summary for a specific year
year_summary = db.get_year_summary(2022)
print(f"Year Summary for 2022:\n{year_summary}\n")

# Plot and display the distribution of days lived across countries
plot_country_distribution(df)

# Plot and display the distribution of days lived across cities
plot_city_distribution(df)

# Plot and display the top cities over time
plot_top_cities_over_time(df, top_n=10)

# Plot and display a world map with color-coded values per country
countries = countries_data["country"]
values = countries_data["total_days_lived"]
plot_country_values(countries, values)

# Print summaries
print(f"Summary of countries:\n{countries_data}\n")
print(f"Summary of cities:\n{cities_data}\n")

# Plot and display a map showing the countries visited
plot_visited_countries_map(countries)

# Plot and display the top 5 cities with the most days lived over time (cumulative)
plot_top_cities_over_time(df, top_n=5, cumulative=True)

# Plot and display the distribution of days lived across countries (without log scale)
plot_country_distribution(df, log_scale=False)

# Plot and display the distribution of days lived across cities (without log scale)
plot_city_distribution(df, log_scale=False)
