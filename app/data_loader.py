# app/data_loader.py

import pandas as pd

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # Convert dates
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

    # Handle missing values
    df.fillna({
        'children': 0,
        'country': 'Unknown',
        'agent': 0,
        'company': 0
    }, inplace=True)

    # Drop rows with missing reservation date or adr
    df.dropna(subset=['reservation_status_date', 'adr'], inplace=True)

    return df
