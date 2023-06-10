from commandProcessor.Command import Command
from commandProcessor.arguments.default.FloatArgument import IntArgument
from commandProcessor.processor.ParsedCommandArguments import ParsedCommandArguments


class FpsCommand(Command):

    def __init__(self):
        super().__init__('fps')
        self.arguments.add_positional(IntArgument(required=True, min_val=1, max_val=10000))

    def execute(self, args: ParsedCommandArguments):
        pass

