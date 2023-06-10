from command.arguments.CommandArguments import CommandArguments
from command.processor.ParsedCommandArguments import ParsedCommandArguments


class Command:
    name: str
    arguments: CommandArguments

    def execute(self, args: ParsedCommandArguments):
        pass
