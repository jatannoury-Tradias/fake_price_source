import datetime


def z_string2datetime_obj(z_time_string: str) -> datetime.datetime:
    return datetime.datetime.strptime(z_time_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def datetime_obj2z_string(datetime_obj: datetime.datetime) -> str:
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
