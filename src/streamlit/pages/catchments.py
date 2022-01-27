# Visualise measurements for whole catchments

from functools import cache
import streamlit as st
from datetime import date
from src.ea_flood_monitoring import EaData
import src.dataio as dataio
import pandas as pd
import altair as alt
import yaml

PAGE_NAME = "Catchments"


def app():

    st.header(PAGE_NAME)

    selected_qualifier = yaml.safe_load(open("params.yaml"))["readings"]["qualifier"]

    cache_only = st.checkbox("Cache only", value=True)

    if cache_only:
        readings = get_cached_readings()
    else:
        readings = download_readings(selected_qualifier)

    st.altair_chart(
        alt.Chart(readings)
        .properties(width=1000, height=400)
        .mark_line(interpolate="basis")
        .encode(x="dateTime", y="value", color="river:N", tooltip=["river", "value"])
    )


def get_cached_readings():

    all_readings = pd.read_parquet("data/catchment_readings.parquet")
    catchment_names = all_readings.catchment.unique()
    selected_catchment = st.selectbox("Select a station", catchment_names)
    st.write(all_readings)
    return all_readings[all_readings.catchment == selected_catchment]


def download_readings(selected_qualifier):
    stations = dataio.get_stations(mappable_only=True)
    catchment_names = stations.catchmentName.unique()
    selected_catchment = st.selectbox("Select a station", catchment_names)
    measures = dataio.get_measures()
    station_measures = measures[
        measures.stationReference.isin(
            stations[stations.catchmentName == selected_catchment].stationReference
        )
    ]

    station_measures = station_measures[
        station_measures.qualifier == selected_qualifier
    ]

    station_measures = pd.merge(
        station_measures,
        stations[["stationReference", "label"]],
        on="stationReference",
        how="left",
    )
    readings = []
    for measure_id in station_measures.id:
        efm = EaData()
        measure_data = efm.get_readings(measure_id, since_date=date(2021, 12, 23))
        measure_data = pd.DataFrame(measure_data)
        readings.append(measure_data)

    readings = pd.concat(readings, keys=station_measures.label)
    readings = readings.reset_index(0)
    readings["dateTime"] = pd.to_datetime(readings["dateTime"])
    return readings
