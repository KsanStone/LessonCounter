from enum import Enum


class ExtendedAsciiLine(Enum):
    VERTICAL = "\u2502"  # │
    HORIZONTAL = "\u2500"  # ─
    TOP_LEFT = "\u250c"  # ┌
    TOP_RIGHT = "\u2510"  # ┐
    BOTTOM_LEFT = "\u2514"  # └
    BOTTOM_RIGHT = "\u2518"  # ┘
    T_LEFT = "\u251c"  # ├
    T_RIGHT = "\u2524"  # ┤
    T_TOP = "\u252c"  # ┬
    T_BOTTOM = "\u2534"  # ┴
    CROSS = "\u253c"  # ┼


class ExtendedAsciiDoubleLine(Enum):
    VERTICAL = "\u2551"  # ║
    HORIZONTAL = "\u2550"  # ═
    TOP_LEFT = "\u2554"  # ╔
    TOP_RIGHT = "\u2557"  # ╗
    BOTTOM_LEFT = "\u255a"  # ╚
    BOTTOM_RIGHT = "\u255d"  # ╝
    T_LEFT = "\u2560"  # ╠
    T_RIGHT = "\u2563"  # ╣
    T_TOP = "\u2566"  # ╦
    T_BOTTOM = "\u2569"  # ╩
    CROSS = "\u256c"  # ╬


if __name__ == '__main__':
    for line in ExtendedAsciiLine:
        print(f"{line.value}")

    for line in ExtendedAsciiDoubleLine:
        print(f"{line.value}")
