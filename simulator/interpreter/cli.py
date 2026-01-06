import argparse
import readline
import logging
import sys

from simulator.arduino import Arduino
from simulator.compiler.commands import ArduinoCompiler
from simulator.interpreter.debugger.adb import Debugger
from simulator.interpreter.runtime.interpreter import Interpreter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

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
    parser.add_argument(
        "--arduino-runtime",
        type=str,
        choices=["compiler", "interpreter"],
        default="interpreter",
        help="Choose the runtime that executes Arduino code",
        required=False,
    )

    args = parser.parse_args()

    if args.file.isatty():
        parser.error(message="No filename was specified and stdin is empty.")

    code = args.file.read()

    if args.arduino_runtime == "compiler":
        arduino_runtime = ArduinoCompiler
    else:
        arduino_runtime = Interpreter

    arduino: Arduino = arduino_runtime(code)

    if args.command == "run":
        if arduino.compile(None, None):
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
                case brk if brk.startswith("b"):
                    line_number = int(brk[1:])
                    if debugger.toggle_breakpoint(line_number):
                        break
                    else:
                        print("Line not found.")
                case _:
                    print(
                        f"Command not recognized. Select a valid command.\n{help_prompt}"
                    )


if __name__ == "__main__":
    main()
