# Download and save the full list of monitoring stations
from . import ea_flood_monitoring as efm
import json
from pathlib import Path

STATION_FIELDS = [
    "id",
    "name",
    "lat",
    "long",
    "catchmentName",
    "label",
    "riverName",
    "stationReference",
    "town",
]


def process_station_entry(station):
    return {k: v for k, v in station.items() if k in STATION_FIELDS}


def main():
    datadir = Path("data")
    datadir.mkdir(exist_ok=True)

    data = efm.get_measurement_stations()
    processed = [process_station_entry(s) for s in data["items"]]
    json.dump(processed, open(datadir / "stations.json", "w"))
