# 74hc595.py
from core.component import Component
from core.pin import PinDirection


class HC595(Component):
    """
    74HC595 — Serial-in, Parallel-out shift register.
    Pins:
      SER, SRCLK, RCLK
      Q0–Q7 outputs
    """

    def __init__(self):
        super().__init__("74HC595")

        self.add_pin("SER", PinDirection.INPUT)
        self.add_pin("SRCLK", PinDirection.INPUT)
        self.add_pin("RCLK", PinDirection.INPUT)

        for i in range(8):
            self.add_pin(f"Q{i}", PinDirection.OUTPUT)

        self.state["shift"] = [0] * 8
        self.state["latch"] = [0] * 8
        self.state["last_srclk"] = 0
        self.state["last_rclk"] = 0

    def update(self, tick):
        ser = self.pins["SER"].read() or 0
        srclk = self.pins["SRCLK"].read() or 0
        rclk = self.pins["RCLK"].read() or 0

        # Shift on rising SRCLK
        if self.state["last_srclk"] == 0 and srclk == 1:
            self.state["shift"] = [ser] + self.state["shift"][:-1]

        # Latch on rising RCLK
        if self.state["last_rclk"] == 0 and rclk == 1:
            self.state["latch"] = self.state["shift"][:]

        self.state["last_srclk"] = srclk
        self.state["last_rclk"] = rclk

        # Output
        for i in range(8):
            self.pins[f"Q{i}"].write(self.state["latch"][i])