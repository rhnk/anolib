import polars as pl

from anolib.constants import InputSourceType
from anolib.models.input_source import InputSource


def load_dataframe(input_source: InputSource):
    if input_source.type == InputSourceType.EXCEL:
        if input_source.excel_sheet is None:
            return pl.read_excel(input_source.excel_path)
        else:
            return pl.read_excel(
                input_source.excel_path, sheet_name=input_source.excel_sheet
            )
    elif input_source.type == InputSourceType.CSV:
        return pl.read_csv(input_source.csv_path)
