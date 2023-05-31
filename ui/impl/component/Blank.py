from ui.interface.Component import Component


class Blank(Component):
    def __init__(self, w, h):
        self.preferred_width = w
        self.preferred_height = h
