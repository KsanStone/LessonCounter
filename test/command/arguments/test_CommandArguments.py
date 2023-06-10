from unittest import TestCase

from commandProcessor.arguments.CommandArguments import CommandArguments
from commandProcessor.arguments.default.FloatArgument import IntArgument
from commandProcessor.arguments.default.StringArgument import StringArgument


class TestCommandArguments(TestCase):

    def test_split_argument_string(self):
        # Test case 1: Basic arguments with unescaped quotes
        argument_string = 'commandProcessor -p "parameter value" --flag'
        expected_arguments = ['commandProcessor', '-p', 'parameter value', '--flag']
        self.assertEqual(CommandArguments.split_argument_string(argument_string), expected_arguments)

        # Test case 2: Empty argument string
        argument_string = ''
        expected_arguments = []
        self.assertEqual(CommandArguments.split_argument_string(argument_string), expected_arguments)

        # Test case 3: Arguments with escaped quotes
        argument_string = 'arg1 "arg\\"2"'
        expected_arguments = ['arg1', 'arg"2']
        self.assertEqual(CommandArguments.split_argument_string(argument_string), expected_arguments)

        # Test case 4: Arguments with no quotes
        argument_string = 'arg1 arg2 arg3'
        expected_arguments = ['arg1', 'arg2', 'arg3']
        self.assertEqual(CommandArguments.split_argument_string(argument_string), expected_arguments)

    def test_parse_positional_arguments(self):
        args = CommandArguments()
        args.add_positional(IntArgument(required=True, min_val=1, max_val=10000))
        command_string = "1000"

        parsed = args.parse(command_string)

        self.assertEqual(parsed.positional_arguments[0], 1000)

    def test_parse_with_missing_named_arguments(self):
        args = CommandArguments()
        args.add_named('name', StringArgument(required=True))
        command_string = "--name"

        with self.assertRaises(ValueError):
            args.parse(command_string)

    def test_parse_with_missing_value_for_named_argument(self):
        args = CommandArguments()
        args.add_named('name', StringArgument(required=True))
        command_string = "--name"

        with self.assertRaises(ValueError):
            args.parse(command_string)

    def test_parse_with_missing_positional_arguments(self):
        args = CommandArguments()
        args.add_positional(StringArgument(required=True))
        command_string = "value1 value2"

        with self.assertRaises(ValueError):
            args.parse(command_string)

    def test_parse_with_extra_positional_arguments(self):
        args = CommandArguments()
        args.add_positional(StringArgument(required=True))
        command_string = "value1"

        with self.assertRaises(ValueError):
            args.parse(command_string)

    def test_parse_valid_command(self):
        args = CommandArguments()
        args.add_named('name', StringArgument(required=True))
        args.add_positional(StringArgument(required=True))
        command_string = "--name value1 value2"

        parsed_args = args.parse(command_string)

        self.assertEqual(parsed_args['name'], 'value1')
        self.assertEqual(parsed_args['positional'], 'value2')
