import datetime

from TimingInterval import TimingInterval
from TimingType import TimingType

timings = [
    TimingInterval(TimingType.LESSON, "07:30", "08:15"),
    TimingInterval(TimingType.BREAK, "07:45", "08:25"),

    TimingInterval(TimingType.LESSON, "08:25", "09:10"),
    TimingInterval(TimingType.BREAK, "09:10", "09:20"),

    TimingInterval(TimingType.LESSON, "08:25", "09:10"),
    TimingInterval(TimingType.BREAK, "09:10", "09:20"),

    TimingInterval(TimingType.LESSON, "09:20", "10:05"),
    TimingInterval(TimingType.BREAK, "10:05", "10:15"),

    TimingInterval(TimingType.LESSON, "10:15", "11:00"),
    TimingInterval(TimingType.BREAK, "11:00", "11:15"),

    TimingInterval(TimingType.LESSON, "11:15", "12:00"),
    TimingInterval(TimingType.BREAK, "12:00", "12:10"),

    TimingInterval(TimingType.LESSON, "12:10", "12:55"),
    TimingInterval(TimingType.BREAK, "12:55", "13:05"),

    TimingInterval(TimingType.LESSON, "13:05", "13:50"),
    TimingInterval(TimingType.BREAK, "13:50", "13:55"),

    TimingInterval(TimingType.LESSON, "13:55", "14:40"),
    TimingInterval(TimingType.BREAK, "14:40", "15:00"),

    TimingInterval(TimingType.LESSON, "15:00", "15:45"),
    TimingInterval(TimingType.BREAK, "15:45", "15:50"),

    TimingInterval(TimingType.LESSON, "15:50", "16:35"),
    TimingInterval(TimingType.BREAK, "16:35", "16:45"),

    TimingInterval(TimingType.LESSON, "16:45", "17:30"),
    TimingInterval(TimingType.BREAK, "17:30", "17:35"),

    TimingInterval(TimingType.LESSON, "17:35", "18:20"),
    TimingInterval(TimingType.BREAK, "18:20", "18:25"),

    TimingInterval(TimingType.LESSON, "18:25", "19:10"),
    TimingInterval(TimingType.BREAK, "19:10", "19:15"),

    TimingInterval(TimingType.LESSON, "19:15", "23:59"),
    TimingInterval(TimingType.BREAK, "00:00", "7:30"),
]


def parse_time_as_of_today(t, now):
    t = t.split(":")
    return datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(t[0]), minute=int(t[1]), second=0)


def get_interval_index(now) -> int:
    for i, timing in enumerate(timings):
        t = parse_time_as_of_today(timing.end, now)
        if t > now:
            t = parse_time_as_of_today(timing.start, now)
            if now > t:
                return i
            else:
                return -1
    return -1


def get_interval(index) -> TimingInterval:
    return TimingInterval(TimingType.NONE, "00:00", "00:00") if index == -1 else timings[index]


def get_intervals() -> list[TimingInterval]:
    return timings
