from command.arguments.CommandArgument import CommandArgument


class StringArgument(CommandArgument):

    def parse(self, val: str | None) -> any:
        return val
