from ui.util.ExtendedAsciiLine import ExtendedAsciiLine
from ui.util.Message import Message


class ScreenWrapper:

    def __init__(self, stdscr, x: int, y: int, default_color):
        self.x = x
        self.y = y
        self.stdscr = stdscr
        self.default_color = default_color

    def __get_color(self, color):
        return color if color is not None else self.default_color

    def addstr(self, text, y: int = None, x: int = None, color=None):
        color = self.__get_color(color)

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

    def addch(self, char: str, y: int = None, x: int = None, color=None):
        color = self.__get_color(color)
        self.stdscr.addch(self.y + y, self.x + x, char[0], color)

    def pretty_line_x(self, y, x_1, x_2, color=None):
        for x in range(x_1, x_2 + 1):
            self.addch(ExtendedAsciiLine.HORIZONTAL.value, y, x, color)

    def pretty_line_y(self, x, y_1, y_2, color=None):
        for y in range(y_1, y_2 + 1):
            self.addch(ExtendedAsciiLine.VERTICAL.value, y, x, color)

    def fill(self, char: str, x: int, y: int, width: int, height: int, color=None):
        color = self.__get_color(color)
        filler_str = char[0] * width
        for y in range(y, y + height):
            self.stdscr.addstr(self.y + y, self.x + x, filler_str, color)

    def move(self, y, x):
        self.stdscr.move(self.y + y, self.x + x)

    def derive_child(self, y: int, x: int):
        return ScreenWrapper(self.stdscr, x, y, self.default_color)
