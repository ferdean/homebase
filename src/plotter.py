"""This module provides functions for visualizing geographical and temporal data.
It includes capabilities for plotting:

1. **Geographical Maps**: Generates a world map with color-coded values for specific countries.
     It uses Cartopy for geographical plotting and supports logarithmic scaling of values.

2. **Time Series Plots**: Creates line plots showing the top N cities with the most days lived
     over time. It includes options to display cumulative values and to exclude the most important city.
"""

import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from pathlib import Path
import warnings
import pandas as pd
from math import log

# Default shapefile path
_SHAPEFILE_PATH = (
    Path("data") / "ne_110m_admin_0_countries" / "ne_110m_admin_0_countries.shp"
)


def plot_country_values(
    countries: list[str],
    values: list[int | float],
    shapefile_path: Path = _SHAPEFILE_PATH,
    title: str | None = "world map with days stayed per country",
    cmap_name: str = "PuBu",
    projection: ccrs.Projection = ccrs.PlateCarree(),
    log_scale: bool = True,
    show: bool = True,
) -> None:
    """Plot a world map with values associated with specific countries."""
    if len(countries) != len(values):
        raise ValueError("Length of 'countries' and 'values' lists must be the same.")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)

        ax: GeoAxes = plt.axes(projection=projection)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle="-", linewidth=0.5)

        countries_feature = ShapelyFeature(
            Reader(shapefile_path).geometries(), projection
        )
        ax.add_feature(
            countries_feature, facecolor="none", edgecolor="gray", linewidth=0.1
        )

        cmap = plt.cm.get_cmap(cmap_name)
        max_val = (
            max(log(value) + 1 if value > 0 else 0 for value in values)
            if log_scale
            else max(values)
        )

        for country, value in zip(countries, values):
            norm_value = log(value) + 1 if value > 0 and log_scale else value
            for geom in Reader(shapefile_path).records():
                if geom.attributes["NAME"] == country:
                    ax.add_geometries(
                        [geom.geometry],
                        projection,
                        facecolor=cmap(norm_value / max_val),
                        edgecolor="black",
                        linewidth=0.2,
                    )

        plt.title(title)
        if show:
            plt.show()


def plot_top_cities_over_time(
    df: pd.DataFrame,
    top_n: int = 10,
    cumulative: bool = False,
    exclude_top: int = 0,
    log_scale: bool = False,
    title: str | None = None,
    xlabel: str = "year",
    ylabel: str = "days lived",
    figsize: tuple = (15, 10),
    show: bool = True,
) -> None:
    """Plot the top N cities with the most days lived over time."""
    city_year_data = (
        df.groupby(["city", "year"])["days_lived"].sum().unstack().fillna(0)
    )
    top_cities = (
        city_year_data.sum(axis=1).nlargest(top_n + exclude_top).index[exclude_top:]
    )
    city_year_data = (
        city_year_data.loc[top_cities].cumsum(axis=1)
        if cumulative
        else city_year_data.loc[top_cities]
    )

    ax = city_year_data.T.plot(kind="line", figsize=figsize, marker="o")
    ax.set_yscale("log" if log_scale else "linear")

    plot_title = title or f"top {top_n} cities with most days lived"
    if cumulative:
        plot_title += " (cumulative)"

    plt.title(plot_title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title="city")
    plt.grid(True)
    if show:
        plt.show()


def plot_visited_countries_map(
    countries: list[str],
    shapefile_path: Path = _SHAPEFILE_PATH,
    title: str | None = None,
    cmap_name: str = "GnBu",
    projection: ccrs.Projection = ccrs.PlateCarree(),
    show: bool = True,
) -> None:
    """Plot a world map highlighting the countries visited."""
    unique_countries = set(countries)
    num_countries_visited = len(unique_countries)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)

        ax: GeoAxes = plt.axes(projection=projection)
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle="-", linewidth=0.5)

        countries_feature = ShapelyFeature(
            Reader(shapefile_path).geometries(), projection
        )
        ax.add_feature(
            countries_feature, facecolor="none", edgecolor="gray", linewidth=0.1
        )

        cmap = plt.cm.get_cmap(cmap_name)
        for geom in Reader(shapefile_path).records():
            if geom.attributes["NAME"] in unique_countries:
                ax.add_geometries(
                    [geom.geometry],
                    projection,
                    facecolor=cmap(0.6),  # Fixed color value for all visited countries
                    edgecolor="black",
                    linewidth=0.2,
                )

        plot_title = title or f"Countries Visited: {num_countries_visited}"
        plt.title(plot_title)
        if show:
            plt.show()


def plot_city_distribution(
    df: pd.DataFrame,
    log_scale: bool = True,
    title: str | None = "distribution of days lived",
    xlabel: str = "city",
    ylabel: str = "total days lived",
    color: str = "skyblue",
    figsize: tuple = (15, 10),
    rotation: int = 45,
    show: bool = True,
) -> None:
    """Plot the distribution of days lived across different cities."""
    city_days = df.groupby("city")["days_lived"].sum().sort_values(ascending=False)
    ax = city_days.plot(kind="bar", figsize=figsize, color=color)
    ax.set_yscale("log" if log_scale else "linear")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()
    plt.grid(True)
    if show:
        plt.show()


def plot_country_distribution(
    df: pd.DataFrame,
    log_scale: bool = True,
    title: str | None = "distribution of days lived",
    xlabel: str = "country",
    ylabel: str = "total days lived",
    color: str = "salmon",
    figsize: tuple = (15, 10),
    rotation: int = 45,
    show: bool = True,
) -> None:
    """Plot the distribution of days lived across different countries."""
    country_days = (
        df.groupby("country")["days_lived"].sum().sort_values(ascending=False)
    )
    ax = country_days.plot(kind="bar", figsize=figsize, color=color)
    ax.set_yscale("log" if log_scale else "linear")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right")
    plt.tight_layout()
    plt.grid(True)
    if show:
        plt.show()
