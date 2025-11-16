
    def preprocess(self, df):
        """
        Basic preprocessing:
        - Fill missing numeric values with median
        - Fill missing categorical values with 'Unknown'
        - Convert date columns to datetime
        """
        for col in df.select_dtypes(include="number").columns:
            df[col].fillna(df[col].median(), inplace=True)
        
        for col in df.select_dtypes(include="object").columns:
            df[col].fillna("Unknown", inplace=True)
        
        # Convert 'Date' columns if exist
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        return df
