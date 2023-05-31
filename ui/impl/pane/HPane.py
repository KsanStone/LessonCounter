from ui.interface.Pane import Pane


class HPane(Pane):

    def layout(self):
        if len(self.children) == 0:
            return

        with_preferred = list(map(lambda x: x.preferred_width,
                                  filter(lambda x: x.preferred_width is not None, self.children)))

        __x = 0
        for i, child, in enumerate(self.children):
            child.y = self.y
            child.height = self.height
            child.x = self.x + __x
            if child.preferred_width is not None:
                child.width = child.preferred_width
                __x += child.preferred_width
                with_preferred.pop(0)
            else:
                tw = (self.width - __x - sum(with_preferred)) // (
                        len(self.children) - i - len(with_preferred))
                child.width = tw
                __x += tw
            if isinstance(child, Pane):
                child.layout()
