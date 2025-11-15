"""
This module contains all code used to interact with the FAOSTAT API
and the SQLite database for the Crop Yield Prediction Project.
API configuration (like BASE_URL and country/crop settings) is
stored in your `.env` file and loaded through the `config` module.
"""

import sqlite3
import pandas as pd
import requests
from config import settings


class FAOSTATAPI:
    """
    A class to interact with the FAOSTAT API for retrieving agricultural data.
    """

    def __init__(self, base_url=settings.faostat_base_url):
        self.__base_url = base_url

    def get_crop_data(self, crop, country, element="Yield", year_start=2000, year_end=2023):
        """
        Retrieve crop data (yield/production/area harvested) from FAOSTAT API.

        Parameters
        ----------
        crop : str
            Name of the crop (e.g., 'Maize', 'Wheat').
        country : str
            Country name (e.g., 'Kenya').
        element : str, optional
            FAOSTAT element to retrieve ('Yield', 'Production', etc.).
        year_start : int
            Starting year.
        year_end : int
            Ending year.

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by year, containing crop metrics.
        """

        endpoint = f"{self.__base_url}/QA/Crops"
        params = {
            "item": crop,
            "element": element,
            "area": country,
            "year": f"{year_start},{year_end}"
        }

        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            raise ConnectionError(
                f"FAOSTAT API request failed with status {response.status_code}"
            )

        data_json = response.json()

        if "data" not in data_json or len(data_json["data"]) == 0:
            raise ValueError(f"No FAOSTAT data found for {crop}, {country}, {element}")

        df = pd.DataFrame(data_json["data"])

        # Ensure essential columns exist
        expected_cols = ["year", "value"]
        for col in expected_cols:
            if col not in df.columns:
                raise KeyError(f"Missing expected column '{col}' in FAOSTAT response")

        # Clean DataFrame
        df = df[["year", "value"]]
        df.rename(columns={"value": element.lower()}, inplace=True)

        df["year"] = pd.to_numeric(df["year"])
        df.set_index("year", inplace=True)

        return df


class SQLRepository:
    """
    A wrapper class to interact with SQLite database for storing and retrieving crop data.
    """

    def __init__(self, connection):
        self.connection = connection

    def insert_table(self, table_name, records: pd.DataFrame, if_exists="fail"):
        """
        Insert a DataFrame into SQLite table.
        """

        n_inserted = records.to_sql(
            name=table_name,
            con=self.connection,
            if_exists=if_exists
        )

        return {
            "transaction_successful": True,
            "records_inserted": n_inserted
        }

    def read_table(self, table_name, limit=None):
        """
        Read data from a SQLite table.

        Parameters
        ----------
        table_name : str
            Name of the table.
        limit : int or None
            Number of most recent records to retrieve.

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by year with numeric columns.
        """

        sql = f"SELECT * FROM '{table_name}'"
        if limit:
            sql += f" LIMIT {limit}"

        df = pd.read_sql(
            sql=sql,
            con=self.connection,
            index_col="year"
        )

        # Convert all numeric columns
        df = df.apply(pd.to_numeric, errors="coerce")

        return df
