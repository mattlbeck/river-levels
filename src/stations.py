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

MEASURE_FIELDS = ["parameter", "parameterName", "period", "qualifier", "unitName"]


def process_station_entry(station):
    return {k: v for k, v in station.items() if k in STATION_FIELDS}


def process_measure_entry(station_id, measure):
    processed = {"id": measure["@id"].split("/")[-1], "stationReference": station_id}
    processed.update({k: v for k, v in measure.items() if k in MEASURE_FIELDS})
    return processed


def main():
    datadir = Path("data")
    datadir.mkdir(exist_ok=True)

    data = efm.EaData().get_measurement_stations()
    processed = [process_station_entry(s) for s in data["items"]]
    json.dump(processed, open(datadir / "stations.json", "w"))

    measures = []
    for station in data["items"]:
        if "measures" in station:
            measures += [
                process_measure_entry(station["stationReference"], m)
                for m in station["measures"]
            ]
    json.dump(measures, open(datadir / "station_measures.json", "w"))
