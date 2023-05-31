from enum import Enum


class Alignment(Enum):
    # 1 = unchanged
    # 2 = center
    # 3 = all the way
    #               X        Y
    TOP_LEFT      = (1 << 8) + 1
    TOP_CENTER    = (2 << 8) + 1
    TOP_RIGHT     = (3 << 8) + 1
    CENTER_LEFT   = (1 << 8) + 2
    CENTER        = (2 << 8) + 2
    CENTER_RIGHT  = (3 << 8) + 2
    BOTTOM_LEFT   = (1 << 8) + 3
    BOTTOM_CENTER = (2 << 8) + 3
    BOTTOM_RIGHT  = (3 << 8) + 3


def align_single_axis(size: int, content_size: int, alignment: int):
    match alignment:
        case 1:
            return 0
        case 2:
            return size // 2 - content_size // 2
        case 3:
            return size - content_size


def align_2d(size: tuple[int, int], content_size: tuple[int, int], alignment: Alignment) -> tuple[int, int]:
    return (align_single_axis(size[0], content_size[0], alignment.value >> 8),
            align_single_axis(size[1], content_size[1], alignment.value % 256))
