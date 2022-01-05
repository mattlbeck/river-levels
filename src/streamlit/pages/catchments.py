# Visualise measurements for whole catchments

import streamlit as st
from datetime import date
from src.ea_flood_monitoring import EaData
import src.dataio as dataio
import pandas as pd
import altair as alt

PAGE_NAME = "Catchments"


def app():

    st.header(PAGE_NAME)
    stations = dataio.get_stations(mappable_only=True)
    selected_catchment = st.selectbox(
        "Select a station", stations.catchmentName.unique()
    )

    measures = dataio.get_measures()
    station_measures = measures[
        measures.stationReference.isin(
            stations[stations.catchmentName == selected_catchment].stationReference
        )
    ]

    selected_qualifier = st.selectbox(
        "Select a qualifier", station_measures.qualifier.unique()
    )
    station_measures = station_measures[
        station_measures.qualifier == selected_qualifier
    ]

    station_measures = pd.merge(
        station_measures,
        stations[["stationReference", "label"]],
        on="stationReference",
        how="left",
    )
    all_data = []
    for measure_id in station_measures.id:
        efm = EaData()
        measure_data = efm.get_readings(measure_id, since_date=date(2021, 12, 23))
        measure_data = pd.DataFrame(measure_data)
        all_data.append(measure_data)

    all_data = pd.concat(all_data, keys=station_measures.label)
    all_data = all_data.reset_index(0)
    all_data["dateTime"] = pd.to_datetime(all_data["dateTime"])
    st.altair_chart(
        alt.Chart(all_data)
        .properties(width=1000, height=400)
        .mark_line(interpolate="basis")
        .encode(x="dateTime", y="value", color="label:N", tooltip=["label", "value"])
    )
