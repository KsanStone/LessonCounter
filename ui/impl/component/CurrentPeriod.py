import curses
import datetime

from LessonSchedule import parse_time_as_of_today
from TimingInterval import TimingInterval
from TimingType import TimingType
from ui.impl.component.Label import Label
from ui.impl.component.ProgressBar import ProgressBar
from ui.impl.pane.VPane import VPane
from ui.util.Alignment import Alignment


class CurrentPeriod(VPane):

    def __init__(self):
        super().__init__()

        self.date_label = Label("", color=curses.color_pair(2), alignment=Alignment.TOP_CENTER)
        self.period_label = Label("", alignment=Alignment.TOP_CENTER)
        self.remaining_label = Label("", color=curses.color_pair(3), alignment=Alignment.TOP_CENTER)
        self.progress_bar = ProgressBar(horizontally_centered=True, width=40)

        self.children.append(self.date_label)
        self.children.append(self.period_label)
        self.children.append(self.remaining_label)
        self.children.append(self.progress_bar)

    def update(self, period: TimingInterval, now: datetime.datetime):
        if period.type == TimingType.NONE:
            self.no_interval(now)
        else:
            lesson_start = parse_time_as_of_today(period.start, now)
            lesson_end = parse_time_as_of_today(period.end, now)
            lesson_percentage = (lesson_end - now).total_seconds() / (lesson_end - lesson_start).total_seconds()

            self.date_label.text = str(now)
            self.period_label.text = period.msg()
            self.remaining_label.text = str(lesson_end - now)
            self.progress_bar.percentage = 1 - lesson_percentage

    def no_interval(self, now: datetime.datetime):
        self.date_label.text = str(now)
        self.period_label.text = "None"
        self.remaining_label.text = "-;-"
        self.progress_bar.percentage = 0
