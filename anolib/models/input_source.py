import yaml
from pydantic import BaseModel

from anolib.constants import InputSourceType


class InputSource(BaseModel):
    """
    Configuration for data input sources.
    
    Supports CSV and Excel file formats with configurable paths and options.
    For CSV files, csv_path can be either a local file path or a remote URL.
    """
    type: InputSourceType
    excel_path: str | None = None
    excel_sheet: str | None = None
    csv_path: str | None = None  # Can be local file path or remote URL

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))
