"""This module provides functions for visualizing geographical and temporal data.
It includes capabilities for plotting:

1. **Geographical Maps**:
   - `plot_country_values`: Generates a world map with color-coded values for specific countries.
     It uses Cartopy for geographical plotting and supports logarithmic scaling of values.

2. **Time Series Plots**:
   - `plot_top_cities_over_time`: Creates line plots showing the top N cities with the most days lived
     over time. It includes options to display cumulative values and to exclude the most important city.
"""

import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from pathlib import Path
from math import log
import pandas as pd
import warnings

_SHAPEFILE_PATH: Path = (
    Path("data") / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"
)


def plot_country_values(
    countries: list[str],
    values: list[int],
    shapefile_path: Path = _SHAPEFILE_PATH,
) -> None:
    """Plot a world map with values associated with specific countries using Cartopy."""
    if len(countries) != len(values):
        raise ValueError("Length of 'countries' and 'values' lists must be the same.")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)

        ax: GeoAxes = plt.axes(projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle="-", linewidth=0.5)

        # Read the shapefile
        shp = Reader(shapefile_path)
        countries_feature = ShapelyFeature(shp.geometries(), ccrs.PlateCarree())

        ax.add_feature(
            countries_feature, facecolor="none", edgecolor="gray", linewidth=0.1
        )

        # Assign a value to each country
        norm_values = [log(value) + 1 if value > 0 else 0 for value in values]
        max_val = max(norm_values)

        cmap = plt.cm.get_cmap("PuBu")

        for country, norm_value in zip(countries, norm_values):
            for geom in shp.records():
                if geom.attributes["NAME"] == country:
                    ax.add_geometries(
                        [geom.geometry],
                        ccrs.PlateCarree(),
                        facecolor=cmap(norm_value / max_val),
                        edgecolor="black",
                        linewidth=0.2,
                    )

        plt.title("World Map with Values Per Country")
        plt.show()


def plot_top_cities_over_time(
    df: pd.DataFrame,
    top_n: int = 10,
    cumulative: bool = False,
    exclude_top: int = 0,
    log_scale: bool = True,
) -> None:
    """Plots the top N cities with the most days lived over time, with the ability to exclude the top X cities."""
    city_year_data = (
        df.groupby(["city", "year"])["days_lived"].sum().unstack().fillna(0)
    )

    top_cities = city_year_data.sum(axis=1).nlargest(top_n + exclude_top).index
    top_cities = top_cities[exclude_top:]
    city_year_data = city_year_data.loc[top_cities]

    if cumulative:
        city_year_data = city_year_data.cumsum(axis=1)

    ax = city_year_data.T.plot(kind="line", figsize=(15, 10), marker="o")

    if log_scale:
        ax.set_yscale("log")

    title = f"Top {top_n} Cities with Most Days Lived Over Time"

    if cumulative:
        title += " (Cumulative)"

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Days Lived")
    plt.legend(title="City")
    plt.grid(True)
    plt.show()


def plot_city_distribution(df: pd.DataFrame, log_scale: bool = True) -> None:
    """Plot the distribution of days lived across different cities."""
    city_days = df.groupby("city")["days_lived"].sum().sort_values(ascending=False)
    ax = city_days.plot(kind="bar", figsize=(15, 10), color="skyblue")
    if log_scale:
        ax.set_yscale("log")
    plt.title("Distribution of Days Lived Across Different Cities")
    plt.xlabel("City")
    plt.ylabel("Total Days Lived")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.grid(True)
    plt.show()


def plot_country_distribution(df: pd.DataFrame, log_scale: bool = True) -> None:
    """Plot the distribution of days lived across different countries."""
    country_days = (
        df.groupby("country")["days_lived"].sum().sort_values(ascending=False)
    )
    ax = country_days.plot(kind="bar", figsize=(15, 10), color="salmon")
    if log_scale:
        ax.set_yscale("log")
    plt.title("Distribution of Days Lived Across Different Countries")
    plt.xlabel("Country")
    plt.ylabel("Total Days Lived")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Example usage of the functions for testing
    print("This is a module for plotting geographical and temporal data.")
