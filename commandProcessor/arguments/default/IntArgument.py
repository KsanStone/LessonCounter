from commandProcessor.arguments.CommandArgument import CommandArgument


class IntArgument(CommandArgument):

    def __init__(self, required: bool, min_val: int | None = None, max_val: int | None = None):
        super().__init__(required, expects_value=True)
        self.min_val = min_val
        self.max_val = max_val

    def parse(self, val: str | None) -> int:
        int_val = int(val)
        if self.min_val is not None and int_val < self.min_val:
            raise ValueError(f"Provided int is smaller than {self.min_val}")
        elif self.max_val is not None and int_val > self.max_val:
            raise ValueError(f"Provided int is larger than {self.max_val}")
        return int_val
