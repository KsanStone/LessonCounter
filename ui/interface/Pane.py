from ui.interface.Component import Component
from ui.util.ScreenWrapper import ScreenWrapper


class Pane(Component):

    children: list[Component]

    def __init__(self):
        self.children = []

    def layout(self):
        pass

    def blit(self, wrapper: ScreenWrapper):
        for child in self.children:
            child.blit(wrapper.derive_child(child.y, child.x))
