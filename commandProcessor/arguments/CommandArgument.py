class CommandArgument:
    name: str | None
    required: bool
    expects_value: bool

    def __init__(self, required: bool, expects_value: bool, name: str = None):
        self.required = required
        self.name = name
        self.expects_value = expects_value

    def parse(self, val: str | None) -> any:
        pass
