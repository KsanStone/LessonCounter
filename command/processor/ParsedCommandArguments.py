class ParsedCommandArguments:
    command_string: str
    named_arguments: dict[str, object]
    positional_arguments: list[object]

    def __init__(self, named_arguments: dict[str, object], positional_arguments: list[object], command_string: str):
        self.named_arguments = named_arguments
        self.positional_arguments = positional_arguments
        self.command_string = command_string

    def get(self, index: str | int):
        if type(index) == str:
            return self.named_arguments.get(index)
        else:
            return self.positional_arguments[index]
