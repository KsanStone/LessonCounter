import time


class FPSCounter:
    __slots__ = "frames"

    def __init__(self) -> None:
        self.frames = []

    def tick(self):
        self.frames.append(time.time_ns())

    def fps(self):
        now = time.time_ns() - 1_000_000_000
        self.frames = list(filter(lambda x: x > now, self.frames))
        return len(self.frames)

    def last_frame_time(self) -> int:
        if len(self.frames) < 2:
            return 0
        return self.frames[-1] - self.frames[-2]
