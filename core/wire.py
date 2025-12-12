# wire.py
from core.pin import PinDirection


class Wire:
    """
    Represents a wire connecting multiple pins.
    A wire resolves its value based on the pins driving it.
    """
    _id_counter = 1

    def __init__(self):
        self.id = Wire._id_counter
        Wire._id_counter += 1

        self.pins = []      # list of Pin objects
        self.value = None   # 0, 1, or None (high-Z)
        self.short = False  # True if conflicting outputs detected

    # ---------------------------------------------------------
    # CONNECTION
    # ---------------------------------------------------------

    def connect_pin(self, pin):
        if pin not in self.pins:
            self.pins.append(pin)
            pin.connect(self)

    # ---------------------------------------------------------
    # RESOLUTION
    # ---------------------------------------------------------

    def resolve(self):
        """
        Determine the wire's value based on connected output pins.
        Rules:
        - If no outputs drive the wire → high-Z
        - If one output drives → that value
        - If multiple outputs disagree → short circuit
        """
        driven_values = []

        for pin in self.pins:
            if pin.direction in (PinDirection.OUTPUT, PinDirection.TRISTATE):
                if pin.value is not None:
                    driven_values.append(pin.value)

        # No drivers → high-Z
        if len(driven_values) == 0:
            self.value = None
            self.short = False
            return

        # One driver → clean signal
        if len(driven_values) == 1:
            self.value = driven_values[0]
            self.short = False
            return

        # Multiple drivers → check for conflict
        if all(v == driven_values[0] for v in driven_values):
            self.value = driven_values[0]
            self.short = False
        else:
            # Conflict → short circuit
            self.value = None
            self.short = True

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    def serialize(self):
        return {
            "id": self.id,
            "pins": [(pin.name, pin.owner.id) for pin in self.pins],
        }