# pin.py
from enum import Enum
from typing import Any


class PinDirection(Enum):
    INPUT = "input"
    OUTPUT = "output"
    TRISTATE = "tri"


class Pin:
    """
    Represents a single pin on a component.
    A pin may be connected to multiple wires.
    """
    def __init__(self, name, direction, owner=None):
        self.name = name
        self.direction = direction
        self.owner:Any = owner      # Component that owns this pin
        self.value = None       # 0, 1, or None (high-Z)
        self.wires = []         # list of Wire objects
        self.screen_pos:tuple[int,int] = (0,0) # Position on Screen for renderer

    # ---------------------------------------------------------
    # VALUE ACCESS
    # ---------------------------------------------------------

    def read(self):
        """Return the current value of the pin."""
        return self.value

    def write(self, value):
        """
        Set the pin's output value.
        Only valid for OUTPUT or TRISTATE pins.
        """
        if self.direction == PinDirection.INPUT:
            raise ValueError(
                f"Pin {self.name} on {self.owner.label} is INPUT and cannot drive a value"
            )
        self.value = value

    def is_shorted(self):
        return any(wire.short for wire in self.wires)
    
    def get_screen_pos(self):
        return self.screen_pos

    # ---------------------------------------------------------
    # CONNECTION
    # ---------------------------------------------------------

    def connect(self, wire):
        """Attach this pin to a wire."""
        if wire not in self.wires:
            self.wires.append(wire)

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    def serialize(self):
        return {
            "name": self.name,
            "direction": self.direction.value,
            "value": self.value,
        }