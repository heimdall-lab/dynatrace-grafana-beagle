from datetime import datetime


class DatetimeUtils:

    @staticmethod
    def convert_to_timestamp(target: datetime):
        return int(target.timestamp() * 1000)

    @staticmethod
    def convert_from_timestamp(target: int):
        return datetime.fromtimestamp(target / 1000)