import argparse
import sys

from simulator.arduino import Arduino
from simulator.interpreter.interpreter import Interpreter


def main():
    """Command Line Interface of the Arduino Interpreter."""

    parser = argparse.ArgumentParser(prog="interpino", description=main.__doc__)

    parser.add_argument("command", type=str, choices=["run", "check", "debug"])
    parser.add_argument(
        "-f",
        "--filename",
        default=sys.stdin,
        type=argparse.FileType("r"),
        dest="file",
        help="Path to file containing the Arduino sketch source code. If no path is specified, tries to read from stdin",
    )

    args = parser.parse_args()

    if args.file.isatty():
        parser.error(message="No filename was specified and stdin is empty.")

    code = args.file.read()

    arduino: Arduino = Interpreter(code)

    if args.command == "run":
        arduino.run()

    elif args.command == "check":
        if arduino.check():
            print("All good!!")
        else:
            print("Found some errors:")
            arduino.print_diagnostics()

    elif args.command == "debug":
        print("Debug not implemented yet")
        pass


if __name__ == "__main__":
    main()
