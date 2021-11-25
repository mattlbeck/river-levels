# Interact with the environment agency flood monitoring data API
from json.decoder import JSONDecodeError
import requests

API_ROOT = "https://environment.data.gov.uk/flood-monitoring/id"


class EaData:
    def request(self, uri):
        response = requests.get(f"{API_ROOT}/{uri}")
        try:
            return response.json()
        except JSONDecodeError:
            print(f"Error: {response.text}")
            raise

    def get_measurement_stations(self):
        """Downloads all the measurement stations"""
        return self.request("stations")

    def get_measures(self, station_id):
        """
        Downloads the measures for a given station.
        Measures in this sense are the instruments that provide the
        readings.
        :param station_id: The reference name of the station
        """
        return self.request(f"stations/{station_id}/measures")
