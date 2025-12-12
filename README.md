# GUI‑circuit‑builder

GUI‑circuit‑builder is a Python‑based digital logic simulator with a drag‑and‑drop GUI.  
It includes a modular simulation engine, a visual circuit editor, and a growing library of real logic chips.

---

## Features

- Drag‑and‑drop circuit building  
- Click‑to‑wire pin connections  
- Scrollable chip menu with docstring previews  
- Real‑time simulation engine  
- Tri‑state logic and short‑circuit detection  
- Right‑click component deletion  
- LED glow rendering  
- Support for many real ICs (74xx, 40xx, memory, ALU, etc.)

---

## Included Chips

- Basic components: Button, Switch, LED, Clock  
- Logic gates: 74HC00, 74HC08, 74HC32  
- Shift registers: 74HC165, 74HC595  
- Latches and registers: 74HC373  
- Counters: 74HC161, 74HC193, CD4017  
- Memory: 28C16 EEPROM, 6116 SRAM  
- ALU: 74LS181  
- Timer: NE555 (digital model)
- And a ton more!

---

## Running the Simulator
In Bash do:

`pip install pygame` Then `python main.py` in the main folder of the project

Requires Python 3.10+.

---

## Project Structure

core/      engine, wires, pins, components
chips/     individual IC implementations
gui/       renderer + input handler
main.py    program entry point

---

## Contributing

Contributions are welcome.  
See `CONTRIBUTING.md` for guidelines on adding chips, improving the GUI, or extending the engine.

---

## License

MIT License.  
See `LICENSE` for details.
