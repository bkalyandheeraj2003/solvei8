# data/fetchdata.py

import os
import requests

DATA_URL = "https://solvei8-aiml-assignment.s3.ap-southeast-1.amazonaws.com/hotel_bookings.csv"
SAVE_PATH = "data/hotel_bookings.csv"

def download_data(url=DATA_URL, save_path=SAVE_PATH):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    print(f"Downloading data from {url}...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Data saved to {save_path}")
    else:
        print(f"❌ Failed to download data. Status code: {response.status_code}")

if __name__ == "__main__":
    download_data()
