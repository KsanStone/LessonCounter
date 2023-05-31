from ui.interface.Pane import Pane


class VPane(Pane):

    def layout(self):
        if len(self.children) == 0:
            return

        with_preferred = list(map(lambda x: x.preferred_height,
                                  filter(lambda x: x.preferred_height is not None, self.children)))

        __y = 0
        for i, child, in enumerate(self.children):
            child.x = self.x
            child.width = self.width
            child.y = self.y + __y
            if child.preferred_height is not None:
                child.height = child.preferred_height
                __y += child.preferred_height
                with_preferred.pop(0)
            else:
                th = (self.height - __y - sum(with_preferred)) // (
                        len(self.children) - i - len(with_preferred))
                child.height = th
                __y += th
            if isinstance(child, Pane):
                child.layout()
