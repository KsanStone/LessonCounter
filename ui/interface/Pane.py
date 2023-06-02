from ui.interface.Component import Component
from ui.util.ScreenWrapper import ScreenWrapper


class Pane(Component):

    children: list[Component]

    def __init__(self):
        self.children = []

    def append_all(self, appended: list[Component]):
        self.clear()
        for child in appended:
            self.append(child)

    def clear(self):
        for child in self.children:
            child.parent = None
        self.children.clear()

    def remove(self, child):
        try:
            self.children.remove(child)
            child.parent = None
        except ValueError:
            pass

    def append(self, child: Component):
        if child.parent is not None:
            child.parent.remove(child)
        child.parent = self
        self.children.append(child)

    def layout(self):
        pass

    def blit(self, wrapper: ScreenWrapper):
        for child in self.children:
            child.blit(wrapper.derive_child(child.y, child.x))
