from enum import Enum
from typing import Any

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class ArmorSlotType(Enum):
    ARMS = "ARMS"
    BACK = "BACK"
    FEET = "FEET"
    HANDS = "HANDS"
    HEAD = "HEAD"
    LEGS = "LEGS"
    OFF_HAND = "OFF_HAND"
    TORSO = "TORSO"
    WAIST = "WAIST"

    @property
    def label(self):
        return _(self.value)
