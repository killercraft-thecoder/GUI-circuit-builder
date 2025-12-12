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
        "62256 SRAM":SRAM62256
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