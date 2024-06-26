import curses
import datetime

from ui.impl.component.Label import Label
from ui.impl.pane.VPane import VPane


class Countdown(VPane):
    target: datetime.datetime
    now: datetime.datetime
    label: str

    def __init__(self, target: datetime.datetime = None, label: str = None):
        super().__init__()
        self.target = target
        self.label = label

    def update(self):
        now = self.now if self.now is not None else datetime.datetime.now()

        if self.target is None:
            self.clear()
            self.append_all([Label("No target", curses.color_pair(1))])
            return

        remaining = self.target - now
        if remaining.total_seconds() < 0:
            self.clear()
            self.append_all([Label("Completed", curses.color_pair(2))])
            return

        self.clear()
        self.append_all([
            Label("Counting down to:" if self.label is None else self.label, curses.color_pair(3)),
            Label(str(self.target), curses.color_pair(4)),
            Label(str(remaining), curses.color_pair(5)),
        ])
