"""
Interface with data tracked data in this repo
"""
import pandas as pd
from pathlib import Path

datadir = Path("./data")


def get_stations(mappable_only=False):
    stations = pd.read_json(
        datadir / "stations.json", orient="records", dtype={"long": float, "lat": float}
    )
    if mappable_only:
        stations = stations.dropna(subset=["lat", "long"])
        stations = stations.fillna(
            {
                "catchmentName": "No catchment",
                "riverName": "No river",
                "town": "No town",
            }
        )
    return stations


def get_measures():
    measures = pd.read_json(datadir / "station_measures.json", orient="records")
    return measures
