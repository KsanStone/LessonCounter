from ui.util.Message import Message


class ScreenWrapper:

    def __init__(self, stdscr, x: int, y: int, default_color):
        self.x = x
        self.y = y
        self.stdscr = stdscr
        self.default_color = default_color

    def addstr(self, text, y: int = None, x: int = None, color=None):
        if color is None:
            color = self.default_color

        if y is not None and x is not None:
            self.stdscr.addstr(y + self.y, x + self.x, text, color)
        else:
            self.stdscr.addstr(text, color)

    def addmsg(self, text: Message, y: int = None, x: int = None):
        if len(text.parts) == 0:
            return

        if y is not None and x is not None:
            self.stdscr.addstr(y + self.y, x + self.x, text.parts[0][0], text.parts[0][1])
        else:
            self.stdscr.addstr(text.parts[0][0], text.parts[0][1])

        for i in range(1, len(text.parts)):
            self.stdscr.addstr(text.parts[i][0], text.parts[i][1])

    def move(self, y, x):
        self.stdscr.move(self.y + y, self.x + x)

    def derive_child(self, y: int, x: int):
        return ScreenWrapper(self.stdscr, x, y, self.default_color)
