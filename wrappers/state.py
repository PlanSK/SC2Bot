from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    MINING = auto()
    BUILDING = auto()
    SCOUTING = auto()
    ATTACKING = auto()
    REPAIRING = auto()