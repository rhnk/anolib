import polars as pl
import yaml
from pydantic import BaseModel, model_validator
from typing_extensions import Self

from anolib.constants import RecordSetType
from anolib.models.alert_channel import AlertChannel
from anolib.models.anomaly_condition import AnomalyCondition
from anolib.models.input_source import InputSource
from anolib.models.record_set import RecordSet
from anolib.utils.data_loaders import load_dataframe
from anolib.utils.logger import error


class Experiment(BaseModel):
    record_set: str
    type: str
    alert_condition: (
        list[dict[str, list[AnomalyCondition]]] | list[AnomalyCondition] | None
    ) = None
    algorithm: str | None = None
    alert_channel: str | None = "STDOUT"

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))

    @model_validator(mode="after")
    def check_valid_setup_type_anomaly(self) -> Self:
        if self.type == "anomaly" and self.algorithm is None:
            raise ValueError("Experiment.algorithm is required for type=anomaly")
        return self

    @model_validator(mode="after")
    def check_valid_setup_type_condition(self) -> Self:
        if self.type == "conditional" and self.alert_condition is None:
            raise ValueError(
                "Experiment.alert_condition is required for type=conditional"
            )
        return self

    def run(
        self,
        record_sets: dict[str, RecordSet],
        input_sources: dict[str, InputSource],
        alert_channels: dict[str, AlertChannel],
    ):
        record_set = record_sets.get(self.record_set)
        # load data from input source into an variable
        if globals().get(f"_{record_set.input_source}") is None:
            globals()[f"_{record_set.input_source}"] = load_dataframe(
                input_sources.get(record_set.input_source)
            )

        records = pl.DataFrame()
        # apply record set selector
        if record_set.type == RecordSetType.SQL:
            records: pl.DataFrame = globals()[f"_{record_set.input_source}"].sql(
                record_set.records_selector
            )

        if len(records) == 0:
            error("RecordSet is empty. Ending experiment run.", exc_info=False)
            return

        alert_channel = alert_channels.get(self.alert_channel, AlertChannel())

        for alert in self.alert_condition:
            if isinstance(alert, AnomalyCondition):
                anomaly_records = alert.get_anomalies(records, record_set)
                # Send anomaly records out
                alert_channel.publish(anomaly_records)

            elif isinstance(alert, dict):
                # complex clause
                pass
