# Interact with the environmen agency flood monitoring data API
import requests

API_ROOT = "https://environment.data.gov.uk/flood-monitoring/id"


def get_data_for_location(location):
    """Downloads data for a location"""
    url = f"{API_ROOT}/stations/{location}"
    response = requests.get(url)
    return response.json()


def get_data_for_river(river):
    """Downloads data for a river"""
    url = f"{API_ROOT}/stations?river={river}"
    response = requests.get(url)
    return response.json()


def get_measurement_stations():
    """Downloads all the measurement stations"""
    url = f"{API_ROOT}/stations"
    response = requests.get(url)
    return response.json()
