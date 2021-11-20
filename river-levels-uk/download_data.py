import requests
from pathlib import Path

RIVER_LEVELS_DOMAIN = "https://riverlevels.uk/"

def download_data(url, path):
    """Downloads data from a url to a path"""
    print(f"Downloading {url} to {path}")
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

def get_data_for_location(location):
    """Downloads data for a location"""
    url = RIVER_LEVELS_DOMAIN + f"{location}/data/csv"
    path = Path("data")
    path.mkdir(parents=True, exist_ok=True)
    download_data(url, path / f"{location}.csv")

def parse_args():
    """Parses command line arguments"""
    import argparse
    parser = argparse.ArgumentParser(description="Downloads river level data")
    parser.add_argument("location", help="Location to download data for")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    get_data_for_location(args.location)