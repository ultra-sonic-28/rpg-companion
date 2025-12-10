from enum import Enum
from typing import Any

# Avoid « _ » n’est pas défini `PylancereportUndefinedVariable)`
_: Any

class WeaponHandsType(Enum):
    ONE_HAND = "ONE_HAND"
    TWO_HANDS = "TWO_HANDS"

    @property
    def label(self):
        return _(self.value)
