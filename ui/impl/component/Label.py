from ui.interface.Component import Component
from ui.util.Alignment import Alignment, align_2d
from ui.util.Message import Message
from ui.util.ScreenWrapper import ScreenWrapper


class Label(Component):
    text: str | Message
    alignment: Alignment
    color: int

    def __init__(self, text: str | Message = "", color=None, alignment: Alignment = Alignment.TOP_LEFT):
        self.text = text
        self.alignment = alignment
        self.color = color

    def blit(self, wrapper: ScreenWrapper):
        pos = align_2d((self.width, self.height), (len(self.text), 1), self.alignment)
        if type(self.text) == str:
            wrapper.addstr(self.text, pos[1], pos[0], self.color)
        else:
            wrapper.addmsg(self.text, pos[1], pos[0])
