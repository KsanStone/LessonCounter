from ui.interface.Component import Component
from ui.util.ScreenWrapper import ScreenWrapper
from typing import Callable


class TextField(Component):
    text: str
    prefix: str
    submit: Callable[[str], str]

    def __init__(self, text: str = '', prefix: str = '', submit: Callable[[str], str] = lambda x: ''):
        self.focusable = True
        self.submit = submit
        self.text = text
        self.prefix = prefix

    def blit(self, wrapper: ScreenWrapper):
        wrapper.addstr(self.prefix, 0, 0)
        wrapper.addstr(self.text[:(self.width - len(self.prefix))])

    def handle_key(self, keycode):
        try:
            c = chr(keycode)
        except ValueError:
            c = '\0'

        if keycode == ord('\b'):
            self.text = self.text[:-1]
        elif keycode == ord('\n'):
            self.text = self.submit(self.text)
        elif c.isprintable():
            self.text += c
