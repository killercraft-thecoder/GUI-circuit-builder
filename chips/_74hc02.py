from core.component import Component
from core.pin import Pin,PinDirection

class HC02(Component):
    def __init__(self):
        super().__init__("74HC02")

        self.pins = {
            "A1": Pin("A1", PinDirection.INPUT, self),
            "B1": Pin("B1", PinDirection.INPUT, self),
            "Y1": Pin("Y1", PinDirection.OUTPUT, self),

            "A2": Pin("A2", PinDirection.INPUT, self),
            "B2": Pin("B2", PinDirection.INPUT, self),
            "Y2": Pin("Y2", PinDirection.OUTPUT, self),

            "A3": Pin("A3", PinDirection.INPUT, self),
            "B3": Pin("B3", PinDirection.INPUT, self),
            "Y3": Pin("Y3", PinDirection.OUTPUT, self),

            "A4": Pin("A4", PinDirection.INPUT, self),
            "B4": Pin("B4", PinDirection.INPUT, self),
            "Y4": Pin("Y4", PinDirection.OUTPUT, self),
        }

    def update(self):
        # NOR = NOT (A OR B)
        def nor(a, b):
            if a == 1 or b == 1:
                return 0
            return 1

        self.pins["Y1"].write(nor(self.pins["A1"].read(), self.pins["B1"].read()))
        self.pins["Y2"].write(nor(self.pins["A2"].read(), self.pins["B2"].read()))
        self.pins["Y3"].write(nor(self.pins["A3"].read(), self.pins["B3"].read()))
        self.pins["Y4"].write(nor(self.pins["A4"].read(), self.pins["B4"].read()))