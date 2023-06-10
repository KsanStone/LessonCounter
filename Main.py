import curses
import datetime
import time

from FpsCounter import FPSCounter
from LessonSchedule import get_interval_index, get_interval, get_intervals
from Settings import Settings
from commandProcessor.processor.CommandProcessor import CommandProcessor
from commands.FpsCommand import FpsCommand
from ui.application.ApplicationManager import ApplicationManager
from ui.impl.component.Blank import Blank
from ui.impl.component.Countdown import Countdown
from ui.impl.component.CurrentPeriod import CurrentPeriod
from ui.impl.component.Label import Label
from ui.impl.component.Separator import Separator
from ui.impl.component.TextField import TextField
from ui.impl.pane.HPane import HPane
from ui.impl.pane.VPane import VPane
from ui.util.Alignment import Alignment
from ui.util.Orientation import Orientation

settings = Settings()
command_processor = CommandProcessor()


def init_command_processor():
    global settings
    command_processor.register(FpsCommand(settings))


def init_colours():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_BLUE)


def handle_command(command: str) -> str:
    try:
        command_processor.process(command)
        return ''
    except ValueError as e:
        return str(e)


def construct_ui():
    root_pane = VPane()

    # General information
    fps_label = Label("Fps counter not yet initialized", color=curses.color_pair(4))
    fps_label.preferred_height = 1
    command_field = TextField(submit=handle_command, prefix=">|")
    command_field.preferred_height = 1

    main_content_pane = HPane()

    # Current lessons
    current_lessons = VPane()
    current_period = CurrentPeriod()
    current_period.preferred_height = 4

    before_periods = VPane()
    after_periods = VPane()

    current_lessons.append(before_periods)
    current_lessons.append(Blank(1, 1))
    current_lessons.append(current_period)
    current_lessons.append(Blank(1, 1))
    current_lessons.append(after_periods)

    # Countdowns
    countdown_pane = VPane()
    end_of_school_year = Countdown(datetime.datetime(year=2023, month=6, day=23, hour=12, minute=0, second=0),
                                   "End of school year")
    end_of_school_year.preferred_height = 3
    nearest_weekend = Countdown(None, "Weekend")
    nearest_weekend.preferred_height = 3

    countdown_pane.append(end_of_school_year)
    countdown_pane.append(Blank(1, 1))
    countdown_pane.append(nearest_weekend)

    main_content_pane.append(current_lessons)
    main_content_pane.append(Separator(orientation=Orientation.VERTICAL, width=1))
    main_content_pane.append(countdown_pane)

    root_pane.append(fps_label)
    root_pane.append(main_content_pane)
    root_pane.append(command_field)

    return root_pane, fps_label, current_period, before_periods, after_periods, end_of_school_year, nearest_weekend


def populate_past_and_future_interval_lists(period_index, before_periods, after_periods):
    if period_index == -1:
        return

    past_intervals = get_intervals()[:period_index]
    future_intervals = get_intervals()[period_index + 1:]

    extra_past = max(min(before_periods.height - 1, len(past_intervals)), 0)
    extra_future = max(min(after_periods.height - 1, len(future_intervals)), 0)

    offset = len(past_intervals) - extra_past
    before_periods.append(
        Label(f'{offset} more' if offset > 0 else '', color=curses.color_pair(4), alignment=Alignment.BOTTOM_CENTER))
    for i in range(0, extra_past):
        label = Label(past_intervals[i + offset].misc_msg(i + offset), alignment=Alignment.TOP_CENTER)
        label.preferred_height = 1
        before_periods.append(label)

    for i in range(0, extra_future):
        label = Label(future_intervals[i].misc_msg(i + extra_past + offset + 1), alignment=Alignment.TOP_CENTER)
        label.preferred_height = 1
        after_periods.append(label)
    offset = len(future_intervals) - extra_future
    after_periods.append(
        Label(f'{offset} more' if offset > 0 else '', color=curses.color_pair(4), alignment=Alignment.TOP_CENTER))

    after_periods.layout()
    before_periods.layout()


def find_nearest_weekend(today) -> datetime.datetime:
    days_ahead = (5 - today.weekday()) % 7  # Number of days until next Friday
    nearest_weekend = today + datetime.timedelta(days=days_ahead)
    return nearest_weekend


def main(stdscr):
    fps_counter = FPSCounter()
    init_colours()
    init_command_processor()
    ui, fps_label, current_period, before_periods, after_periods, end_of_school_year, nearest_weekend = construct_ui()
    app_manager = ApplicationManager(ui, stdscr)
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)

    while True:
        keycode = stdscr.getch()
        if app_manager.handle_key(keycode):
            break

        now = datetime.datetime.now()
        interval_index = get_interval_index(now)
        interval = get_interval(interval_index)

        current_period.update(interval, now)

        end_of_school_year.now = now
        nearest_weekend.now = now
        nearest_weekend.target = find_nearest_weekend(now)
        end_of_school_year.update()
        nearest_weekend.update()

        fps_label.text = f'{fps_counter.fps():,d} fps | {fps_counter.last_frame_time() / 1_000_000:.2f}ms'

        before_periods.clear()
        after_periods.clear()

        app_manager.layout()
        populate_past_and_future_interval_lists(interval_index, before_periods, after_periods)
        app_manager.blit()

        if settings.fps < 10000:
            time.sleep(1 / settings.fps)
        fps_counter.tick()


if __name__ == '__main__':
    curses.wrapper(main)
