import yaml
from pydantic import BaseModel


class ColumnCondition(BaseModel):
    column: str
    condition: str
    value: str

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))
