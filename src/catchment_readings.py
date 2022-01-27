from .util import DvcWorkspace
from .ea_flood_monitoring import EaData

import pandas as pd


def main():
    ws = DvcWorkspace(root_param="readings")
    stations = ws.load_json("stations.json", asTable=True)
    station_measures = ws.load_json("station_measures.json", asTable=True)
    try:
        catchment_readings = pd.read_parquet(ws.data_dir / "catchment_readings.parquet")
        latest_reading = catchment_readings.dateTime.max()
    except FileNotFoundError:
        catchment_readings = pd.DataFrame()
        latest_reading = None

    catchments = ws.params["catchments"]
    # for now stick to caching data for just one qualifier
    # note, if this is changed, the cache should be invalidated
    qualifier = ws.params["qualifier"]

    stations = stations[stations.catchmentName.isin(catchments)][
        ["stationReference", "riverName", "catchmentName"]
    ]
    measures = pd.merge(
        stations,
        station_measures[station_measures.qualifier == qualifier],
        on="stationReference",
    )

    ea = EaData()
    print(f"Download readings since {latest_reading}")
    num_readings = len(catchment_readings)
    print(f"num readings cached {num_readings}")
    for id, measure in measures.iterrows():
        readings = pd.DataFrame(ea.get_readings(measure.id, latest_reading))

        # API has a bug where it ignores the time part of the date, so we filter
        # these readings ourselves
        if latest_reading is not None:
            readings = readings[pd.to_datetime(readings["dateTime"]) > latest_reading]

        print(f"Got {len(readings)} readings for {measure.riverName}")
        readings = readings.assign(
            measure=measure.id, river=measure.riverName, catchment=measure.catchmentName
        )
        catchment_readings = catchment_readings.append(readings)

    print(f"num readings cached after {len(catchment_readings)}")
    if len(catchment_readings) == num_readings:
        print("No new readings")

    catchment_readings.dateTime = pd.to_datetime(catchment_readings.dateTime, utc=True)
    catchment_readings.to_parquet(ws.data_dir / "catchment_readings.parquet")
