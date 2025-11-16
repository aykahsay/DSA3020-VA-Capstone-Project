# src/data_collection.py
import pandas as pd
from src.config import settings

class MaizeDataHandler:
    """
    Handles loading, cleaning, and combining maize price datasets (agribora + KAMIS)
    """
    def __init__(self):
        self.agribora_csv = settings.AGRIBORA_CSV
        self.kamis_raw_csv = settings.KAMIS_RAW_CSV
        self.kamis_csv = settings.KAMIS_CSV

    def load_agribora(self):
        """Load agriBORA maize price data"""
        df = pd.read_csv(self.agribora_csv)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def load_kamis_raw(self):
        """Load raw KAMIS maize price data"""
        df = pd.read_csv(self.kamis_raw_csv)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def load_kamis_processed(self):
        """Load processed KAMIS data"""
        df = pd.read_csv(self.kamis_csv)
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def combine_datasets(self, use_processed_kamis=True):
        """Combine agriBORA and KAMIS data"""
        agribora = self.load_agribora()
        kamis = self.load_kamis_processed() if use_processed_kamis else self.load_kamis_raw()
        
        combined = pd.concat([agribora, kamis], ignore_index=True)
        combined.sort_values(by=['County','Date'], inplace=True)
        combined.reset_index(drop=True, inplace=True)
        return combined
