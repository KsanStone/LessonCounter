from commandProcessor.arguments.CommandArgument import CommandArgument
from commandProcessor.processor.ParsedCommandArguments import ParsedCommandArguments


class CommandArguments:
    """
    Arguments are expected to be in the given order:

    1. Named args, mixed order
    2. Positional args, defined order
    """

    named_arguments: dict[str, CommandArgument]
    positional_arguments: list[CommandArgument]

    def __init__(self):
        self.named_arguments = {}
        self.positional_arguments = []

    def add_named(self, name: str, arg: CommandArgument):
        arg.name = name
        self.named_arguments[name] = arg

    def add_positional(self, arg: CommandArgument):
        arg.name = 'pos_arg'
        if len(self.positional_arguments) > 0 and arg.required and not self.positional_arguments[-1].required:
            raise ValueError('Required positional arguments cannot exist after non-required positional arguments')
        self.positional_arguments.append(arg)

    @staticmethod
    def split_argument_string(argument_string: str):
        arguments = []
        current_argument = ""
        inside_quotes = False
        escaped = False

        for char in argument_string:
            if escaped:
                current_argument += char
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                inside_quotes = not inside_quotes
            elif char == " " and not inside_quotes:
                if current_argument:
                    arguments.append(current_argument)
                    current_argument = ""
            else:
                current_argument += char

        if current_argument:
            arguments.append(current_argument)

        return arguments

    @staticmethod
    def check_missing_arguments(dict_a: dict[str, CommandArgument], dict_b: dict[str, object]):
        missing = []

        for key in dict_a.keys():
            if key not in dict_b and dict_a[key].required:
                missing.append(key)

        if len(missing) > 0:
            raise ValueError(f"Missing argument(s) {missing}")

    def parse(self, argument_string: str) -> ParsedCommandArguments:
        # arg split
        args = CommandArguments.split_argument_string(argument_string)

        # gather named arguments
        named_args_end = 0
        gathered_args = {}
        next_consumed = False
        for i, arg in enumerate(args):
            if next_consumed:
                next_consumed = False
                continue

            if not arg.startswith('-'):
                break

            arg_name = arg[1:]
            if arg_name in gathered_args.keys():
                raise ValueError(f"Duplicate argument '-{arg_name}' provided")
            if arg_name not in self.named_arguments.keys():
                raise ValueError(f"Unknown argument '-{arg_name}' provided")

            cmd_arg = self.named_arguments.get(arg_name)
            if cmd_arg.expects_value and (i + 1 == len(args) or args[i + 1].startswith('-')):
                raise ValueError(f"Missing value for argument '-{arg_name}'")
            elif cmd_arg.expects_value:
                gathered_args[arg_name] = cmd_arg.parse(args[i + 1])
                next_consumed = True
                named_args_end = i + 2
            else:
                gathered_args[arg_name] = None
                named_args_end = i + 1
        CommandArguments.check_missing_arguments(self.named_arguments, gathered_args)

        # gather positional arguments
        positional = []
        for i, arg in enumerate(self.positional_arguments):
            if arg.required and i + named_args_end >= len(args):
                raise ValueError(f'Missing {(i + named_args_end) - len(args) + 1} positional arguments')
            elif not arg.required and i + named_args_end >= len(args):
                break
            else:
                positional.append(arg.parse(args[i + named_args_end]))

        return ParsedCommandArguments(named_arguments=gathered_args, positional_arguments=positional, command_string='')
