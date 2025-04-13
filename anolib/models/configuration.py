from pydantic import BaseModel
from yaml import safe_load

from anolib.models.alert_channel import AlertChannel
from anolib.models.experiment import Experiment
from anolib.models.input_source import InputSource
from anolib.models.record_set import RecordSet


class Configuration(BaseModel):
    record_sets: dict[str, RecordSet]
    experiments: dict[str, Experiment]
    input_sources: dict[str, InputSource]
    alert_channels: dict[str, AlertChannel] | None = {}

    def run_experiments(self):
        # Run experiments
        for name, experiment in self.experiments.items():
            print(f"[INFO] Processing experiment `{name}`")
            experiment.run(self.record_sets, self.input_sources, self.alert_channels)

    @classmethod
    def init_from_yaml(self, config_path):
        config_reader = open(config_path, "r")
        # TODO: validate yaml
        config_dict = safe_load(config_reader)
        return self(**config_dict)
