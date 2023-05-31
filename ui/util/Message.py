class Message:

    def __init__(self, parts: list[(str, int)]):
        self.parts = parts

    def __len__(self):
        acc = 0
        for part in self.parts:
            acc += len(part[0])
        return acc

    def __str__(self):
        acc = ""
        for part in self.parts:
            acc += part[0]
        return acc
