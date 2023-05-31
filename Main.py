import curses
import datetime
import time

from FpsCounter import FPSCounter
from LessonSchedule import get_interval_index, get_interval, get_intervals
from TimingType import TimingType
from ui.impl.component.Countdown import Countdown
from ui.impl.component.CurrentPeriod import CurrentPeriod
from ui.impl.component.Label import Label
from ui.impl.pane.HPane import HPane
from ui.impl.pane.VPane import VPane
from ui.util.Alignment import Alignment
from ui.util.ScreenWrapper import ScreenWrapper


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


def construct_ui():
    root_pane = VPane()

    # General information
    fps_label = Label("Fps counter not yet initialized", color=curses.color_pair(4))
    fps_label.preferred_height = 1
    quit_info_label = Label("Press 'q' to quit", color=curses.color_pair(4))
    quit_info_label.preferred_height = 1

    main_content_pane = HPane()

    # Current lessons
    current_lessons = VPane()
    current_period = CurrentPeriod()
    current_period.preferred_height = 4

    before_periods = VPane()
    after_periods = VPane()

    current_lessons.children.append(before_periods)
    filler_label = Label()
    filler_label.preferred_height = 1
    current_lessons.children.append(filler_label)
    current_lessons.children.append(current_period)
    filler_label = Label()
    filler_label.preferred_height = 1
    current_lessons.children.append(filler_label)
    current_lessons.children.append(after_periods)

    # Countdown til end of year
    countdown_pane = VPane()
    end_of_school_year = Countdown(datetime.datetime(year=2023, month=6, day=26, hour=12, minute=0, second=0))
    end_of_school_year.preferred_height = 3
    countdown_pane.children.append(end_of_school_year)

    main_content_pane.children.append(current_lessons)
    main_content_pane.children.append(countdown_pane)

    root_pane.children.append(fps_label)
    root_pane.children.append(main_content_pane)
    root_pane.children.append(quit_info_label)

    return root_pane, fps_label, current_period, before_periods, after_periods, end_of_school_year


def populate_past_and_future_interval_lists(period_index, before_periods, after_periods):
    past_intervals = get_intervals()[:period_index]
    future_intervals = get_intervals()[period_index + 1:]

    extra_past = max(min(before_periods.height - 1, len(past_intervals)), 0)
    extra_future = max(min(after_periods.height - 1, len(future_intervals)), 0)

    offset = len(past_intervals) - extra_past
    before_periods.children.append(
        Label(f'{offset} more' if offset > 0 else '', color=curses.color_pair(4), alignment=Alignment.BOTTOM_CENTER))
    for i in range(0, extra_past):
        label = Label(past_intervals[i + offset].misc_msg(i + offset), alignment=Alignment.TOP_CENTER)
        label.preferred_height = 1
        before_periods.children.append(label)

    for i in range(0, extra_future):
        label = Label(future_intervals[i].misc_msg(i + extra_past + offset + 1), alignment=Alignment.TOP_CENTER)
        label.preferred_height = 1
        after_periods.children.append(label)
    offset = len(future_intervals) - extra_future
    after_periods.children.append(
        Label(f'{offset} more' if offset > 0 else '', color=curses.color_pair(4), alignment=Alignment.TOP_CENTER))

    after_periods.layout()
    before_periods.layout()


def main(stdscr):
    fps_counter = FPSCounter()
    init_colours()
    ui, fps_label, current_period, before_periods, after_periods, end_of_school_year = construct_ui()
    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        height, width = stdscr.getmaxyx()
        ui.width, ui.height = width, height

        now = datetime.datetime.now()
        interval_index = get_interval_index(now)
        interval = get_interval(interval_index)

        if interval.type != TimingType.NONE:
            current_period.update(interval, now)

        end_of_school_year.now = now
        end_of_school_year.update()

        fps_label.text = f'{fps_counter.fps():,d} fps | {fps_counter.last_frame_time()/1_000_000:.2f}ms'

        before_periods.children.clear()
        after_periods.children.clear()

        ui.layout()
        populate_past_and_future_interval_lists(interval_index, before_periods, after_periods)
        stdscr.erase()
        ui.blit(ScreenWrapper(stdscr, 0, 0, curses.color_pair(6)))
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

        # time.sleep(0.25)
        fps_counter.tick()


if __name__ == '__main__':
    curses.wrapper(main)
