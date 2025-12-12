# ne555.py
from core.component import Component
from core.pin import PinDirection


class NE555(Component):
    """
    Digital-accurate NE555 model.
    Pins:
      TRIG  (input)
      THRES (input)
      RESET (input)
      CTRL  (ignored for now)
      OUT   (output)
      DISCH (output)
      VCC, GND (ignored electrically)
    """

    def __init__(self):
        super().__init__("NE555")

        self.add_pin("TRIG", PinDirection.INPUT)
        self.add_pin("THRES", PinDirection.INPUT)
        self.add_pin("RESET", PinDirection.INPUT)
        self.add_pin("OUT", PinDirection.OUTPUT)
        self.add_pin("DISCH", PinDirection.OUTPUT)

        # Internal SR latch
        self.state["Q"] = 0

    def update(self, tick):
        trig = self.pins["TRIG"].read()
        thres = self.pins["THRES"].read()
        reset = self.pins["RESET"].read()

        # RESET dominates
        if reset == 0:
            self.state["Q"] = 0

        else:
            # Trigger comparator (active low)
            if trig == 0:
                self.state["Q"] = 1

            # Threshold comparator (active high)
            if thres == 1:
                self.state["Q"] = 0

        # Outputs
        self.pins["OUT"].write(self.state["Q"])
        self.pins["DISCH"].write(0 if self.state["Q"] else 1)