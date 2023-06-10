from commandProcessor.Command import Command


class CommandProcessor:
    commands: dict[str, Command]

    def __init__(self):
        self.commands = {}

    def register(self, command: Command):
        self.commands[command.name] = command

    def remove(self, command):
        del self.commands[command.name]

    def process(self, command: str):
        i = command.find(' ')
        command_name = command[:i] if i != -1 else command
        argument_string = command[i+1:] if i != -1 else ''

        command = self.commands.get(command_name)
        parsed_args = command.arguments.parse(argument_string)
        parsed_args.command_string = command
        command.execute(parsed_args)
