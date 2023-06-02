from ui.util.ScreenWrapper import ScreenWrapper
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.interface.Pane import Pane


class Component:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    preferred_width: int = None
    preferred_height: int = None
    parent: 'Pane' = None

    def blit(self, wrapper: ScreenWrapper):
        pass
