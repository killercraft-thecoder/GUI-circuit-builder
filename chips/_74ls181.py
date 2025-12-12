# 74ls181.py
from core.component import Component
from core.pin import PinDirection


class LS181(Component):
    """
    74LS181 — 4-bit ALU.
    Supports 16 logic and 16 arithmetic functions.
    """

    def __init__(self):
        super().__init__("74LS181")

        # Inputs
        for i in range(4):
            self.add_pin(f"A{i}", PinDirection.INPUT)
            self.add_pin(f"B{i}", PinDirection.INPUT)

        for i in range(4):
            self.add_pin(f"S{i}", PinDirection.INPUT)

        self.add_pin("M", PinDirection.INPUT)   # Mode
        self.add_pin("Cn", PinDirection.INPUT)  # Carry in

        # Outputs
        for i in range(4):
            self.add_pin(f"F{i}", PinDirection.OUTPUT)

        self.add_pin("Cn4", PinDirection.OUTPUT)  # Carry out

    def update(self, tick):
        # Read inputs
        A = sum((self.pins[f"A{i}"].read() or 0) << i for i in range(4))
        B = sum((self.pins[f"B{i}"].read() or 0) << i for i in range(4))
        S = sum((self.pins[f"S{i}"].read() or 0) << i for i in range(4))
        M = self.pins["M"].read() or 0
        Cn = self.pins["Cn"].read() or 0

        if M == 1:
            # Logic mode — 16 logic functions
            logic_table = [
                A | B,      # 0000
                ~(A | B),   # 0001
                A | ~B,     # 0010
                ~A,         # 0011
                A & B,      # 0100
                ~(A & B),   # 0101
                A ^ B,      # 0110
                ~A | B,     # 0111
                A,          # 1000
                ~A & B,     # 1001
                B,          # 1010
                ~(A ^ B),   # 1011
                A & ~B,     # 1100
                ~B,         # 1101
                ~(A & ~B),  # 1110
                0xF         # 1111
            ]
            result = logic_table[S] & 0xF
            carry = 0

        else:
            # Arithmetic mode — A + f(B,S) + Cn
            # 181 arithmetic uses a weird internal function table
            f_table = [
                ~A, A | ~B, A | B, 0xF,
                ~(A & B), ~(A & ~B), ~(A ^ B), ~A,
                A, A & ~B, A & B, A,
                A ^ B, B, ~B, 0
            ]
            f = f_table[S] & 0xF
            result = (f + Cn) & 0xF
            carry = 1 if (f + Cn) > 0xF else 0

        # Output
        for i in range(4):
            self.pins[f"F{i}"].write((result >> i) & 1)

        self.pins["Cn4"].write(carry)