from pydantic import BaseModel

from anolib.constants import AlertChannelType
from anolib.utils.logger import info


class AlertChannel(BaseModel):
    type: AlertChannelType | None = AlertChannelType.STDOUT

    def publish(self, records):
        if self.type == AlertChannelType.STDOUT:
            info(records) if len(records) > 0 else info("No anomalies")
