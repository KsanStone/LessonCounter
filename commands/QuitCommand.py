from commandProcessor.Command import Command
from commandProcessor.processor.ParsedCommandArguments import ParsedCommandArguments


class QuitCommand(Command):

    def __init__(self):
        super().__init__('quit')

    def execute(self, args: ParsedCommandArguments):
        exit(0)

