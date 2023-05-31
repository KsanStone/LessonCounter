from ui.util.ScreenWrapper import ScreenWrapper


class Component:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    preferred_width: int = None
    preferred_height: int = None

    def blit(self, wrapper: ScreenWrapper):
        pass
