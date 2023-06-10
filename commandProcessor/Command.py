from commandProcessor.arguments.CommandArguments import CommandArguments
from commandProcessor.processor.ParsedCommandArguments import ParsedCommandArguments


class Command:
    name: str
    arguments: CommandArguments

    def __init__(self, name: str):
        self.arguments = CommandArguments()
        self.name = name

    def execute(self, args: ParsedCommandArguments):
        pass
