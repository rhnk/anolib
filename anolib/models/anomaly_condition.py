import polars as pl
import yaml
from pydantic import BaseModel

from anolib.constants import AnomalyConditionType, Operators


class AnomalyCondition(BaseModel):
    type: AnomalyConditionType
    value: str | int | float
    condition: Operators

    @classmethod
    def from_yaml(self, yaml_str):
        return self(**yaml.safe_load(yaml_str))

    def get_anomalies(self, records, record_set):
        if self.type == AnomalyConditionType.PCT_DELTA:
            records = records.with_columns(
                (
                    (
                        pl.col(record_set.metric_column)
                        / pl.col(record_set.metric_column).shift(1)
                        - 1
                    )
                    * 100
                ).alias("pct_delta")
            )
            return records.sql(
                f"""select * from self where pct_delta {self.condition.value} {self.value}"""
            )
