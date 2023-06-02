import curses

from ui.interface.Component import Component
from ui.interface.Pane import Pane
from ui.util.ScreenWrapper import ScreenWrapper


class ApplicationManager:
    root: Component
    quit_key: str

    def __init__(self, root: Component, screen, quit_key = 'q'):
        self.root = root
        self.screen = screen
        self.quit_key = quit_key

    def handle_key(self, keycode):
        if keycode == ord(self.quit_key):
            return True
        return False

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
