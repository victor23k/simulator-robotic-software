import argparse
import readline
import logging
import sys

from simulator.arduino import Arduino
from simulator.interpreter.debugger.adb import Debugger
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
        if arduino.compile(None, None):
            logging.info("All good!!")
        else:
            logging.info("Found some errors :(")

    elif args.command == "debug":
        if arduino.compile(None, None):
            debugger = arduino.debug(None)
            debugger_loop(debugger)


def debugger_loop(debugger: Debugger):
    debugger.start()
    help_prompt = """Commands available:
c (continue)
s (step) 
n (next)
p (print current node)
b[line] (set breakpoint on line)
"""

    print(f"Welcome to the arduino debugger.\n{help_prompt}")
    while debugger.debug_state.stopped.wait():
        if debugger.debug_state.finished:
            debugger.join()
            print("finished debugging")
            break
        while True:
            command = input("adb> ")
            match command:
                case "c":
                    debugger.cont()
                    break
                case "s":
                    debugger.step()
                    break
                case "n":
                    debugger.next()
                    break
                case "p":
                    print(debugger.print())
                case "v":
                    print(debugger.get_values())
                case "h":
                    print(help_prompt)
                case brk if brk.startswith('b'):
                    line_number = int(brk[1:])
                    if debugger.set_breakpoint(line_number):
                        break
                    else:
                        print("Line not found.")
                case _:
                    print(f"Command not recognized. Select a valid command.\n{help_prompt}")


if __name__ == "__main__":
    main()
