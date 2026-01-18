import enum


class TrsfForm(enum.IntEnum):
    IDENTITY = 0
    ROTATION = 1
    TRANSLATION = 2
    PNTMIRROR = 3
    AX1MIRROR = 4
    AX2MIRROR = 5
    SCALE = 6
    COMPOUNDTRSF = 7
    OTHRR = 8
