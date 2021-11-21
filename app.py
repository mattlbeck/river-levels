"""Entry point for the streamlit data visualisation app"""
import os
import streamlit as st

from src.streamlit.multipage import MultiPage
from src.streamlit.pages import stations

app = MultiPage()

# Main page
stations.app()

# Add pages
for page in (stations,):
    app.add_page(page.PAGE_NAME, page.app)

app.run()
