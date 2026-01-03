# main.py
import pygame
import sys

from core.engine import Engine
from gui.render import Renderer
from gui.input import InputHandler

# Import chips
from chips.button import Button
from chips.switch import Switch
from chips.led import LED
from chips.clock import Clock
from chips.ne555 import NE555
from chips._28c16 import AT28C16  
from chips._6116 import SRAM6116  
from chips._4017 import CD4017    
from chips._74hc373 import HC373  
from chips._74ls181 import LS181
from chips._74hc165 import HC165
from chips._74hc595 import HC595
from chips._74hc00 import HC00
from chips._74hc08 import HC08
from chips._74hc32 import HC32
from chips._74hc161 import HC161
from chips._74hc193 import HC193
from chips._74hc245 import HC245
from chips._74hc125 import HC125
from chips._74hc138 import HC138
from chips._74hc139 import HC139
from chips._74hc157 import HC157
from chips._74hc153 import HC153
from chips._74hc04 import HC04
from chips._74hc14 import HC14
from chips._74hc74 import HC74
from chips._74hc175 import HC175
from chips._74hc273 import HC273
from chips._74hc85 import HC85
from chips._74hc4040 import HC4040
from chips._74hc4060 import HC4060
from chips._74hc4066 import HC4066
from chips._74hc02 import HC02
from chips._74hc86 import HC86
from chips._62256 import SRAM62256
from chips.cy7c128 import CY7C128
from chips._74hc164 import HC164
from chips._74hc174 import HC174
from chips._74hc244 import HC244
from chips._74hc195 import HC195
from chips._74hc541 import HC541
from chips._74hc191 import HC191
from chips._74hc283 import HC283
from chips._74hc4051 import HC4051
from chips._74hc4052 import HC4052
from chips._74hc4053 import HC4053
from chips._74hc299 import HC299
from chips._74hc646 import HC646
from chips._74hc688 import HC688
from chips._74hc163 import HC163
from chips._74hc107 import HC107
from chips._74hc182 import HC182
from chips._74hc280 import HC280
from chips._74hc381 import HC381
from chips._74hc382 import HC382
from chips._74hc573 import HC573
from chips._74hc574 import HC574
from chips._74hc670 import HC670
from chips._74hc671 import HC671
from chips._74hc150 import HC150
from chips._74hc151 import HC151
from chips._74hc154 import HC154
from chips._74hc238 import HC238
from chips._74hc237 import HC237
from chips._74hc182 import HC182
from chips._74hc280 import HC280
from chips._74hc381 import HC381
from chips._74hc382 import HC382
from chips._74ls47 import LS47
from chips._74ls48 import LS48
from chips._74ls145 import LS145
from chips._74ls147 import LS147
from chips._74ls148 import LS148
from chips._74ls90 import LS90
from chips._74ls93 import LS93
from chips._74ls251 import LS251
from chips._74ls253 import LS253
from chips._74ls367 import LS367
from chips._74ls121 import LS121
from chips._74ls123 import LS123
from chips._74ls138a import LS138A
from chips._74ls240 import LS240
from chips._74ls241 import LS241



def build_chip_registry():
    """
    Returns a dict: label -> class
    Used by the renderer menu and input handler.
    """
    return {
        "Button": Button,
        "Switch": Switch,
        "LED": LED,
        "Clock": Clock,
        "NE555": NE555,
        "28C16 EEPROM": AT28C16,
        "6116 SRAM": SRAM6116,
        "4017 Decade Counter": CD4017,
        "74HC373 Latch": HC373,
        "74LS181 ALU": LS181,
        "74HC165 PISO": HC165,
        "74HC595 SIPO": HC595,
        "74HC00 NAND": HC00,
        "74HC08 AND": HC08,
        "74HC32 OR": HC32,
        "74HC161 Counter": HC161,
        "74HC193 Up/Down Counter": HC193,
        "74HC245 Bus Transceiver": HC245,
        "74HC125 Quad Tri-State Buffer": HC125,
        "74HC138 3-to-8 Decoder": HC138,
        "74HC139 Dual 2-to-4 Decoder": HC139,
        "74HC157 Quad 2-to-1 MUX": HC157,
        "74HC153 Dual 4-to-1 MUX": HC153,
        "74HC04 Hex Inverter": HC04,
        "74HC14 Schmitt Inverter": HC14,
        "74HC74 Dual D Flip-Flop": HC74,
        "74HC175 Quad D Flip-Flop": HC175,
        "74HC273 8-bit Register": HC273,
        "74HC85 4-bit Comparator": HC85,
        "74HC4040 12-bit Counter": HC4040,
        "74HC4060 Oscillator/Counter": HC4060,
        "74HC4066 Quad Analog Switch": HC4066,
        "74HC02 Quad 2-Input NOR Gate":HC02,
        "74HC86 Quad 2-Input XOR Gate":HC86,
        "62256 SRAM":SRAM62256,
        "CY7C128 SRAM":CY7C128,
    "74HC164 8-bit Serial-In Parallel-Out Shift Register": HC164,
    "74HC174 Hex D Flip-Flop": HC174,
    "74HC244 Octal Buffer/Line Driver": HC244,
    "74HC195 Universal 4-bit Shift Register": HC195,
    "74HC541 Octal Buffer/Line Driver": HC541,
    "74HC191 Up/Down Synchronous Counter": HC191,
    "74HC283 4-bit Binary Adder": HC283,
    "74HC4051 8-Channel Analog Multiplexer": HC4051,
    "74HC4052 Dual 4-Channel Analog Multiplexer": HC4052,
    "74HC4053 Triple 2-Channel Analog Switch": HC4053,
    "74HC299 Universal 8-bit Shift Register": HC299,
    "74HC646 Bidirectional 8-bit Shift Register": HC646,
    "74HC688 8-bit Equality Comparator": HC688,
    "74HC163 4-bit Synchronous Counter": HC163,
    "74HC107 Dual JK Flip-Flop": HC107,
    "74HC182 Carry Lookahead Generator": HC182,
    "74HC280 9-bit Parity Generator/Checker": HC280,
    "74HC381 4-bit ALU": HC381,
    "74HC382 4-bit ALU Variant": HC382,
    "74HC573 Octal Transparent Latch": HC573,
"74HC574 Octal D Register": HC574,
"74HC670 4x4 Register File": HC670,
"74HC671 4x4 Register File with Tri-State": HC671,
"74HC150 16-to-1 Multiplexer": HC150,
"74HC151 8-to-1 Multiplexer": HC151,
"74HC154 4-to-16 Decoder": HC154,
"74HC238 3-to-8 Decoder (Active High)": HC238,
"74HC237 3-to-8 Decoder with Latch": HC237,
"74HC182 Carry Lookahead Generator": HC182,
"74HC280 9-bit Parity Generator/Checker": HC280,
"74HC381 4-bit ALU": HC381,
"74HC382 4-bit ALU Variant": HC382,
"74LS47 BCD to 7-Segment Decoder (Active Low)": LS47,
"74LS48 BCD to 7-Segment Decoder (Active High)": LS48,
"74LS145 BCD to Decimal Decoder": LS145,
"74LS147 10-to-4 Priority Encoder": LS147,
"74LS148 8-to-3 Priority Encoder": LS148,
"74LS90 Divide-by-2/5 Decade Counter": LS90,
"74LS93 4-bit Ripple Counter": LS93,
"74LS251 8-to-1 Multiplexer with Tri-State": LS251,
"74LS253 Dual 4-to-1 Multiplexer with Tri-State": LS253,
"74LS367 Hex Buffer/Driver with Tri-State": LS367,
"74LS121 Monostable One-Shot": LS121,
"74LS123 Dual Retriggerable One-Shot": LS123,
"74LS138A 3-to-8 Decoder (TTL Variant)": LS138A,
"74LS240 Octal Inverting Buffer/Driver": LS240,
"74LS241 Octal Buffer/Driver": LS241,
    }

def main():
    pygame.init()
    pygame.display.set_caption("Logic Simulator")

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height),pygame.RESIZABLE)

    clock = pygame.time.Clock()

    engine = Engine()
    chip_registry = build_chip_registry()
    renderer = Renderer(engine, screen, chip_registry)
    input_handler = InputHandler(engine, renderer)

    running = True

    # Simulation speed: number of engine ticks per second
    sim_fps = 60

    while running:
        # -----------------------------
        # EVENT HANDLING
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            input_handler.handle_event(event)

        # -----------------------------
        # SIMULATION TICK
        # -----------------------------
        engine.tick()

        # -----------------------------
        # RENDER
        # -----------------------------
        renderer.draw()

        # -----------------------------
        # FRAME LIMIT
        # -----------------------------
        clock.tick(sim_fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()