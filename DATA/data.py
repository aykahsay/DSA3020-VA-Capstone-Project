"""
Module for handling crop data retrieval and storage for Crop Yield Prediction.
Uses FAOSTAT CSV downloads and SQLite for persistence.
"""

import sqlite3
import pandas as pd
from config import settings
import os

class FAOSTATHandler:
    """
    Handles loading crop data from FAOSTAT CSV files.
    """

    def __init__(self, raw_data_dir=settings.RAW_DATA_DIR):
        self.raw_data_dir = raw_data_dir
        os.makedirs(self.raw_data_dir, exist_ok=True)

    def load_crop_csv(self, crop_file, element="Yield"):
        """
        Load FAOSTAT CSV data for a crop.

        Parameters
        ----------
        crop_file : str
            Name of the CSV file in raw_data_dir (e.g., 'Maize.csv')
        element : str
            Column to extract (e.g., 'Yield', 'Production')

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by year with column `element.lower()`.
        """
        path = os.path.join(self.raw_data_dir, crop_file)
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found. Download CSV first.")

        df = pd.read_csv(path)
        # Keep only essential columns
        if not all(col in df.columns for col in ["Year", element]):
            raise KeyError(f"CSV missing required columns: 'Year' or '{element}'")
        df = df[["Year", element]].copy()
        df.rename(columns={element: element.lower(), "Year": "year"}, inplace=True)
        df.set_index("year", inplace=True)
        df[element.lower()] = pd.to_numeric(df[element.lower()], errors="coerce")
        return df


class SQLRepository:
    """
    Handles SQLite database operations for crop data.
    """

    def __init__(self, db_path=settings.DB_PATH):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)

    def create_table(self, table_name, columns):
        """
        Create table if it doesn't exist.

        Parameters
        ----------
        table_name : str
            Name of the table.
        columns : dict
            Dictionary of {column_name: sqlite_type} e.g., {"year": "INTEGER", "yield": "REAL"}
        """
        col_defs = ", ".join([f"{k} {v}" for k, v in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})"
        self.connection.execute(sql)
        self.connection.commit()

    def insert_table(self, table_name, records: pd.DataFrame, if_exists="fail"):
        """
        Insert a DataFrame into SQLite table.
        """
        n_inserted = records.to_sql(
            name=table_name,
            con=self.connection,
            if_exists=if_exists
        )
        return {"transaction_successful": True, "records_inserted": n_inserted}

    def read_table(self, table_name, limit=None):
        """
        Read data from a SQLite table.

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by year.
        """
        sql = f"SELECT * FROM '{table_name}'"
        if limit:
            sql += f" LIMIT {limit}"

        df = pd.read_sql(sql, con=self.connection, index_col="year")
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    def close(self):
        self.connection.close()
