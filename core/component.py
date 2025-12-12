# component.py
from enum import Enum
from core.pin import Pin,PinDirection



class Component:
    """
    Base class for all chips/components in the simulator.
    Every chip inherits from this.
    """
    _id_counter = 1

    def __init__(self, label="Component"):
        self.id = Component._id_counter
        Component._id_counter += 1

        self.label = label
        self.pins: dict[str,Pin] = {}      # name -> Pin
        self.position = (0, 0)  # GUI will set this
        self.state = {}     # internal chip state (registers, counters, etc.)

    # ---------------------------------------------------------
    # PIN MANAGEMENT
    # ---------------------------------------------------------

    def add_pin(self, name, direction):
        """Create and register a pin."""
        if name in self.pins:
            raise ValueError(f"Pin {name} already exists on {self.label}")
        self.pins[name] = Pin(name, direction)

    def get_pin(self, name):
        return self.pins[name]

    # ---------------------------------------------------------
    # SIMULATION HOOK
    # ---------------------------------------------------------

    def update(self, tick):
        """
        Override this in subclasses.
        Called once per simulation tick.
        """
        pass

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    def serialize(self):
        """Convert component to a JSON‑friendly dict."""
        return {
            "id": self.id,
            "label": self.label,
            "position": self.position,
            "state": self.state,
            "pins": {
                name: {
                    "direction": pin.direction.value,
                    "value": pin.value
                }
                for name, pin in self.pins.items()
            }
        }

    @classmethod
    def deserialize(cls, data):
        """
        Recreate a component from saved data.
        Subclasses should override this if they have custom state.
        """
        obj = cls(label=data["label"])
        obj.id = data["id"]
        obj.position = tuple(data["position"])
        obj.state = dict(data["state"])

        # Recreate pins
        for name, pinfo in data["pins"].items():
            direction = PinDirection(pinfo["direction"])
            obj.add_pin(name, direction)
            obj.pins[name].value = pinfo["value"]

        return obj