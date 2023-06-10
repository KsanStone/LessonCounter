import curses.ascii

from ui.interface.Component import Component
from ui.interface.Pane import Pane
from ui.util.ScreenWrapper import ScreenWrapper
from ui.util.UiCrawler import UiCrawler


def focusable(component: Component):
    return component.focusable


class ApplicationManager:
    root: Component
    quit_key: str
    __focused: Component | None

    def __init__(self, root: Component, screen, quit_key='q'):
        self.root = root
        self.screen = screen
        self.__focused = None
        self.quit_key = quit_key

    def handle_key(self, keycode):
        if keycode == ord(self.quit_key) and self.__focused is None:
            return True
        elif keycode == ord('\t'):
            self.advance_focus()
        elif keycode == curses.ascii.ESC:
            if self.__focused is not None:
                self.__focused.focused = False
                self.__focused = None
        elif self.__focused is not None and keycode != -1:
            self.__focused.handle_key(keycode)
        return False

    def advance_focus(self):
        if not isinstance(self.root, Pane):
            return

        if self.__focused is None:
            try:
                elem = next(filter(focusable, UiCrawler(self.root)))
                self.__focused = elem
                self.__focused.focused = True
            except StopIteration:
                pass
            return

        self.__focused.focused = False
        first = None
        get_next = False

        for i, component in enumerate(filter(focusable, UiCrawler(self.root))):
            if i == 0:
                first = component
            if get_next:
                self.__focused = component
                self.__focused.focused = True
                get_next = False
                break
            if component == self.__focused:
                get_next = True

        if get_next and first:
            self.__focused = first
            self.__focused.focused = True

    def layout(self):
        if isinstance(self.root, Pane):
            height, width = self.screen.getmaxyx()
            self.root.width, self.root.height = width, height
            self.root.layout()

    def blit(self):
        try:
            self.screen.erase()
            self.root.blit(ScreenWrapper(self.screen, 0, 0, curses.color_pair(6)))
            self.screen.refresh()
        except Exception as e:
            self.screen.addstr(0, 0, "Blit fail")
            self.screen.addstr(1, 0, f"{e}")

    def get_focused(self):
        return self.__focused
