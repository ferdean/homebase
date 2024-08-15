import pandas as pd
from pathlib import Path
import logging
import difflib

logger = logging.getLogger(__name__)


class _Database:
    """Wrapper for managing data stored in CSV files as Pandas DataFrames."""

    def __init__(self, file_paths: list[Path] | Path) -> None:
        """Initialize the database by loading data from one or more CSV files."""
        if isinstance(file_paths, Path):
            file_paths = [file_paths]
        self.dataframes = {file.stem: self._load_data(file) for file in file_paths}
        self._post_init()

    def _post_init(self) -> None:
        """Complete dataframe initialization by calculating additional fields."""
        for df in self.dataframes.values():
            df["days_lived"] = (df["end_date"] - df["start_date"]).dt.days
            df["year"] = df["start_date"].dt.year

    def _load_data(self, file_path: Path) -> pd.DataFrame | None:
        """Load data from a CSV file into a Pandas DataFrame."""
        if not file_path.suffix.lower() == ".csv":
            logger.warning(f"The file {file_path} is not a CSV.")
            return None

        return pd.read_csv(
            file_path, parse_dates=["start_date", "end_date"], dayfirst=True
        )


class ExtendedDatabase(_Database):
    """Extended functionality for managing and analyzing location-based data."""

    def get_basic_stats(self, key: str | None = None) -> dict:
        """Generate basic statistics from the data."""
        df = self._get_dataframe(key)
        return {
            "total_days_lived": df["days_lived"].sum() if not df.empty else 0,
            "average_days_per_location": df["days_lived"].mean() if not df.empty else 0,
            "number_of_locations": df["city"].nunique(),
            "years_covered": df["year"].nunique(),
        }

    def get_location_summary(self, city: str, exact_match: bool = True) -> dict:
        """Get a summary of stays in a particular city."""
        df = self._filter_by_location(city, exact_match)
        return {
            "city": city,
            "total_days_lived": df["days_lived"].sum() if not df.empty else 0,
            "first_stay": (
                pd.to_datetime(df["start_date"]).dt.date.min() if not df.empty else None
            ),
            "last_stay": (
                pd.to_datetime(df["end_date"]).dt.date.max() if not df.empty else None
            ),
            "number_of_stays": df.shape[0],
        }

    def get_country_summary(self, country: str, exact_match: bool = True) -> dict:
        """Get a summary of stays in a particular country."""
        df = self._filter_by_country(country, exact_match)
        return {
            "country": country,
            "total_days_lived": df["days_lived"].sum() if not df.empty else 0,
            "cities": df["city"].unique().tolist(),
            "number_of_cities": df["city"].nunique(),
            "first_stay": (
                pd.to_datetime(df["start_date"]).dt.date.min() if not df.empty else None
            ),
            "last_stay": (
                pd.to_datetime(df["end_date"]).dt.date.max() if not df.empty else None
            ),
            "number_of_stays": df.shape[0],
        }

    def get_year_summary(self, year: int) -> dict:
        """Get a summary of stays in a particular year."""
        df = self._filter_by_year(year)
        return {
            "year": year,
            "number_of_countries": df["country"].nunique(),
            "number_of_locations": df["city"].nunique(),
            "number_of_stays": df.shape[0],
        }

    def get_countries_days_lived(self) -> pd.DataFrame:
        """Generate a list of countries and the total days lived in each."""
        df = self._get_dataframe()
        country_days = df.groupby("country")["days_lived"].sum().reset_index()
        country_days.columns = ["country", "total_days_lived"]
        return country_days

    def _filter_by_location(self, city: str, exact_match: bool = True) -> pd.DataFrame:
        """Filter the dataframe by city."""
        df = self._get_dataframe()
        if exact_match:
            return df[df["city"].str.lower() == city.lower()]
        else:
            closest_matches = difflib.get_close_matches(
                city, df["city"].unique(), n=1, cutoff=0.8
            )
            if closest_matches:
                logger.info(f"Using closest match for city: {closest_matches[0]}")
                return df[df["city"].str.lower() == closest_matches[0].lower()]
            else:
                logger.warning(f"No close match found for city: {city}.")
                return pd.DataFrame()

    def _filter_by_country(
        self, country: str, exact_match: bool = True
    ) -> pd.DataFrame:
        """Filter the dataframe by country."""
        df = self._get_dataframe()
        if exact_match:
            return df[df["country"].str.lower() == country.lower()]
        else:
            closest_matches = difflib.get_close_matches(
                country, df["country"].unique(), n=1, cutoff=0.8
            )
            if closest_matches:
                logger.info(f"Using closest match for country: {closest_matches[0]}")
                return df[df["country"].str.lower() == closest_matches[0].lower()]
            else:
                logger.warning(f"No close match found for country: {country}.")
                return pd.DataFrame()

    def _filter_by_year(self, year: int) -> pd.DataFrame:
        """Filter the dataframe by year."""
        df = self._get_dataframe()
        return df[df["year"] == year]

    def _get_dataframe(self, key: str | None = None) -> pd.DataFrame:
        """Retrieve the appropriate dataframe."""
        return (
            self.dataframes[next(iter(self.dataframes))]
            if key is None
            else self.dataframes[key]
        )


if __name__ == "__main__":
    db = ExtendedDatabase(Path("data") / "ferran.csv")
    print(db.get_basic_stats())
    # print(db.get_location_summary("Castello", exact_match=False))
    # print(db.get_year_summary(2023))
    # print(db.get_country_summary("Spain"))
    # print(db.get_countries_days_lived())
