import curses
import math

from ui.interface.Component import Component
from ui.util.ScreenWrapper import ScreenWrapper


class ProgressBar(Component):
    percentage: int = 0

    def __init__(self, width: int = None, include_percentage: bool = True, decimals: int = 3,
                 horizontally_centered: bool = False,
                 vertically_centered: bool = False):
        self.bar_width = width
        self.horizontally_centered = horizontally_centered
        self.vertically_centered = vertically_centered
        self.include_percentage = include_percentage
        self.decimals = decimals

    def blit(self, wrapper: ScreenWrapper):
        length = self.width if self.bar_width is None else self.bar_width

        filled = math.floor(length * max(min(self.percentage, 1), 0))
        not_filled = length - filled
        # a = '\u25A0'
        a = ' '
        bar = list(f'[{a * filled}{" " * not_filled}]')
        if self.include_percentage:
            percentage_string = f'{self.percentage * 100:.{self.decimals}f}%'
            center = (length + 2) / 2
            place_at = math.floor(center - len(percentage_string) / 2)
            bar[place_at:place_at + len(percentage_string)] = list(percentage_string)
        wrapper.move(self.height // 2 if self.vertically_centered else 0,
                     self.width // 2 - length // 2 if self.horizontally_centered else 0)
        wrapper.addstr(''.join(bar[0]), color=curses.color_pair(5))
        wrapper.addstr(''.join(bar[1:filled + 1]), color=curses.color_pair(8))
        wrapper.addstr(''.join(bar[1 + filled:]), color=curses.color_pair(5))
