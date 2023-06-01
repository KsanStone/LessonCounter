from ui.interface.Component import Component
from ui.util.Alignment import Alignment, align_2d
from ui.util.Orientation import Orientation
from ui.util.ScreenWrapper import ScreenWrapper


class Separator(Component):
    orientation: Orientation
    alignment: Alignment
    length: int | None

    def __init__(self, height: int = None, width: int = None, length: int = None,
                 orientation: Orientation = Orientation.HORIZONTAL, alignment: Alignment = Alignment.CENTER):
        self.preferred_height = height
        self.preferred_width = width
        self.orientation = orientation
        self.alignment = alignment
        self.length = length

    def __get_len(self):
        if self.length is not None:
            return self.length
        elif self.orientation == Orientation.HORIZONTAL:
            return self.width
        elif self.orientation == Orientation.VERTICAL:
            return self.height

    def blit(self, wrapper: ScreenWrapper):
        length = self.__get_len()
        pos = align_2d((self.width, self.height),
                       (length, 1) if self.orientation == Orientation.HORIZONTAL else (1, length), self.alignment)
        if self.orientation == Orientation.HORIZONTAL:
            wrapper.pretty_line_x(pos[1], pos[0], pos[0] + length - 1)
        elif self.orientation == Orientation.VERTICAL:
            wrapper.pretty_line_y(pos[0], pos[1], pos[1] + length - 1)
