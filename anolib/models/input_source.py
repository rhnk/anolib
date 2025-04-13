import yaml
from pydantic import BaseModel

from anolib.constants import InputSourceType


class InputSource(BaseModel):
    type: InputSourceType
    excel_path: str | None = None
    excel_sheet: str | None = None
    csv_path: str | None = None

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))
