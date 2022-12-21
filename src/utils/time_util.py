import time
from datetime import datetime


def get_unix_time_stamp_milliseconds(datetime):
    return (time.mktime(datetime.timetuple())) * 1000


def get_time_in_seconds_from_unix_time(unix_time):

    datetime_from_unix = datetime.fromtimestamp(unix_time)
    time_result = datetime_from_unix - datetime.now()
    return int(time_result.total_seconds())
