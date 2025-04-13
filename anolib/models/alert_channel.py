from pydantic import BaseModel

from anolib.constants import AlertChannelType


class AlertChannel(BaseModel):
    type: AlertChannelType | None = AlertChannelType.STDOUT

    def publish(self, records):
        if self.type == AlertChannelType.STDOUT:
            print(records) if len(records) > 0 else print("No anomalies")
