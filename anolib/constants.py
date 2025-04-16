from enum import Enum

LOGGER_NAMESPACE = "anolib"
LOGGER_MAX_LEN = 1000


class Operators(Enum):
    greater_than_equals = ">="
    less_than_equals = "<="
    equals = "=="
    not_equal = "!="
    less_than = "<"
    greater_than = ">"


class InputSourceType(Enum):
    CSV = "CSV"
    EXCEL = "EXCEL"
    # REST_API = 'REST_API'
    # DATABASE = 'DATABASE'


class RecordSetType(Enum):
    SQL = "SQL"


class AlertChannelType(Enum):
    STDOUT = "STDOUT"
    WEBHOOK = "WEBHOOK"


class AnomalyConditionType(Enum):
    PCT_DELTA = "PCT_DELTA"
