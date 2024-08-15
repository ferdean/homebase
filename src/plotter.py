from data_processor import ExtendedDatabase
from geopandas import read_file, GeoDataFrame
import matplotlib.pyplot as plt
import geopandas as gpd
from pathlib import Path
from typing import Final
from math import log

_SHAPEFILE_PATH: Final[Path] = (
    Path("data") / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"
)

# Note: These plots are preliminary drafts, focusing on functionality.
# Aesthetic and formatting improvements will be included in a future commit.


def plot_country_values(
    countries: list[str], values: list[int], shapefile_path: Path = _SHAPEFILE_PATH
) -> None:
    """Plots a world map with values associated with specific countries."""
    if len(countries) != len(values):
        raise ValueError("Length of 'countries' and 'values' lists must be the same.")

    world: GeoDataFrame = read_file(shapefile_path)

    world = world.set_index("NAME")
    world["VALUES"] = 0
    for country, value in zip(countries, values):
        if country in world.index:
            world.loc[country, "VALUES"] = log(value)
        else:
            print(f"Warning: Country '{country}' not found in the shapefile. Skipping.")

    _, ax = plt.subplots(1, 1, figsize=(15, 10))
    world.boundary.plot(ax=ax, linewidth=1, color="black")
    world.plot(
        column="VALUES",
        ax=ax,
        legend=True,
        missing_kwds={"color": "lightgrey"},
        legend_kwds={"label": "Values by Country", "orientation": "horizontal"},
        cmap="OrRd",
    )
    plt.title("World Map with Values Per Country")
    plt.show()


def plot_top_cities_over_time(
    df: gpd.GeoDataFrame, top_n: int = 10, cumulative: bool = False
) -> None:
    """Plots the top N cities with the most days lived over time, optionally cumulative."""
    city_year_data = (
        df.groupby(["city", "year"])["days_lived"].sum().unstack().fillna(0)
    )

    top_cities = city_year_data.sum(axis=1).nlargest(top_n).index
    city_year_data = city_year_data.loc[top_cities]

    if cumulative:
        city_year_data = city_year_data.cumsum(axis=1)

    # Plot the data
    city_year_data.T.plot(kind="line", figsize=(15, 10), marker="o")
    title = f"Top {top_n} Cities with Most Days Lived Over Time"
    if cumulative:
        title += " (Cumulative)"
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Days Lived")
    plt.legend(title="City")
    plt.grid(True)
    plt.show()


def _list_available_countries(shapefile_path: Path = _SHAPEFILE_PATH) -> list[str]:
    """Lists all available country names from the shapefile.

    NOTE: This function has only debugging purposes.
    """
    world = read_file(shapefile_path)
    return world["NAME"].sort_values().unique().tolist()


if __name__ == "__main__":
    print(_list_available_countries())
