import polars as pl
import yaml
from pydantic import BaseModel

from anolib.constants import AnomalyConditionType, Operators
from anolib.models.record_set import RecordSet


class AnomalyCondition(BaseModel):
    type: AnomalyConditionType
    value: str | int | float
    condition: Operators

    @classmethod
    def from_yaml(self, yaml_str: str):
        return self(**yaml.safe_load(yaml_str))

    def get_anomalies(self, records: pl.DataFrame, record_set: RecordSet):
        records = records.sort(record_set.timeseries_column)
        if self.type == AnomalyConditionType.PCT_DELTA:
            records = records.with_columns(
                (
                    (
                        pl.col(record_set.metric_column)
                        / pl.col(record_set.metric_column).shift(1)
                        - 1
                    )
                    * 100
                ).alias(AnomalyConditionType.PCT_DELTA.value)
            )
            return records.sql(
                f"""select * from self where {AnomalyConditionType.PCT_DELTA.value} {self.condition.value} {self.value}"""
            )
