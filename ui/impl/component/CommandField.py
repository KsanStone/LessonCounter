import curses

from commandProcessor.processor.CommandProcessor import CommandProcessor
from ui.impl.component.TextField import TextField
import curses.ascii


class CommandField(TextField):

    def __init__(self, processor: CommandProcessor):
        super().__init__()
        self.processor = processor
        self.prefix = ">|"
        self.submit = self.handle_command
        self.is_err = False

    def handle_key(self, keycode):
        if self.is_err:
            self.is_err = False
            self.text = ""
            self.color = curses.color_pair(6)
        super().handle_key(keycode)

    def handle_command(self, command: str) -> str:
        try:
            self.processor.process(command)
            return ''
        except ValueError as e:
            self.is_err = True
            self.color = curses.color_pair(1)
            return str(e)
        except AttributeError:
            self.is_err = True
            self.color = curses.color_pair(1)
            return f'Unknown command'
