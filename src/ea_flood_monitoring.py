# Interact with the environment agency flood monitoring data API
from datetime import date
from json.decoder import JSONDecodeError
import requests

API_ROOT = "https://environment.data.gov.uk/flood-monitoring/id"


class EaData:
    def request(self, uri):
        response = requests.get(f"{API_ROOT}/{uri}")
        try:
            return response.json()
        except JSONDecodeError:
            print(f"{API_ROOT}/{uri}")
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

    def get_readings(self, measure_id, since_date: date):
        """
        Downloads the readings for a given station and measure.
        :param measure_id: The ID of the measure
        :param since_date: The ealiest date to query readings for
        """
        since_date_str = since_date.strftime("%Y-%m-%d")
        resp = self.request(f"measures/{measure_id}/readings?since={since_date_str}")

        # extract just the date and value from the response
        values = [{k: r[k] for k in ["dateTime", "value"]} for r in resp["items"]]
        return values
