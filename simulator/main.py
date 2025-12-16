import argparse
import logging
import simulator.graphics.gui as gui
from simulator.compiler.commands import ArduinoCompiler
from simulator.interpreter.interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--arduino_runtime", type=str, choices=["compiler", "interpreter"],
        default="interpreter", required=False
    )
    parser.add_argument(
        "--log-level", type=str, choices=["debug", "info", "warn"],
        default="info", required=False
    )

    args = parser.parse_args()

    if args.arduino_runtime == "compiler":
        arduino_runtime = ArduinoCompiler
    else:
        arduino_runtime = Interpreter

    logging.basicConfig(level=args.log_level.upper())

    app = gui.MainApplication(arduino_runtime)
    app.mainloop()


if __name__ == "__main__":
    main()
