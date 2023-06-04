from ui.interface.Pane import Pane


class UiCrawler:

    def __init__(self, root: Pane):
        self.root = root
        self.index = 0
        self.nested_iterator = None
        if not isinstance(root, Pane):
            raise ValueError("Not a pane")

    def __iter__(self):
        return self

    def __inc_index(self):
        if self.index >= len(self.root.children):
            raise StopIteration
        child = self.root.children[self.index]
        self.index += 1
        if isinstance(child, Pane):
            self.nested_iterator = UiCrawler(child)
        return child

    def __next__(self):
        if self.nested_iterator is not None:
            try:
                return next(self.nested_iterator)
            except StopIteration:
                self.nested_iterator = None
                return self.__inc_index()
        else:
            return self.__inc_index()
