from commandProcessor.arguments.CommandArgument import CommandArgument


class StringArgument(CommandArgument):

    def __init__(self, required: bool, min_len: int | None = None, max_len: int | None = None):
        super().__init__(required, expects_value=True)
        self.min_len = min_len
        self.max_len = max_len

    def parse(self, val: str | None) -> str:
        if self.min_len is not None and len(val) < self.min_len:
            raise ValueError("Provided value is too short")
        elif self.max_len is not None and len(val) > self.max_len:
            raise ValueError("Provided value is too lng")
        return val
