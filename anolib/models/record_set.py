import yaml
from pydantic import BaseModel, model_validator
from typing_extensions import Self

from anolib.constants import RecordSetType
from anolib.models.column_condition import ColumnCondition


class RecordSet(BaseModel):
    input_source: str
    timeseries_column: str
    metric_column: str
    type: RecordSetType
    records_selector: str | list[str]
    filters: list[ColumnCondition] | None = None

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))

    @model_validator(mode="after")
    def check_record_selector_for_type_sql(self) -> Self:
        if self.type == "sql" and not (isinstance(self.records_selector, str)):
            raise ValueError(
                "records_selector should be a SQL of type string when type is 'sql'"
            )
        return self
