import time


def get_unix_time_stamp_milliseconds(datetime):
    return (time.mktime(datetime.timetuple())) * 1000
