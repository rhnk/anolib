import yaml
from pydantic import BaseModel

from anolib.models.anomaly_condition import AlertCondition


class ConditionBlock(BaseModel):
    conditions: list[AlertCondition]

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))
