import yaml
from pydantic import BaseModel

from anolib.models.anomaly_condition import AnomalyCondition


class ConditionBlock(BaseModel):
    """Block containing multiple anomaly conditions."""
    conditions: list[AnomalyCondition]

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))
