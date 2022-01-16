import json
from pathlib import Path
import yaml
import pandas as pd


class DvcWorkspace:
    """
    Store and retrieve data and config from standard places
    in a DVC workspace.
    """

    data_dir = Path("data")
    params_file = "params.yaml"

    def __init__(self, root_param=None):
        self.data_dir.mkdir(exist_ok=True)
        self.params = yaml.safe_load(open(self.params_file))
        if root_param:
            self.params = self.params[root_param]

    def load_json(self, filename, asTable=False):
        data = json.load(open(self.data_dir / filename))
        if asTable:
            data = pd.DataFrame(data)
        return data

    def save_json(self, filename, data):
        with open(self.data_dir / filename, "w") as f:
            json.dump(data, f)
