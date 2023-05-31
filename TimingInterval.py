import curses

from TimingType import TimingType
from ui.util.Message import Message


class TimingInterval:
    __slots__ = "type", "start", "end"

    def __init__(self, type: TimingType, start: str, end: str):
        self.type = type
        self.start = start
        self.end = end

    def __str__(self):
        return f'{self.type.value: <6} - {self.start} -> {self.end}'

    def msg(self):
        parts = str(self).split(' ')
        return Message([(parts[0] + " ", curses.color_pair(2 if self.type.name == 'LESSON' else 5)),
                        (parts[1] + " ", curses.color_pair(4)), (parts[2] + " ", curses.color_pair(2)),
                        (parts[3] + " ", curses.color_pair(4)), (parts[4] + " ", curses.color_pair(2))])

    def misc_msg(self, index: int):
        return Message([(f'{index:02d}: ', curses.color_pair(4)), (str(self), curses.color_pair(6))])
