# 74ls123.py
from core.component import Component
from core.pin import PinDirection


class LS123(Component):
    """74LS123 — Dual retriggerable monostable (digital model)."""

    def __init__(self):
        super().__init__("74LS123")

        for ch in ("A", "B"):
            self.add_pin(f"TRIG{ch}", PinDirection.INPUT)
            self.add_pin(f"CLR{ch}", PinDirection.INPUT)  # active LOW
            self.add_pin(f"Q{ch}", PinDirection.OUTPUT)

        self.state["pulseA"] = 0
        self.state["pulseB"] = 0
        self.state["remA"] = 0
        self.state["remB"] = 0
        self.state["lastA"] = 0
        self.state["lastB"] = 0

        self.PW = 5

    def update(self, tick):
        for ch in ("A", "B"):
            trig = self.pins[f"TRIG{ch}"].read() or 0
            clr = self.pins[f"CLR{ch}"].read() or 1

            pulse = self.state[f"pulse{ch}"]
            rem = self.state[f"rem{ch}"]
            last = self.state[f"last{ch}"]

            if clr == 0:
                pulse = 0
                rem = 0
            else:
                if last == 0 and trig == 1:
                    pulse = 1
                    rem = self.PW

                if rem > 0:
                    rem -= 1
                    if rem == 0:
                        pulse = 0

            self.state[f"pulse{ch}"] = pulse
            self.state[f"rem{ch}"] = rem
            self.state[f"last{ch}"] = trig

            self.pins[f"Q{ch}"].write(pulse)