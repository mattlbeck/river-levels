# Visualise historical river levels

import streamlit as st
from datetime import date
from src.ea_flood_monitoring import EaData
import src.dataio as dataio
import pandas as pd
import altair as alt

PAGE_NAME = "River Levels"


def app():

    st.header(PAGE_NAME)
    stations = dataio.get_stations(mappable_only=True)
    selected_station = st.selectbox("Select a station", stations.label.tolist())
    station_ref = stations.loc[
        stations.label == selected_station
    ].stationReference.values[0]

    measures = dataio.get_measures()
    station_measures = measures[measures.stationReference == station_ref]
    selected_measure = st.selectbox("Select a measure", station_measures.id)

    efm = EaData()
    data = efm.get_readings(selected_measure, since_date=date(2021, 12, 23))
    data = pd.DataFrame(data)
    data["dateTime"] = pd.to_datetime(data["dateTime"])
    st.altair_chart(
        alt.Chart(data).mark_line(interpolate="basis").encode(x="dateTime", y="value")
    )
