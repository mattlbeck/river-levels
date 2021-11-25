# Explore EA station data
import json
from pandas.core.arrays.base import ExtensionArray
import streamlit as st
import pandas as pd
import pydeck as pdk

import src.dataio as dataio

PAGE_NAME = "Measurement Stations"

MARKER_COLOUR = "#5fb6e2"


def hex_to_rgb(hex):
    """
    Convert hex to rgb.
    """
    hex = hex.lstrip("#")
    hlen = len(hex)
    return [int(hex[i : i + hlen // 3], 16) for i in range(0, hlen, hlen // 3)]


def app():
    # Process mappable stations. Drop stations lacking coords and fill in NAs in there info
    mappable_stations = dataio.get_stations(mappable_only=True)
    measures = dataio.get_measures()
    measure = st.selectbox("Stations with measure", measures.parameterName.unique())
    mappable_stations = pd.merge(
        mappable_stations,
        measures[measures.parameterName == measure][["stationReference"]],
        on="stationReference",
        how="inner",
    )

    st.header(PAGE_NAME)

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/basic-v9",
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    mappable_stations[
                        ["lat", "long", "label", "riverName", "town", "catchmentName"]
                    ],
                    get_position=["long", "lat"],
                    auto_highlight=True,
                    pickable=True,
                    elevation_scale=50,
                    elevation_range=[0, 1000],
                    get_radius=1000,
                    get_fill_color=hex_to_rgb(MARKER_COLOUR) + [255 * 0.5],
                    coverage=1,
                )
            ],
            initial_view_state=pdk.ViewState(
                longitude=-1.415,
                latitude=52.2323,
                zoom=6,
                min_zoom=5,
                max_zoom=15,
            ),
            tooltip={
                "html": "<b>{label}</b> <br> {catchmentName} <br> {riverName} - {town}"
            },
        )
    )

    st.dataframe(mappable_stations)
