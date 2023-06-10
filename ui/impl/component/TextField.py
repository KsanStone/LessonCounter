import curses

from ui.interface.Component import Component
from ui.util.ScreenWrapper import ScreenWrapper
from typing import Callable
import curses.ascii


class TextField(Component):
    text: str
    prefix: str
    submit: Callable[[str], str]

    def __init__(self, text: str = '', prefix: str = '', submit: Callable[[str], str] = lambda x: '', color=None):
        self.focusable = True
        self.submit = submit
        self.text = text
        self.prefix = prefix
        self.color = color

    def blit(self, wrapper: ScreenWrapper):
        wrapper.addstr(self.prefix, 0, 0, color=curses.color_pair(4) if self.focused else wrapper.default_color)
        wrapper.addstr(self.text[:(self.width - len(self.prefix))],
                       color=self.color if self.color is not None else wrapper.default_color)

    def handle_key(self, keycode):
        try:
            c = chr(keycode)
        except ValueError:
            c = '\0'

        if keycode == curses.ascii.BS:
            self.text = self.text[:-1]
        elif keycode == curses.ascii.NL:
            self.text = self.submit(self.text)
        elif curses.ascii.isprint(c):
            self.text += c
