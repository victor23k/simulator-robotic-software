import argparse
import simulator.graphics.gui as gui
from simulator.compiler.commands import ArduinoCompiler
from simulator.interpreter.interpreter import Interpreter


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--arduino_runtime", type=str, choices=["compiler", "interpreter"],
        default="interpreter", required=False
    )

    args = parser.parse_args()

    if args.arduino_runtime == "compiler":
        arduino_runtime = ArduinoCompiler
    else:
        arduino_runtime = Interpreter

    app = gui.MainApplication(arduino_runtime)
    app.mainloop()


if __name__ == "__main__":
    main()
